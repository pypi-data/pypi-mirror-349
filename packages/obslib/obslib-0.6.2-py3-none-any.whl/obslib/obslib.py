
import jinja2
import logging
import yaml
import copy
import obslib.exception as exception

from jinja2.meta import find_undeclared_variables

logger = logging.getLogger(__name__)

class Default:
    pass


def validate(val, message, extype=exception.OBSValidationException):
    """
    Convenience method for raising an exception on validation failure
    """
    if not val:
        raise extype(message)


def walk_object(root, callback, *, depth=-1, update=False):
    validate(callable(callback), "Invalid callback supplied to walk_object")
    validate(isinstance(update, bool), "Invalid update flag passed to walk_object")
    validate(isinstance(depth, int), "Invalid depth passed to walk_object")

    # Always visit the top level object
    ret = callback(root)
    if update:
        # If we're updating, this becomes the new root level object to return
        root = ret

    if not isinstance(root, (dict, list)):
        # Nothing else to do for this object
        return root

    visited = set()
    item_list = [(0, root)]

    while len(item_list) > 0:

        level, current = item_list.pop()

        if level > 200:
            raise exception.OBSRecursionLimitException("Exceeded the maximum recursion depth limit")

        if depth >= 0 and level >= depth:
            # Ignore this object as it is too deep
            continue

        # Check if we've seen this object before
        if id(current) in visited:
            continue

        # Save this to the visited list, so we don't revisit again, if there is a loop
        # in the origin object
        visited.add(id(current))

        if isinstance(current, dict):
            for key in current:
                # Call the callback to replace the current object
                ret = callback(current[key])
                if update:
                    current[key] = ret

                if isinstance(current[key], (dict, list)):
                    item_list.append((level + 1, current[key]))
        elif isinstance(current, list):
            index = 0
            while index < len(current):
                ret = callback(current[index])
                if update:
                    current[index] = ret

                if isinstance(current[index], (dict, list)):
                    item_list.append((level + 1, current[index]))

                index = index + 1
        else:
            # Anything non dictionary or list should never have ended up in this list, so this
            # is really an internal error
            raise exception.OBSInternalException(f"Invalid type for resolve in walk_object: {type(current)}")

    return root

def yaml_loader(val):

    # Can only load from a string
    if not isinstance(val, str):
        return (False, None)

    # Try loading document as yaml
    try:
        result = yaml.safe_load(val)
        return (True, result)

    except yaml.YAMLError as e:
        pass

    return (False, None)

def coerce_value(val, types, *, loader=yaml_loader):
    validate(callable(loader) or loader is None, "Invalid loader callback provided to coerce_value")

    # Just return the value if there is no type
    if types is None:
        # Nothing to do here
        return val

    # Wrap a single type in a tuple
    if isinstance(types, type):
        types = (types,)

    # Make sure all elements of the types tuple are a type
    validate(isinstance(types, tuple) and all(isinstance(x, type) for x in types),
        "Invalid types passed to coerce_value")

    for type_item in types:
        # Return val if it is already the correct type
        if isinstance(val, type_item):
            return val

        if type_item == bool:
            try:
                result = parse_bool(val)
                return result
            except:
                pass
        elif type_item == str:
            if val is None:
                # Don't convert None to string. This is likely not wanted.
                continue

            return str(val)

        # None of the above have worked, try using the loader to see if it
        # becomes the correct type
        if loader is not None:
            success, parsed = loader(val)

            if success and isinstance(parsed, type_item):
                return parsed

    raise exception.OBSConversionException(f"Could not convert value to target types: {types}")


def parse_bool(obj) -> bool:
    validate(obj is not None, "None value passed to parse_bool")

    if isinstance(obj, bool):
        return obj

    obj = str(obj)

    if obj.lower() in ["true", "1"]:
        return True

    if obj.lower() in ["false", "0"]:
        return False

    raise exception.OBSConversionException(f"Unparseable value ({obj}) passed to parse_bool")


def eval_vars(source_vars:dict, environment:jinja2.Environment=None, inplace:bool=False, ignore_list:list=None):
    """
    Performs templating on the source dictionary and attempts to resolve variable references
    taking in to account nested references.
    """
    validate(isinstance(source_vars, dict), "Invalid source vars provided to resolve_refs")
    validate(isinstance(inplace, bool), "Invalid inplace var provided to resolve_refs")
    validate(ignore_list is None or (all(isinstance(x, str) for x in ignore_list)),
        "Invalid ignore_list provided to resolve_refs")
    validate(environment is None or isinstance(environment, jinja2.Environment), "Invalid environment passed to eval_vars")

    # Create a default Jinja2 environment
    if environment is None:
        environment = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

    if ignore_list is None:
        ignore_list = []

    var_map = {}

    working_vars = source_vars
    if not inplace:
        working_vars = copy.copy(source_vars)

    # Create a map of keys to the vars the value references
    for key in working_vars:
        deps = set()

        # Recursively walk through all properties for the object and calculate a set
        # of dependencies
        # It's possible that some dependencies could be resolvable, but will show as unresolvable here:
        # If a.b depends on x.y, and x.x depends on a.a, it could, in theory, be resolved, but this will
        # show it as unresolvable.
        # Since we don't have access to that info from jinja2 easily, it would be difficult to calculate
        # and offers little value being a small edge case.
        # Skip calculating dependencies, if the key is in the ignore list, meaning it has no dependencies
        if key not in ignore_list:
            walk_object(working_vars[key], lambda x: deps.update(get_template_refs(x, environment)))

        var_map[key] = deps

    # Loop while there are values left in var_map, which represents the key/value
    # and the vars it depends on
    while len(var_map.keys()) > 0:
        process_list = []

        # Add any keys to the process list that don't have any dependencies left
        for key in var_map:
            if len(var_map[key]) == 0:
                process_list.append(key)

        # Remove the items we're processing from the var map
        for key in process_list:
            var_map.pop(key)

        # Fail if there is nothing to process
        if len(process_list) < 1:
            raise exception.OBSResolveException(
                f"Circular or unresolvable variable references: vars {var_map}"
            )

        for prockey in process_list:
            if prockey not in ignore_list:
                # Template the variable and update 'new_vars', if it's not in the ignore_list
                working_vars[prockey] = walk_object(
                    working_vars[prockey],
                    lambda x: template_if_string(x, environment, working_vars),
                    update=True
                )

            # Remove the variable as a dependency for all other variables
            for key in var_map:
                if prockey in var_map[key]:
                    var_map[key].remove(prockey)

    return working_vars


def template_if_string(source, environment:jinja2.Environment, template_vars:dict, resolve_refs=False, ignore_list=None):
    """
    Template the source object using the supplied environment and vars, if it is a string
    The templated string is returned, or the original object, if it is not a string
    """
    validate(isinstance(environment, jinja2.Environment), "Invalid environment passed to template_string")
    validate(isinstance(template_vars, dict), "Invalid template_vars passed to template_string")
    validate(isinstance(resolve_refs, bool), "Invalid resolve_refs passed to template_if_string")
    validate(isinstance(ignore_list, (list, type(None))), "Invalid ignore_list passed to template_if_string")

    if ignore_list is None:
        ignore_list = []

    if not isinstance(source, str):
        return source

    source_vars = template_vars
    if resolve_refs:

        # We'll create a new dictionary limited to the vars that are
        # directly or indirectly referenced by the source string to avoid
        # evaluating other vars unnecessarily
        limited_vars = dict()

        # Get a list of the references the source string makes
        queue = list(get_template_refs(source, environment))

        while len(queue) > 0:
            item = queue.pop(0)

            # Have we already seen/processed this var?
            if item in limited_vars:
                continue

            # Make sure we have this var in the provided var list
            if item not in template_vars:
                raise exception.OBSResolveException(f"Reference to unknown variable: {item}")

            limited_vars[item] = template_vars[item]

            # Don't check this items references, if it's in the ignore list
            if item in ignore_list:
                continue

            # Add any references for this var to the queue
            for ref in get_template_refs(limited_vars[item], environment):
                queue.append(ref)

        # Now we have a dictionary of the reachable vars from the original source
        # string
        # Flatten/resolve the vars
        source_vars = eval_vars(limited_vars, environment, ignore_list=ignore_list)

    template = environment.from_string(source)
    return template.render(source_vars)


def get_template_refs(template_str, environment:jinja2.Environment):
    """
    Return a set of the variable references from the template string
    """
    if not isinstance(template_str, str):
        return set()

    ast = environment.parse(template_str)
    deps = set(find_undeclared_variables(ast))

    return deps


class Session:
    def __init__(self, template_vars:dict, environment:jinja2.Environment=None, ignore_list=None):
        validate(isinstance(template_vars, dict), "Invalid template vars passed to Session")
        validate(environment is None or isinstance(environment, jinja2.Environment), "Invalid environment passed to Session")
        validate(isinstance(ignore_list, (list, type(None))), "Invalid ignore_list passed to Session")

        # Save the ignore list
        if ignore_list is None:
            ignore_list = []

        self._ignore_list = ignore_list

        # Create a default Jinja2 environment
        if environment is None:
            environment = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

        self._environment = environment
        self.vars = template_vars

    def resolve(self, value, types=None, *, template=True, depth=-1, on_none=Default):
        validate(isinstance(template, bool), "Invalid value for template passed to resolve")
        validate(isinstance(depth, int), "Invalid value for depth passed to resolve")

        if template:
            value = walk_object(value, lambda x: template_if_string(x, self._environment, self.vars, resolve_refs=True, ignore_list=self._ignore_list), update=True, depth=depth)

        if types is not None:
            value = coerce_value(value, types)

        if value is None and on_none != Default:
            return on_none

        return value

def extract_property(source, key, *, on_missing=Default, on_none=Default, remove=True):
    validate(isinstance(source, dict), "Invalid source passed to extract_property. Must be a dict")
    validate(isinstance(key, str), "Invalid key passed to extract_property")
    validate(isinstance(remove, bool), "Invalid remove parameter to extract_property")


    if key not in source:
        if on_missing != Default:
            return on_missing

        # No replace for missing value, so raise error
        raise KeyError(f'Missing key "{key}" in source or value is null')

    # Retrieve value
    if remove:
        val = source.pop(key)
    else:
        val = source[key]

    if val is None and on_none != Default:
        return on_none

    return val


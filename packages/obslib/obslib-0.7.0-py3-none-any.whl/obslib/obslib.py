
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


def find_reachable_vars(source, environment, template_vars):
    """
    Find all of the reachable vars in template_vars based on the template string 'source'.
    Any vars referenced by the source string are evaluated and their references are included,
    until a full list of references have been identified
    A reduced set of the original template vars is returned, limited to the vars reachable from the source string
    """

    # Validate incoming parameters
    validate(isinstance(environment, jinja2.Environment), "Invalid environment passed to find_reachable_vars")
    validate(isinstance(template_vars, dict), "Invalid template vars passed to find_reachable_vars")

    found_vars = dict()

    if not isinstance(source, str):
        return found_vars

    # Get a list of the references the source string makes
    queue = list(get_template_refs(source, environment))

    while len(queue) > 0:
        item = queue.pop(0)

        # Have we already seen this var?
        if item in found_vars:
            continue

        # Check if this is a known var
        if item not in template_vars:
            continue

        found_vars[item] = template_vars[item]

        # Add any references for this var to the queue
        for ref in get_template_refs(found_vars[item], environment):
            queue.append(ref)

    return found_vars


def eval_vars(source_vars:dict, environment:jinja2.Environment=None, ignore_list:list=None):
    """
    Performs templating on the source dictionary and attempts to resolve variable references
    taking in to account nested references.
    """

    # Validate incoming parameters
    validate(isinstance(source_vars, dict), "Invalid source vars provided to eval_vars")
    validate(isinstance(environment, (jinja2.Environment, type(None))), "Invalid environment passed to eval_vars")
    validate(ignore_list is None or (all(isinstance(x, str) for x in ignore_list)),
        "Invalid ignore_list provided to eval_vars")

    # Create a default Jinja2 environment
    if environment is None:
        environment = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

    if ignore_list is None:
        ignore_list = []

    # callback to add dependencies, but only if they appear in the var ist
    def add_template_ref(deps, working_vars, refs):
        for ref in refs:
            if ref in working_vars:
                deps.add(ref)

    # Create a map of keys to the vars the value references
    dep_map = {}
    for key in source_vars:
        dep_map[key] = set()

        if key in ignore_list:
            # If the item is in the ignore list, ignore any dependencies it may have
            # and don't treat it as a template. It will essentially have an empty dependency list
            continue

        # Recursively walk through all properties for the object and calculate a set
        # of dependencies. Note: The object may not be a string, but may be a complex object
        # containing template strings.
        # If there are two complex objects referencing sub-properties of each other, we may not be able to
        # resolve this
        # Only add the dependency if we have it in our working vars, otherwise, we should leave it
        # to jinja2 to process
        walk_object(source_vars[key], lambda x: add_template_ref(dep_map[key], source_vars, get_template_refs(x, environment)))

    # Process each of the dependency sets in var map
    result_vars = {}
    while len(dep_map) > 0:

        # Get a list of the vars that do no have any dependencies and
        # we'll resolve these
        process_list = [x for x in dep_map.keys() if len(dep_map[x]) == 0]

        if len(process_list) == 0:
            # All items in the dep_map have vars with references to other
            # vars in the var map (unknown vars are not added as dependencies)
            # This is unresolvable and attempting to resolve the templates will
            # result in template strings in the output.
            #
            # Example from an eval_vars version that attempts to resolve anyway:
            # >>> test
            # {'a': '{{ b }}', 'b': '{{ a }}'}
            # >> obslib.eval_vars(test)
            # {'a': '{{ a }}', 'b': '{{ a }}'}
            #
            # Best to raise an unresolvable exception and let the user restructure
            # the var references
            raise exception.OBSResolveException(f"Unresolvable references in var list: {dep_map}")

        for prockey in process_list:

            # Remove this key from further processing
            dep_map.pop(prockey)

            # Remove the variable as a dependency for all other variables
            for key in dep_map:
                if prockey in dep_map[key]:
                    dep_map[key].remove(prockey)

            # Put a copy of the var in to the result vars
            result_vars[prockey] = copy.deepcopy(source_vars[prockey])

            # If it's in the ignore list, don't evaluate it using jinja2
            if prockey in ignore_list:
                continue

            # Replace the object with a resolved version of itself. If this
            # is a complex object or collection, just string properties or members
            # will be replaced
            result_vars[prockey] = walk_object(
                result_vars[prockey],
                lambda x: template_if_string(x, environment, result_vars),
                update=True
            )

    return result_vars


def template_if_string(source, environment:jinja2.Environment, template_vars:dict):
    """
    Template the source object using the supplied environment and vars, if it is a string
    The templated string is returned, or the original object, if it is not a string
    """

    # Validate incoming parameters
    validate(isinstance(environment, jinja2.Environment), "Invalid environment passed to template_string")
    validate(isinstance(template_vars, dict), "Invalid template_vars passed to template_string")

    if not isinstance(source, str):
        return source

    template = environment.from_string(source)
    return template.render(template_vars)


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

        # Validate incoming parameters
        validate(isinstance(template, bool), "Invalid value for template passed to resolve")
        validate(isinstance(depth, int), "Invalid value for depth passed to resolve")


        if template:
            def resolve_string(source, environ, template_vars):
                if not isinstance(source, str):
                    # template_if_string would handle this, but we'll avoid calculating vars
                    # unnecessarily if it is not a string
                    return source

                # Calculate a limited version of the vars from template_vars
                limited_vars = find_reachable_vars(source, environ, template_vars)

                # Evaluate the limited scope vars - references to unknown vars would be handled by jinja2,
                # while circular references will cause an obslib exception
                limited_vars = eval_vars(limited_vars, environ, ignore_list=self._ignore_list)

                # return the templated string
                return template_if_string(source, environ, limited_vars)

            value = walk_object(value, lambda x: resolve_string(x, self._environment, self.vars), update=True, depth=depth)

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


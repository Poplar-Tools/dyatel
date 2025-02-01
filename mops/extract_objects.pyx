import inspect
from typing import Any, Union


cpdef dict extract_named_objects(obj: Any, instance: Union[type, tuple] = None):
    """
    Return all objects of given object or by instance
    Removing parent attribute from list to avoid infinite recursion and all dunder attributes

    :returns: dict of page elements and page objects
    """
    elements = {}

    for attribute, value in extract_all_named_objects(obj).items():
        if not instance or isinstance(value, instance):
            if not attribute.startswith('__') and attribute != 'parent':
                elements[attribute] = value

    return elements


cpdef dict extract_all_named_objects(reference_obj: Any):
    """
    Get attributes from the given object and all its bases.

    :param reference_obj: reference object
    :return: dict of all attributes
    """
    cdef dict items = {}
    reference_class = reference_obj if inspect.isclass(reference_obj) else reference_obj.__class__
    all_bases = inspect.getmro(reference_class)

    for parent_class in all_bases[-2::-1]:  # Skip the reference class itself
        if 'ABC' in str(parent_class) or parent_class == object:
            continue

        items.update(get_attributes_from_object(parent_class))

    items.update(get_attributes_from_object(reference_class))
    items.update(get_attributes_from_object(reference_obj))

    return items

cpdef dict get_attributes_from_object(reference_obj: Any):
    """
    Get attributes from the given object.

    :param reference_obj: reference object
    :return: dict of attributes
    """
    return dict(reference_obj.__dict__)

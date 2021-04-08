from typing import Any


def get_object_type_str(obj: Any) -> str:
    return str(type(obj))[8:-2]

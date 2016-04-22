from src.libs.python_utils.functions.function_utils import _identity


def _provide_params(kwarg_key, firebase_key, data, value_func=_identity, **kwargs):
  if kwarg_key in kwargs:
    value = kwargs[kwarg_key]
    if value is None:
      # Setting the value to null will remove it from firebase. This results in the UI layer using defaults
      # in forms (if provided)
      # so, for example, if the user specifically sets the field value to nothing ("") and the default
      # for that field value is "abc", then we don't want "abc" to show up, we want "" to show up.
      data[firebase_key] = ""
    else:
      data[firebase_key] = value_func(value)

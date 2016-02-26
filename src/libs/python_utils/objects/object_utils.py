# http://stackoverflow.com/questions/1389180/python-automatically-initialize-instance-variables
from functools import wraps
import inspect


def initializer(func):
  """
  Automatically assigns the parameters.

  >>> class process:
  ...     @initializer
  ...     def __init__(self, cmd, reachable=False, user='root'):
  ...         pass
  >>> p = process('halt', True)
  >>> p.cmd, p.reachable, p.user
  ('halt', True, 'root')
  """
  names, varargs, keywords, defaults = inspect.getargspec(func)

  @wraps(func)
  def wrapper(self, *args, **kargs):
    for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
      setattr(self, name, arg)

    # http://stackoverflow.com/questions/1389180/python-automatically-initialize-instance-variables#comment43290363_1389216
    for name, default in zip(reversed(names), reversed(defaults or [])):
      if not hasattr(self, name):
        setattr(self, name, default)

    func(self, *args, **kargs)

  return wrapper

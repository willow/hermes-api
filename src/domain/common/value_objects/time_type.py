time_types = ['day', 'month', 'year']


class TimeType():
  def __init__(self, time_type):
    if time_type not in time_types:
      raise Exception('{0} is not a valid time type'.format(time_type))
    else:
      self.time_type = time_type

  @property
  def time_type_date_format(self):
    # basically pluralize
    return '{0}s'.format(self.time_type)

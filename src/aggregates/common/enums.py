from enum import IntEnum


class DurationTypeEnum(IntEnum):
  day = 1
  month = 2
  year = 3

# can be used for admin
DurationTypeChoices = (
  (DurationTypeEnum.day.value, 'Days'),
  (DurationTypeEnum.month.value, 'Months'),
  (DurationTypeEnum.year.value, 'Years'),
)

DurationTypeDict = dict(DurationTypeChoices)

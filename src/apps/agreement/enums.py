from enum import IntEnum


class AgreementTypeEnum(IntEnum):
  consulting = 1
  licensing = 2
  sales = 3


class DurationTypeEnum(IntEnum):
  day = 1
  month = 2
  year = 3

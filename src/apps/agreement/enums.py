from enum import IntEnum


class AgreementTypeEnum(IntEnum):
  consulting = 1
  licensing = 2
  sales = 3

# can be used for admin
AgreementTypeChoices = (
  (AgreementTypeEnum.consulting.value, 'Consulting Agreement'),
  (AgreementTypeEnum.licensing.value, 'Licensing Agreement'),
  (AgreementTypeEnum.sales.value, 'Sales Agreement'),
)

AgreementTypeDict = dict(AgreementTypeChoices)


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

from django_rq import job
from src.aggregates.potential_agreement.services import potential_agreement_service


@job('default')
def send_alerts_for_potential_agreements_task():
  # get list of agreements where the flag is enabled, not created, and date has passed
  potential_agreement_ids_with_due_expiration_alerts = (
    potential_agreement_service
      .get_potential_agreements_with_due_expiration_alert()
      .values_list('potential_agreement_id', flat=True)
    # putting values_list here and not in service becuase my thinking is if the service returns a django object list
    # then we can just return them. if you look at search_service, the service layer actually calls values_list but
    # this layer is returning a custom object (it includes count, results, etc).
  )

  potential_agreement_ids_with_due_outcome_notice_alerts = (
    potential_agreement_service
      .get_potential_agreements_with_due_outcome_notice_alert()
      .values_list('potential_agreement_id', flat=True)
  )

  exp_set = set(potential_agreement_ids_with_due_expiration_alerts)
  outcome_set = set(potential_agreement_ids_with_due_outcome_notice_alerts)
  ids = exp_set.union(outcome_set)

  # the reason i'm doing this in one task is that i'm worried about concurrency conflicts.
  # if we have a bunch of simultaneous tasks modifying the same instances, we could potentially overwrite bool flags
  # which would result in multiple emails going out.
  for pa in ids:
    send_alert_for_potential_agreement_task.delay(pa)


@job('default')
def send_alert_for_potential_agreement_task(potential_agreement_id):
  pa = potential_agreement_service.get_potential_agreement(potential_agreement_id)
  pa.send_expiration_alert_if_due()
  pa.send_outcome_notice_alert_if_due()
  potential_agreement_service.save_or_update(pa)

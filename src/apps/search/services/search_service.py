from django.core.paginator import Paginator
from src.aggregates.agreement.models import Agreement

from src.aggregates.potential_agreement.models import PotentialAgreement


def federated_search(user, query):
  # refer to https://app.asana.com/0/10235149247655/79432408201376 for upgrading the search service
  query = query.strip()

  results = (
    Agreement
      .objects
      .filter(name__icontains=query)
      .filter(user_id=user.id)
      .values_list('id', 'name')
  )

  paged_results = Paginator(results, 3)

  result_items = [{'id': obj[0], 'name': obj[1]} for obj in paged_results.object_list]

  result_set = {'count': paged_results.count, 'results': result_items}

  return result_set


def advanced_search(user, text, counterparty, agreement_type):
  # refer to https://app.asana.com/0/10235149247655/79432408201376 for upgrading the search service

  results = (
    Agreement
      .objects
      .filter(user_id=user.id)
      .values_list('id', 'name')
  )

  if text:
    text = text.strip()
    results = results.filter(name__icontains=text)

  if counterparty:
    counterparty = counterparty.strip()
    results = results.filter(counterparty__iexact=counterparty)

  if agreement_type:
    agreement_type_id = agreement_type.id
    results = results.filter(agreement_type_id=agreement_type_id)

  count = results.count()

  result_items = [{'id': obj[0], 'name': obj[1]} for obj in results]

  result_set = {'count': count, 'results': result_items}

  return result_set

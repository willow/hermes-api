import stripe
from django.conf import settings

from src.libs.payment_utils.exceptions import InvalidCardError, ChargeError

stripe.api_key = settings.STRIPE_SECRET_KEY


def _normalize_error(e):
  if "security code is incorrect" in str(e).lower():
    throw_ex = InvalidCardError("Invalid card info").with_traceback(e.__traceback__)
  else:
    throw_ex = ChargeError("Error processing payment").with_traceback(e.__traceback__)

  return throw_ex


def charge_payment(amount_in_cents, description, token):
  try:
    charge = stripe.Charge.create(
        currency="usd",
        amount=amount_in_cents,
        description=description,
        card=token,
    )

  except stripe.CardError as e:
    throw_ex = _normalize_error(e)

    raise throw_ex

  return charge


def create_customer(customer_email, plan_name, token):
  try:
    # Create a Customer
    customer = stripe.Customer.create(
        email=customer_email,
        plan=plan_name,
        source=token
    )

  except stripe.CardError as e:
    throw_ex = _normalize_error(e)

    raise throw_ex

  return customer

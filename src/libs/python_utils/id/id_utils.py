# http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
import string
import random

chars = string.ascii_letters + string.digits


def generate_id(length=6):
  ret_val = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
  return ret_val

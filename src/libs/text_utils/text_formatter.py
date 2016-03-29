import re

# http://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
def make_alnum(text):
  ret_val = re.sub('\W+', '', text)
  return ret_val

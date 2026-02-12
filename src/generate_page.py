import re

def extract_title(markdown):
  match = re.match(r'#\s+.*\n', markdown)
  h1 = match.group(0).strip()
  print(h1)


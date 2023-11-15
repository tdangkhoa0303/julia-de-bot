SPECIAL_CHARS = [
  '\\',
  '_',
  '*',
  '[',
  ']',
  '(',
  ')',
  '~',
  '>',
  '<',
  '&',
  '#',
  '+',
  '-',
  '=',
  '|',
  '{',
  '}',
  '.',
  '!'
]

def escape_markdown(text: str) -> str:
  escaped_text = text
  for char in SPECIAL_CHARS:
    escaped_text = escaped_text.replace(char, f"\\{char}")
  return escaped_text

import re

# Different regex constructions for checking correct input
is_time = re.compile(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$')
is_server = re.compile('^[А-я]-?[1-4]$')
is_name = re.compile(r'^([А-ЯЁ][А-яЁё,0-9]{1,15}|[A-Z][A-z,0-9]{1,15})$')

"""
Module contain regex templates
"""
import re

# Different regex constructions for checking correct input
time = re.compile(r"(?P<time>(?P<hours>[0-1]?[0-9]|[2][0-3])(?P<separator>.?)(?P<minutes>[0-5][0-9]))")
server = re.compile(
    r"(?P<server>Арши|Арша|"
    r"(?P<name>(Оливия|оливия|Кальфеон|кальфеон|Баленос|баленос|"
    r"Серендия|серендия|Валенсия|валенсия|Медия|медия|Хидель|хидель|[АаОоКкБбСсВвМмХх]))"
    r"(?P<separator>.?)(?P<number>[1-4]))"
)
name = re.compile(r"^(?P<name>([А-ЯЁ][А-яЁё,0-9]{1,15}|[A-Z][A-z,0-9]{1,15}))$")
number = re.compile(r"(?P<number>\d+)")

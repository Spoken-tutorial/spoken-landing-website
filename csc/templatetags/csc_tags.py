from django import template
import datetime
register = template.Library()

def is_today(value):
    print(f'today : {datetime.date.today()}')
    print(f'value : {value}')
    print(f'checking for date equaity : {value == datetime.date.today()}')

    return value == datetime.date.today()

register.filter('is_today', is_today)
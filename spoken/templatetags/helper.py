from django import template

register = template.Library()
def len_cutter(srting, limit):
    # return srting[:limit] + (srting[limit:] and '..')
    return srting[:limit] + '...'

def is_first_in_row(counter):
	return counter in (0,2,4)

def is_last_in_row(counter):
	return counter in (1,3,5)

register.filter('len_cutter', len_cutter)
register.filter('is_first_in_row', is_first_in_row)
register.filter('is_last_in_row', is_last_in_row)
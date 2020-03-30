from django import template

register = template.Library()
def len_cutter(srting, limit):
    # return srting[:limit] + (srting[limit:] and '..')
    return srting[:limit] + '...'

@register.simple_tag
def get_previous_years(current_year):
	previous_year_list = []
	for year in range(current_year-1,2018,-1):
		previous_year_list.append(year)
	return previous_year_list

register.filter('len_cutter', len_cutter)
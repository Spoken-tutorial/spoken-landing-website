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

@register.simple_tag
def get_formatted_year(start,end):
	start_month=''
	end_month=''
	start_day=''
	end_day=''
	formatted_date=''
	#check for year
	if start.year==end.year:
		if start.month==end.month:
			if start.day==end.day:
				formatted_date=start.strftime("%d")+' '+start.strftime("%b")+' '+start.strftime("%Y")
			else:
				formatted_date=start.strftime("%d")+' - '+end.strftime("%d")+' '+start.strftime("%b")+' '+start.strftime("%Y")
		else:
			formatted_date=start.strftime("%d")+' '+start.strftime("%b")+' - '+end.strftime("%d")+' '+end.strftime("%b")+' '+start.strftime("%Y")
	else:
		formatted_date=start.strftime("%d")+' '+start.strftime("%b")+' '+start.strftime("%Y")+' - '+end.strftime("%d")+' '+end.strftime("%b")+' '+end.strftime("%Y")
	return formatted_date

@register.filter(name='has_group') 
def has_group(user, group_name):
	return user.groups.filter(name=group_name).exists() 
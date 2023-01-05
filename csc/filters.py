import django_filters
from django.db.models import Q  
from .models import Test, CSC

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Test
        fields = ['tdate', 'ttime']
        
class TestFilter(django_filters.FilterSet):
    state_choice = [(x['state'],x['state']) for x in CSC.objects.values('state').distinct().order_by('state')]
    city_choice = [(x['city'],x['city']) for x in CSC.objects.values('city').distinct().order_by('city')]
    city_choice = city_choice + [('','----')]
    vle__csc__state = django_filters.ChoiceFilter(choices=state_choice,label="State")
    vle__csc__city = django_filters.ChoiceFilter(choices=city_choice,label="City",required=False)
    vle__user__email = django_filters.CharFilter(lookup_expr='icontains',label="Email")
    name = django_filters.CharFilter(method='name_filter',label="Name")
    # tdate = django_filters.DateFromToRangeFilter()
    
    
    def name_filter(self, queryset, name, value):
        print(f"FILTER ****** {name}")
        print(f"FILTER ****** {value}")
        return queryset.filter(Q(vle__user__first_name=value)|Q(vle__user__last_name=value))
    
    class Meta(object):
        model = Test
        fields = ['vle__csc__state','vle__csc__city','vle__user__email','name']
    # foss = django_filters.ChoiceFilter(choices= [('', '---------')] + list(
    #     FossAvailableForTest.objects.filter(status=1).order_by('foss__foss').values_list('foss__id', 'foss__foss').distinct()))
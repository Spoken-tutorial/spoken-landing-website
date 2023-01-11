import django_filters
from django.forms import DateInput
from django.db.models import Q  
from .models import Test, CSC,FossCategory

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Test
        fields = ['tdate', 'ttime']
        
class TestFilter(django_filters.FilterSet):
    state_choice = [(x['state'],x['state']) for x in CSC.objects.values('state').distinct().order_by('state')]
    city_choice = [(x['city'],x['city']) for x in CSC.objects.values('city').distinct().order_by('city')]
    test_valid_foss = [x['foss'] for x in Test.objects.values('foss').distinct()]
    foss_choice = [(x.id,x.foss) for x in FossCategory.objects.filter(id__in=test_valid_foss)]
    city_choice = city_choice + [('','----')]
    vle__csc__state = django_filters.ChoiceFilter(choices=state_choice,label="State")
    vle__csc__city = django_filters.ChoiceFilter(choices=city_choice,label="City",required=False)
    vle__user__email = django_filters.CharFilter(lookup_expr='icontains',label="Email")
    name = django_filters.CharFilter(method='name_filter',label="Name")
    foss = django_filters.ChoiceFilter(choices=foss_choice,label="Foss",required=False)
    tdate = django_filters.DateFromToRangeFilter()
    
    def __init__(self, *args, **kwargs):
        super(TestFilter, self).__init__(*args, **kwargs)
        state = args[0].get('vle__csc__state','')
        if state:
            choices = [(x['city'],x['city']) for x in CSC.objects.filter(state=state).values('city').distinct().order_by('city')]
            self.filters['vle__csc__city'].extra.update({'choices' : choices})
        
    
    def name_filter(self, queryset, name, value):
        return queryset.filter(Q(vle__user__first_name=value)|Q(vle__user__last_name=value))
        
    class Meta(object):
        model = Test
        fields = ['vle__csc__state','vle__csc__city','vle__user__email','name','foss','tdate']
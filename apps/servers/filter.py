import django_filters
from .models import Server
from django.db.models import Q

class ServerFilter(django_filters.FilterSet):
    hostname = django_filters.CharFilter(method="search_hostname")

    def search_hostname(self, queryset, name, value):
        return queryset.filter(Q(hostname__icontains=value)|Q(ip__icontains=value))

    class Meta:
        model = Server
        fields = ['hostname']
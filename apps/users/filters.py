import django_filters
from django.contrib.auth import get_user_model
User = get_user_model()

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr='contains')

    class Meta:
        model = User
        fields = ['username']

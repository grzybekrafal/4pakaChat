import django_filters
from django.contrib.auth.models import User

class UserFilters(django_filters.rest_framework.FilterSet):
    id = django_filters.NumberFilter(field_name="id", required='required', lookup_expr='exact', help_text="Id")

    class Meta:
        model = User
        fields = [
            'id'
            ]
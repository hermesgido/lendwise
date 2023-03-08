import django_filters

from main.models import Loan

class LoanFilter(django_filters.FilterSet):
    class Meta:
        model = Loan
        fields = ['client', 'loan_amount', 'created_at', 'status', 'interest_rate']
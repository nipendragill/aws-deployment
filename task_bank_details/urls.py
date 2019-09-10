from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user, BankAPIView, BranchesView, BankBranchDetails, BankIFSCDetails
urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view(), name='create_user'),
    url(r'^get_token/$', authenticate_user, name='get_token'),
    url(r'^bank/$', BankAPIView.as_view(), name='bank_info'),
    url(r'^branches', BranchesView.as_view(), name='add_branch'),
    url(r'^ifsc_code/?$', BankIFSCDetails.as_view(), name = 'ifsc_bank_info'),
    url(r'^bank_city/?$', BankBranchDetails.as_view(), name = 'bank_in_city_details')
]
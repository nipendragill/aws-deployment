from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user, BankAPIView, BranchesView, BankBranchDetails, BankIFSCDetails
urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view(), name='create_user'),
    url(r'^get_token/$', authenticate_user, name='get_token'),
    url(r'^bank/$', BankAPIView.as_view(), name='bank_info'),
    url(r'^branches', BranchesView.as_view(), name='add_branch'),
    url(r'^banks/(?P<ifsc_code>[\w-]+)/?$', BankIFSCDetails.as_view(), name = 'ifsc_bank_info'),
    url(r'^city_name/(?P<city_name>[\w-]+)/?$', BankBranchDetails.as_view(), name = 'get_ifsc_bank_details')
]
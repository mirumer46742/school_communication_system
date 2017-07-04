from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from smsapp.views import RegisterView
from smsapp.views import LoginView
from smsapp.views import LogoutView
from smsapp.views import DashboardView
from smsapp.views import SendView
from smsapp.views import BulkUploadView
from smsapp.views import IndexView



urlpatterns=[
	url(r'^$',RegisterView.as_view(),name='register'),
	url(r'^login/$',LoginView.as_view(),name='login'),
	url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
	url(r'^send/$', SendView.as_view(), name='send'),
	url(r'^index/$', SendView.as_view(), name='index'),
	url(r'^bulk_upload/$', BulkUploadView.as_view(), name='bulk_upload'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
# voter_analytics/urls.py
from django.urls import path
from .views import *

urlpatterns = [
	path('', VotersListView.as_view(), name='home'),
	path('voters_list', VotersListView.as_view(), name='voters'),
	path('graphs', GraphsView.as_view(), name='graphs'),
	path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
]
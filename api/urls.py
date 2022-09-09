from django.urls import path, include
from api.views import DownloadMonthlyReport, ProposalSearch, ProposalViewSet, UserSearch

urlpatterns = [
    path('proposal/', ProposalViewSet.as_view({'get': 'list', 'post': 'create'}), name='proposal_viewset'),
    path('proposal/<int:pk>/', ProposalViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='proposal_viewset_indexed'),
    path('user_search/', UserSearch.as_view(), name='user search'),
    path('proposal_search/', ProposalSearch.as_view(), name='proposal search'),
    path('proposal_download/', DownloadMonthlyReport.as_view(), name='proposal download')
]

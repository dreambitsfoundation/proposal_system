from django.urls import path, include
from authentication.views import LoginView, UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='default_user_login'),
    path('user_account/', UserView.as_view(
        http_method_names=['get', 'post', 'put']), name='user_account_view'),
    path('user_account/<int:pk>/', UserView.as_view(
        http_method_names=['delete']), name='user_account_delete_view'),
]

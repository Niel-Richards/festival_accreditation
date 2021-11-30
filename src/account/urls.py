from django.urls import path
from .views import Login, Logout_view, UserList, CreateUser, DisableUser, UserDetail

app_name = 'account'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout_view, name='logout'),
    path('account/', UserList.as_view(), name='user_list'),
    path('account/create/', CreateUser.as_view(), name='create_user'),
    path('account/<int:id>/', UserDetail.as_view(), name='user_detail'),
    path('account/<int:id>/edit/', DisableUser.as_view(), name='disable_user'),

]
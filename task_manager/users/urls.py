from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UsersPage.as_view(), name='users_list'),
    path('create/', views.UserCreate.as_view(), name='create_user'),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/delete/', views.RemoverUser.as_view(), name='delete_user')
]

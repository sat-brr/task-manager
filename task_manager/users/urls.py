from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UsersPage.as_view()),
    path('create/', views.UserCreate.as_view()),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/delete/', views.RemoverUser.as_view(), name='remove_user')
]

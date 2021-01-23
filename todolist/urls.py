from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path("update/<int:pk>/", views.update_task, name="update_task"),
    path("delete/<int:pk>/", views.delete_task, name="delete_task"),
    path("complate/<int:pk>/", views.complate_task, name="complate_task"),
    path('sign_up/', views.sign_up, name="sign_up")
]

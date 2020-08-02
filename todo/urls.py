from django.urls import path, include
from . import views

urlpatterns = [
    path('current/', views.currenttodos, name='currenttodos'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('create/', views.createtodo, name='createtodo'),

    path('<int:todo_id>', views.viewtodo, name='viewtodo'),
    path('<int:todo_id>/completed', views.completedtodo, name='completedtodo'),
    path('<int:todo_id>/delete', views.deletetodo, name='deletetodo')
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.TrangChuView.as_view(), name='trang-chu'),
    path('logout/', views.DangXuatView.as_view, name='logout'),
]

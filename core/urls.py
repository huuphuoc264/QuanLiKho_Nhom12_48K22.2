"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from homepage.views import TrangChuView, DangXuatView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Trang quản trị Django
    path('admin/', admin.site.urls, name='admin'),

    # Đường dẫn đăng nhập và đăng xuất (đã sửa lại để phù hợp với các tên views mới)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', DangXuatView.as_view(), name='logout'),

    # Trang chủ và giới thiệu (đã sửa để dùng class-based view mới)
    path('', TrangChuView.as_view(), name='trang-chu'),

    # Các phần liên quan đến kho hàng
    path('khohang/', include('inventory.urls')),

    # Các giao dịch liên quan đến nhập kho, bán hàng, nhà cung cấp
    path('giaodich/', include('transactions.urls')),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
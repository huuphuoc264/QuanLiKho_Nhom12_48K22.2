from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class CustomLoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Lấy URL của trang login
        login_url = reverse('login')  # Đảm bảo 'login' là tên URL của trang đăng nhập

        # Bỏ qua middleware nếu người dùng đã đăng nhập hoặc đang truy cập trang login
        if request.user.is_authenticated or request.path == login_url:
            return None  # Không chuyển hướng

        # Bỏ qua middleware cho các yêu cầu AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return None

        # Chuyển hướng đến trang đăng nhập nếu người dùng chưa đăng nhập
        return redirect('login')

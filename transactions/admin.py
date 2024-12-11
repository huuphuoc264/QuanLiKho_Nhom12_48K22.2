from django.contrib import admin
from .models import (
    NhaCungCap,
    PhieuNhapKho,
    SanPhamNhapKho,
    PhieuBanHang,
    SanPhamBan,
)

# Đăng ký các model với trang quản trị của Django
admin.site.register(NhaCungCap)
admin.site.register(PhieuNhapKho)
admin.site.register(SanPhamNhapKho)
admin.site.register(PhieuBanHang)
admin.site.register(SanPhamBan)

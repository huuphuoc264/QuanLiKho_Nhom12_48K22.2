from django.urls import path

from . import views

urlpatterns = [
    # Đường dẫn liên quan đến Nhà Cung Cấp (NhaCungCap)
    path('nhacungcap/', views.NhaCungCapListView.as_view(), name='danh-sach-nha-cung-cap'),
    path('nhacungcap/them-moi', views.NhaCungCapCreateView.as_view(), name='nhacungcap-them-moi'),
    path('nhacungcap/<int:pk>/chinh-sua', views.NhaCungCapUpdateView.as_view(), name='nhacungcap-chinh-sua'),
    path('nhacungcap/<int:pk>/xoa', views.NhaCungCapDeleteView.as_view(), name='nhacungcap-xoa'),
    path('nhacungcap/<str:name>', views.NhaCungCapChiTietView.as_view(), name='nhacungcap-chi-tiet'),

    # Đường dẫn liên quan đến Phiếu Nhập Kho (PhieuNhapKho)
    path('nhapkho/', views.PhieuNhapKhoListView.as_view(), name='phieu-nhap'),
    path('nhapkho/them-moi', views.ChonNhaCungCapView.as_view(), name='chon-nhacungcap'),
    path('nhapkho/them-moi/<int:pk>', views.PhieuNhapKhoCreateView.as_view(), name='phieu-nhap-moi'),
    path('nhapkho/<pk>/xoa', views.PhieuNhapKhoDeleteView.as_view(), name='phieu-nhap-xoa'),

    # Đường dẫn liên quan đến Phiếu Bán Hàng (PhieuBanHang)
    path('banhang/', views.PhieuBanHangListView.as_view(), name='phieu-ban'),
    path('banhang/them-moi', views.PhieuBanHangCreateView.as_view(), name='phieu-ban-moi'),
    path('banhang/<int:pk>/xoa', views.PhieuBanHangDeleteView.as_view(), name='phieu-ban-xoa'),

    # Đường dẫn liên quan đến chi tiết phiếu nhập và phiếu bán
    path("nhapkho/<int:so_phieu>", views.PhieuNhapKhoView.as_view(), name="phieu-nhap-xem"),
    path("banhang/<int:so_phieu>", views.PhieuBanHangView.as_view(), name="phieu-ban-xem"),
]

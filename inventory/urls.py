from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn liên quan đến Tồn Kho (TonKho)
    path('', views.TonKhoListView.as_view(), name='tonkho'),
    path('them-moi', views.TonKhoCreateView.as_view(), name='tonkho-them-moi'),
    path('tonkho/<int:pk>/chinh-sua', views.TonKhoUpdateView.as_view(), name='tonkho-chinh-sua'),
    path('tonkho/<int:pk>/xoa', views.TonKhoDeleteView.as_view(), name='tonkho-xoa'),
    path('tonkho/<int:pk>/', views.hang_hoa_chi_tiet, name='hang_hoa_chi_tiet'),
    # Đường dẫn liên quan đến Danh Mục (DanhMuc)
    path('danhmuc', views.DanhMucListView.as_view(), name='danhmuc'),
    path('danhmuc/them-moi', views.DanhMucCreateView.as_view(), name='danhmuc-them-moi'),
    path('danhmuc/<int:pk>/chinh-sua', views.DanhMucUpdateView.as_view(), name='danhmuc-chinh-sua'),
    path('danhmuc/<int:pk>/xoa', views.DanhMucDeleteView.as_view(), name='danhmuc-xoa'),
    path('danhmuc/<int:pk>/', views.danhmuc_chi_tiet, name='danhmuc-chi-tiet'),
]

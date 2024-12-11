from django.shortcuts import render, redirect
from django.views.generic import View
from inventory.models import TonKho
from transactions.models import PhieuBanHang, PhieuNhapKho, SanPhamBan
from django.contrib.auth import logout
from django.db.models import Sum
import json
# Trang chủ (HomeView)
class TrangChuView(View):
    template_name = "home.html"

    def get(self, request):
        # Dữ liệu tồn kho (TonKho)
        ton_kho_queryset = TonKho.objects.filter(da_xoa=False).order_by('-so_luong')
        ton_kho_labels = [item.ten for item in ton_kho_queryset]
        ton_kho_so_luong = [item.so_luong for item in ton_kho_queryset]

        # Sản phẩm bán chạy nhất
        san_pham_ban_chay_queryset = SanPhamBan.objects.values('ton_kho__ten').annotate(
            tong_ban=Sum('so_luong')).order_by('-tong_ban')[:5]
        san_pham_ban_chay_labels = [item['ton_kho__ten'] for item in san_pham_ban_chay_queryset]
        san_pham_ban_chay_values = [float(item['tong_ban']) for item in san_pham_ban_chay_queryset]

        # Phiếu bán hàng gần đây
        phieu_ban = PhieuBanHang.objects.order_by('-thoi_gian')[:5]

        # Phiếu nhập kho gần đây
        phieu_nhap = PhieuNhapKho.objects.order_by('-thoi_gian')[:5]

        # Tổng số phiếu xuất
        tong_so_phieu_xuat = PhieuBanHang.objects.count()

        # Tổng số phiếu nhập
        tong_so_phieu_nhap = PhieuNhapKho.objects.count()

        # Tổng doanh thu từ tất cả các phiếu xuất
        tong_doanh_thu = SanPhamBan.objects.aggregate(total=Sum('thanh_tien'))['total'] or 0
        tong_doanh_thu = float(tong_doanh_thu)

        # Sản phẩm bán chạy nhất (nếu có)
        san_pham_ban_chay_nhat = san_pham_ban_chay_labels[0] if san_pham_ban_chay_labels else "Không có dữ liệu"

        # Xu hướng xuất kho theo ngày
        ngay_xu_huong_xuat_kho = PhieuBanHang.objects.dates('thoi_gian', 'day')
        gia_tri_xu_huong_xuat_kho = [
            float(SanPhamBan.objects.filter(phieu__thoi_gian__date=date).aggregate(tong=Sum('thanh_tien'))['tong'] or 0)
            for date in ngay_xu_huong_xuat_kho
        ]

        # Kiểm tra dữ liệu để đảm bảo không bị trống
        if not ngay_xu_huong_xuat_kho:
            ngay_xu_huong_xuat_kho = ['N/A']
            gia_tri_xu_huong_xuat_kho = [0]

        if not san_pham_ban_chay_labels:
            san_pham_ban_chay_labels = ['N/A']
            san_pham_ban_chay_values = [0]

        # Chuẩn bị dữ liệu cho JavaScript dưới dạng JSON
        context = {
            'tong_so_phieu_xuat': tong_so_phieu_xuat,
            'tong_so_phieu_nhap': tong_so_phieu_nhap,
            'tong_doanh_thu': tong_doanh_thu,
            'san_pham_ban_chay_nhat': san_pham_ban_chay_nhat,
            'ngay_xu_huong_xuat_kho': json.dumps([date.strftime('%d/%m') for date in ngay_xu_huong_xuat_kho]),
            'gia_tri_xu_huong_xuat_kho': json.dumps(gia_tri_xu_huong_xuat_kho),
            'nhan_san_pham_ban_chay': json.dumps(san_pham_ban_chay_labels),
            'gia_tri_san_pham_ban_chay': json.dumps(san_pham_ban_chay_values),
            'ton_kho_labels': json.dumps(ton_kho_labels),
            'ton_kho_so_luong': json.dumps(ton_kho_so_luong),
            'phieu_ban': phieu_ban,
            'phieu_nhap': phieu_nhap
        }

        return render(request, self.template_name, context)

# Đăng xuất người dùng (CustomLogoutView)
class DangXuatView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

from django.db import models
from django.contrib.auth.models import User  # Import model User của Django để lưu thông tin người dùng
from inventory.models import TonKho
# Nhà cung cấp (NhaCungCap)
class NhaCungCap(models.Model):  # Supplier đổi thành NhaCungCap
    id = models.AutoField(primary_key=True)
    ten = models.CharField(max_length=150)  # 'name' đổi thành 'ten'
    so_dien_thoai = models.CharField(max_length=12, unique=True)  # 'phone' đổi thành 'so_dien_thoai'
    dia_chi = models.CharField(max_length=200)  # 'address' đổi thành 'dia_chi'
    email = models.EmailField(max_length=254, unique=True)
    da_xoa = models.BooleanField(default=False)  # 'is_deleted' đổi thành 'da_xoa'

    def __str__(self):
        return self.ten

# Phiếu nhập kho (PhieuNhapKho)
class PhieuNhapKho(models.Model):  # PurchaseBill đổi thành PhieuNhapKho
    so_phieu = models.AutoField(primary_key=True)  # 'billno' đổi thành 'so_phieu'
    thoi_gian = models.DateTimeField(auto_now=True)  # 'time' đổi thành 'thoi_gian'
    nha_cung_cap = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, related_name='nhapkho_nhacungcap')  # 'supplier' đổi thành 'nha_cung_cap'
    giam_gia = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 'discount' đổi thành 'giam_gia'
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Người thực hiện thao tác

    def __str__(self):
        return "Phiếu số: " + str(self.so_phieu)

    def lay_danh_sach_san_pham(self):  # 'get_items_list' đổi thành 'lay_danh_sach_san_pham'
        return SanPhamNhapKho.objects.filter(phieu=self)

    @property
    def tong_gia_tri(self):
        sanpham_list = SanPhamNhapKho.objects.filter(phieu=self)
        return sum(item.so_luong * item.don_gia for item in sanpham_list)

# Các sản phẩm trong phiếu nhập kho (SanPhamNhapKho)
class SanPhamNhapKho(models.Model):  # PurchaseItem đổi thành SanPhamNhapKho
    phieu = models.ForeignKey(PhieuNhapKho, on_delete=models.CASCADE, related_name='phieunhap')  # 'billno' đổi thành 'phieu'
    ton_kho = models.ForeignKey(TonKho, on_delete=models.CASCADE, related_name='sanpham_nhap')  # 'stock' đổi thành 'ton_kho'
    so_luong = models.IntegerField(default=1)  # 'quantity' đổi thành 'so_luong'
    don_gia = models.IntegerField(default=1)  # 'perprice' đổi thành 'don_gia'
    phan_tram_chiet_khau = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # 'discount_percentage' đổi thành 'phan_tram_chiet_khau'
    don_vi_tinh = models.CharField(max_length=50, default="Chiếc")  # 'unit_of_measurement' đổi thành 'don_vi_tinh'
    han_su_dung = models.DateField(null=True, blank=True)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 'totalprice' đổi thành 'thanh_tien'
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Người thực hiện thao tác
    thoi_gian = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Phiếu số: {self.phieu.so_phieu}, Sản phẩm = {self.ton_kho.ten}"

    def save(self, *args, **kwargs):
        # Tính thành tiền sau khi áp dụng chiết khấu
        he_so_chiet_khau = (100 - self.phan_tram_chiet_khau) / 100
        self.thanh_tien = self.so_luong * self.don_gia * he_so_chiet_khau

        if self.pk is None:  # Chỉ thực hiện khi thêm mới, tránh ghi đè khi chỉnh sửa
            ton_kho = self.ton_kho
            ton_kho.so_luong += self.so_luong  # Cập nhật số lượng tồn kho
            ton_kho.gia_nhap = self.don_gia  # Cập nhật giá nhập mới nhất
            ton_kho.save()
        super(SanPhamNhapKho, self).save(*args, **kwargs)

# Phiếu bán hàng (PhieuBanHang)
class PhieuBanHang(models.Model):  # SaleBill đổi thành PhieuBanHang
    so_phieu = models.AutoField(primary_key=True)  # 'billno' đổi thành 'so_phieu'
    thoi_gian = models.DateTimeField(auto_now=True)  # 'time' đổi thành 'thoi_gian'
    ten_nguoi_mua = models.CharField(max_length=150)  # 'name' đổi thành 'ten_nguoi_mua'
    so_dien_thoai = models.CharField(max_length=12)  # 'phone' đổi thành 'so_dien_thoai'
    dia_chi = models.CharField(max_length=200)  # 'address' đổi thành 'dia_chi'
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Người thực hiện thao tác

    def __str__(self):
        return "Phiếu số: " + str(self.so_phieu)

    def lay_danh_sach_san_pham(self):  # 'get_items_list' đổi thành 'lay_danh_sach_san_pham'
        return SanPhamBan.objects.filter(phieu=self)

    @property
    def tong_gia_tri(self):  # 'get_total_price' đổi thành 'tong_gia_tri'
        danh_sach_san_pham = SanPhamBan.objects.filter(phieu=self)
        tong_tien = sum(item.thanh_tien for item in danh_sach_san_pham)
        return tong_tien

# Các sản phẩm trong phiếu bán hàng (SanPhamBan)
class SanPhamBan(models.Model):  # SaleItem đổi thành SanPhamBan
    phieu = models.ForeignKey(PhieuBanHang, on_delete=models.CASCADE, related_name='phieuban')  # 'billno' đổi thành 'phieu'
    ton_kho = models.ForeignKey(TonKho, on_delete=models.CASCADE, related_name='sanpham_ban')  # 'stock' đổi thành 'ton_kho'
    so_luong = models.IntegerField(default=1)  # 'quantity' đổi thành 'so_luong'
    don_gia = models.IntegerField(default=1)  # 'perprice' đổi thành 'don_gia'
    phan_tram_chiet_khau = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Thêm trường chiết khấu
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Người thực hiện thao tác
    thoi_gian = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Tính thành tiền dựa trên đơn giá, số lượng và chiết khấu
        self.thanh_tien = (self.don_gia * self.so_luong) * (1 - self.phan_tram_chiet_khau / 100)
        super(SanPhamBan, self).save(*args, **kwargs)

    def __str__(self):
        return f"Phiếu số: {self.phieu.so_phieu}, Sản phẩm = {self.ton_kho.ten}"

from django.db import models
from django.contrib.auth.models import User
from datetime import date


class DanhMuc(models.Model):  # Danh mục sản phẩm
    id = models.AutoField(primary_key=True)
    ten = models.CharField(max_length=50, unique=True)
    mo_ta = models.TextField(blank=True, null=True)
    da_xoa = models.BooleanField(default=False)

    def __str__(self):
        return self.ten

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"


class TonKho(models.Model):  # Tồn kho
    id = models.AutoField(primary_key=True)
    ten = models.CharField(max_length=100, unique=True)  # Tên sản phẩm
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, related_name='ton_khos', null=True, blank=True)
    so_luong = models.IntegerField(default=0)  # Tổng số lượng tồn kho (cộng dồn từ các lần nhập)
    da_xoa = models.BooleanField(default=False)  # Sản phẩm có bị xóa không
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ton_kho_nguoi_tao')  # Người cập nhật
    hinh_anh = models.ImageField(upload_to='images/', null=True, blank=True)  # Trường lưu ảnh

    def __str__(self):
        return f"{self.ten} (SL: {self.so_luong})"

    def trang_thai_kha_dung(self):  # Kiểm tra trạng thái tồn kho
        if self.so_luong <= 10:
            return "Hết hàng"
        return "Còn hàng"

    class Meta:
        verbose_name = "Tồn kho"
        verbose_name_plural = "Tồn kho"

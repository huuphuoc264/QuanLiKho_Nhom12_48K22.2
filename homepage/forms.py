from django import forms
from django.contrib.auth.models import User
from .models import HoSoNguoiDung


# Form đăng ký người dùng mới
class DangKyNguoiDungForm(forms.ModelForm):
    mat_khau = forms.CharField(widget=forms.PasswordInput(), label="Mật khẩu")
    xac_nhan_mat_khau = forms.CharField(widget=forms.PasswordInput(), label="Xác nhận mật khẩu")
    vai_tro = forms.ChoiceField(choices=HoSoNguoiDung.VAI_TRO_CHOICES, label="Vai trò")

    class Meta:
        model = User
        fields = ['username', 'email', 'mat_khau']

    def clean(self):
        cleaned_data = super().clean()
        mat_khau = cleaned_data.get("mat_khau")
        xac_nhan_mat_khau = cleaned_data.get("xac_nhan_mat_khau")

        if mat_khau != xac_nhan_mat_khau:
            raise forms.ValidationError("Mật khẩu không khớp.")

        return cleaned_data


# Form để cập nhật vai trò người dùng
class CapNhatNguoiDungForm(forms.ModelForm):
    vai_tro = forms.ChoiceField(choices=HoSoNguoiDung.VAI_TRO_CHOICES, label="Vai trò")

    class Meta:
        model = User
        fields = ['username', 'email']

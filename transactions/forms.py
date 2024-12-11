from django import forms
from django.forms import modelformset_factory
from .models import (
    NhaCungCap,
    PhieuNhapKho,
    SanPhamNhapKho,
    PhieuBanHang,
    SanPhamBan,
)
from inventory.models import TonKho

# form dùng để chọn nhà cung cấp (SelectSupplierForm)
class ChonNhaCungCapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cập nhật queryset cho trường 'nha_cung_cap' để chỉ lấy những nhà cung cấp không bị xóa
        self.fields['nha_cung_cap'].queryset = NhaCungCap.objects.filter(da_xoa=False)
        # Thêm class CSS cho trường 'nha_cung_cap' để hiển thị đẹp hơn
        self.fields['nha_cung_cap'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = PhieuNhapKho  # Liên kết form này với model PhieuNhapKho
        fields = ['nha_cung_cap']  # Chỉ lấy trường 'nha_cung_cap' từ model PhieuNhapKho
        labels = {
            'nha_cung_cap': 'Nhà Cung Cấp'  # Đặt nhãn cho trường 'nha_cung_cap'
        }


# form dùng để thêm sản phẩm nhập kho (PurchaseItemForm)
class SanPhamNhapKhoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # Hàm khởi tạo của form, được gọi khi tạo form.
        super().__init__(*args, **kwargs)  # Gọi hàm khởi tạo của lớp cha.
        # Thêm các class CSS và thuộc tính vào trường 'ma_lo'.

        # Định nghĩa widget và format cho trường 'han_su_dung'.
        self.fields['han_su_dung'].widget = forms.DateInput(
            format='%d/%m/%Y',  # Định dạng dd-mm-yyyy
            attrs={
                'class': 'form-control',
                'placeholder': 'dd/mm/yyyy',
            }
        )
        self.fields['han_su_dung'].input_formats = ['%d/%m/%Y']

        # Thiết lập queryset cho trường 'ton_kho' chỉ lấy kho chưa bị xóa.
        self.fields['ton_kho'].queryset = TonKho.objects.filter(da_xoa=False)
        # Thêm các class CSS và thuộc tính vào trường 'ton_kho'.
        self.fields['ton_kho'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})

        # Thêm các class CSS và thuộc tính vào trường 'so_luong' cho phép nhập số lượng.
        self.fields['so_luong'].widget.attrs.update(
            {'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'}
        )

        # Thêm các class CSS và thuộc tính vào trường 'don_gia' để nhập giá.
        self.fields['don_gia'].widget.attrs.update(
            {'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'}
        )

        # Thêm các class CSS và thuộc tính vào trường 'phan_tram_chiet_khau' để nhập phần trăm chiết khấu.
        self.fields['phan_tram_chiet_khau'].widget.attrs.update(
            {'class': 'textinput form-control setprice discount', 'min': '0', 'max': '100', 'required': 'true'}
        )

    class Meta:
        model = SanPhamNhapKho  # Liên kết form này với model SanPhamNhapKho.
        fields = ['ton_kho', 'so_luong', 'don_gia', 'phan_tram_chiet_khau', 'han_su_dung', 'thanh_tien']


# Formset dùng để thêm nhiều sản phẩm nhập kho
SanPhamNhapKhoFormset = modelformset_factory(
    SanPhamNhapKho,  # Tạo formset từ model SanPhamNhapKho.
    form=SanPhamNhapKhoForm,  # Sử dụng form SanPhamNhapKhoForm cho formset.
    extra=1,  # Thêm một form trống mặc định khi người dùng muốn thêm sản phẩm mới.
    can_delete=True  # Cho phép xóa sản phẩm trong formset.
)


# form dùng để thêm hoặc chỉnh sửa thông tin nhà cung cấp (SupplierForm)
class NhaCungCapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Gọi hàm khởi tạo của lớp cha.
        # Thêm thuộc tính CSS vào trường 'ten' để giới hạn nhập ký tự theo pattern (chỉ chữ và khoảng trắng).
        self.fields['ten'].widget.attrs.update(
            {'class': 'textinput form-control', 'pattern': '[a-zA-Z\s]{1,50}', 'title': 'Alphabets and Spaces only'})
        # Thêm thuộc tính CSS và pattern vào trường 'so_dien_thoai' để nhập đúng số điện thoại.
        self.fields['so_dien_thoai'].widget.attrs.update(
            {'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
        # Thêm thuộc tính CSS vào trường 'email' để nhập email.
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = NhaCungCap  # Liên kết form này với model NhaCungCap.
        fields = ['ten', 'so_dien_thoai', 'dia_chi', 'email']  # Các trường cần có trong form.
        widgets = {
            'dia_chi': forms.Textarea(  # Sử dụng widget Textarea cho trường 'dia_chi' để người dùng nhập địa chỉ nhiều dòng.
                attrs={
                    'class': 'textinput form-control',
                    'rows': '4'  # Đặt chiều cao của Textarea thành 4 dòng.
                }
            )
        }


# form dùng để lấy thông tin khách hàng (SaleForm)
class PhieuBanHangForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Gọi hàm khởi tạo của lớp cha.
        # Thêm thuộc tính CSS và pattern vào trường 'ten_nguoi_mua' để nhập đúng tên.
        self.fields['ten_nguoi_mua'].widget.attrs.update(
            {'class': 'textinput form-control', 'pattern': '[a-zA-Z\s]{1,50}', 'title': 'Alphabets and Spaces only', 'required': 'true'})
        # Thêm thuộc tính CSS và pattern vào trường 'so_dien_thoai' để nhập số điện thoại đúng.
        self.fields['so_dien_thoai'].widget.attrs.update(
            {'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only', 'required': 'true'})
        # Thêm thuộc tính CSS vào trường 'email' để nhập email.
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = PhieuBanHang  # Liên kết form này với model PhieuBanHang.
        fields = ['ten_nguoi_mua', 'so_dien_thoai', 'dia_chi', 'email']  # Các trường cần có trong form.
        widgets = {
            'dia_chi': forms.Textarea(  # Sử dụng Textarea cho trường 'dia_chi' để nhập nhiều dòng địa chỉ.
                attrs={
                    'class': 'textinput form-control',
                    'rows': '4'  # Đặt chiều cao của Textarea thành 4 dòng.
                }
            )
        }



# form dùng để thêm sản phẩm bán hàng (SaleItemForm)
class SanPhamBanForm(forms.ModelForm):
    hsd_choices = forms.ChoiceField(
        choices=[],  # Danh sách HSD khởi tạo rỗng
        required=True,
        widget=forms.Select(attrs={'class': 'form-control hsd-dropdown'}),
        label="Hạn sử dụng"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Gọi hàm khởi tạo của lớp cha.

        # Thiết lập queryset cho trường 'ton_kho' chỉ lấy các kho chưa bị xóa.
        self.fields['ton_kho'].queryset = TonKho.objects.filter(da_xoa=False)

        # Thêm thuộc tính CSS vào trường 'ton_kho'.
        self.fields['ton_kho'].widget.attrs.update(
            {'class': 'textinput form-control setprice stock', 'required': 'true'})

        # Thêm thuộc tính CSS vào trường 'so_luong'.
        self.fields['so_luong'].widget.attrs.update(
            {'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'}
        )

        # Thêm thuộc tính CSS vào trường 'don_gia'.
        self.fields['don_gia'].widget.attrs.update(
            {'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'}
        )

        # Thêm trường chiết khấu với thuộc tính CSS.
        self.fields['phan_tram_chiet_khau'] = forms.DecimalField(
            max_digits=5, decimal_places=2, initial=0.0,
            widget=forms.NumberInput(attrs={
                'class': 'textinput form-control setprice discount', 'min': '0', 'max': '100', 'required': 'true'
            })
        )

    def set_hsd_choices(self, hsd_queryset):
        """
        Thiết lập danh sách HSD động cho trường 'hsd_choices' dựa trên sản phẩm được chọn.
        """
        self.fields['hsd_choices'].choices = [
            (hsd.id, hsd.han_su_dung.strftime('%d-%m-%Y')) for hsd in hsd_queryset
        ]

    class Meta:
        model = SanPhamBan  # Liên kết form này với model SanPhamBan.
        fields = ['ton_kho', 'so_luong', 'don_gia', 'phan_tram_chiet_khau', 'thanh_tien']


# Formset dùng để thêm nhiều sản phẩm bán hàng (SanPhamBanFormset)
SanPhamBanFormset = modelformset_factory(
    SanPhamBan,  # Tạo formset từ model SanPhamBan.
    form=SanPhamBanForm,  # Sử dụng form SanPhamBanForm cho formset.
    extra=1,  # Thêm một form trống mặc định khi người dùng muốn thêm sản phẩm mới.
    can_delete=True  # Cho phép xóa sản phẩm trong formset.
)

from django import forms
from .models import TonKho, DanhMuc


# Form cho model 'TonKho'
class TonKhoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Phương thức khởi tạo form.
        Ở đây chúng ta có thể thay đổi thuộc tính widget của các trường trong form.
        """
        super().__init__(*args, **kwargs)

        # Cập nhật thuộc tính widget của trường 'ten' (Tên sản phẩm) để thêm lớp CSS
        self.fields['ten'].widget.attrs.update(
            {'class': 'textinput form-control'})

        # Cập nhật thuộc tính widget của trường 'so_luong' (Số lượng) để thêm lớp CSS và đặt giá trị min = 0
        self.fields['so_luong'].widget.attrs.update(
            {'class': 'textinput form-control', 'min': '0'})

        # Cập nhật thuộc tính widget của trường 'danh_muc' (Danh mục) để thêm lớp CSS
        self.fields['danh_muc'].widget.attrs.update(
            {'class': 'select form-control'})

        # Cập nhật thuộc tính widget của trường 'hinh_anh' (Ảnh bìa) để thêm lớp CSS
        self.fields['hinh_anh'].widget.attrs.update(
            {'class': 'fileinput form-control'})

    class Meta:
        """
        Cấu hình cho form này, bao gồm việc xác định model và các trường cần có trong form.
        """
        model = TonKho  # Chỉ định model mà form này liên kết, ở đây là model TonKho
        fields = ['ten', 'so_luong', 'danh_muc', 'hinh_anh']  # Các trường sẽ xuất hiện trong form.
        # Đặt nhãn cho các trường trong form để hiển thị cho người dùng
        labels = {
            'ten': 'Tên sản phẩm',  # Nhãn hiển thị cho trường 'ten'
            'so_luong': 'Số lượng',  # Nhãn hiển thị cho trường 'so_luong'
            'danh_muc': 'Danh mục',  # Nhãn hiển thị cho trường 'danh_muc'
            'hinh_anh': 'Ảnh bìa',  # Nhãn hiển thị cho trường 'hinh_anh'
        }


# Form cho model 'DanhMuc'
class DanhMucForm(forms.ModelForm):  # CategoryForm đổi thành DanhMucForm
    class Meta:
        """
        Cấu hình cho form DanhMucForm.
        Đây là form cho model DanhMuc (Danh mục).
        """
        model = DanhMuc  # Chỉ định model mà form này liên kết, ở đây là model DanhMuc
        fields = ['ten', 'mo_ta']  # Các trường sẽ xuất hiện trong form. Các trường này được lấy từ model DanhMuc
        # Đặt nhãn cho các trường trong form để hiển thị cho người dùng
        labels = {
            'ten': 'Tên danh mục',  # Nhãn hiển thị cho trường 'ten' (Tên danh mục)
            'mo_ta': 'Mô tả',  # Nhãn hiển thị cho trường 'mo_ta' (Mô tả danh mục)
        }

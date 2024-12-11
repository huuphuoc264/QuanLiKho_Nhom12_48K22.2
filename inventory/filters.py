import django_filters
from .models import TonKho, DanhMuc

class TonKhoFilter(django_filters.FilterSet):  # StockFilter đổi thành TonKhoFilter
    ten = django_filters.CharFilter(lookup_expr='icontains')  # 'name' đổi thành 'tên' - cho phép lọc không cần nhập đầy đủ tên

    class Meta:
        model = TonKho
        fields = ['ten']  # 'name' đổi thành 'tên'


class DanhMucFilter(django_filters.FilterSet):  # CategoryFilter đổi thành DanhMucFilter
    class Meta:
        model = DanhMuc
        fields = ['ten']  # 'name' đổi thành 'tên'

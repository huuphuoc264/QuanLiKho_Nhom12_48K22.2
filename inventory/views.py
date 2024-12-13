from django.shortcuts import render, redirect, \
    get_object_or_404  # Các hàm hỗ trợ render, redirect và lấy đối tượng từ DB.
from django.views.generic import (
    View,  # View cơ bản trong Django cho các thao tác đơn giản.
    CreateView,  # Lớp view để tạo mới đối tượng trong cơ sở dữ liệu.
    UpdateView  # Lớp view để cập nhật đối tượng trong cơ sở dữ liệu.
)
from django.contrib.messages.views import \
    SuccessMessageMixin  # Mixin để hiển thị thông báo thành công sau khi thực hiện thao tác.
from django.contrib import messages  # Module cho phép gửi thông báo cho người dùng.
from .models import TonKho, DanhMuc  # Import các mô hình TonKho (sản phẩm tồn kho) và DanhMuc (danh mục sản phẩm).
from .forms import TonKhoForm, DanhMucForm  # Import các form để tạo và cập nhật TonKho và DanhMuc.
from django_filters.views import FilterView  # Lớp view hỗ trợ lọc dữ liệu với Django Filters.
from .filters import TonKhoFilter, DanhMucFilter  # Các bộ lọc dùng để lọc TonKho và DanhMuc.
from django.urls import reverse_lazy  # Hàm giúp lấy URL của view bằng tên view (chỉ thực hiện khi cần).
from transactions.models import SanPhamNhapKho
from django.db.models import Sum

class TonKhoListView(FilterView):  # Lớp view để hiển thị danh sách các sản phẩm tồn kho với khả năng lọc.
    filterset_class = TonKhoFilter  # Bộ lọc áp dụng lên queryset để lọc sản phẩm.
    queryset = TonKho.objects.filter(da_xoa=False)  # Lấy tất cả sản phẩm tồn kho chưa bị xóa (da_xoa=False).
    template_name = 'inventory.html'  # Template dùng để hiển thị danh sách sản phẩm tồn kho.
    paginate_by = 10  # Phân trang, mỗi trang sẽ hiển thị tối đa 10 sản phẩm.

    def get_queryset(self):
        queryset = super().get_queryset()
        danh_muc_id = self.request.GET.get('danh_muc')
        if danh_muc_id:
            queryset = queryset.filter(danh_muc_id=danh_muc_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['danh_muc_list'] = DanhMuc.objects.filter(da_xoa=False)
        return context

class TonKhoCreateView(SuccessMessageMixin, CreateView):  # Lớp view để tạo mới sản phẩm tồn kho.
    model = TonKho  # Mô hình TonKho được sử dụng để tạo sản phẩm.
    form_class = TonKhoForm  # Form được sử dụng để nhập dữ liệu sản phẩm.
    template_name = "edit_stock.html"  # Template hiển thị form thêm sản phẩm mới.
    success_url = reverse_lazy('tonkho')  # Sau khi tạo sản phẩm thành công, chuyển hướng về danh sách sản phẩm tồn kho.
    success_message = "Thêm sản phẩm mới thành công"  # Thông báo thành công khi tạo mới sản phẩm.

    def get_context_data(self, **kwargs):  # Thêm dữ liệu context cho template.
        context = super().get_context_data(**kwargs)  # Lấy dữ liệu context mặc định từ lớp cha.
        context["title"] = 'Thêm sản phẩm mới'  # Thêm tiêu đề trang vào context.
        context["savebtn"] = 'Lưu'  # Thêm nhãn nút "Lưu" vào context.
        return context

    def form_valid(self, form):
        # Debug để kiểm tra file
        if 'hinh_anh' in self.request.FILES:
            print("File upload:", self.request.FILES['hinh_anh'])  # Debug
            form.instance.hinh_anh = self.request.FILES['hinh_anh']
        return super().form_valid(form)



class TonKhoUpdateView(SuccessMessageMixin, UpdateView):  # Lớp view để cập nhật thông tin sản phẩm tồn kho.
    model = TonKho  # Mô hình TonKho được sử dụng để cập nhật sản phẩm.
    form_class = TonKhoForm  # Form được sử dụng để chỉnh sửa thông tin sản phẩm.
    template_name = "edit_stock.html"  # Template hiển thị form chỉnh sửa sản phẩm.
    success_url = reverse_lazy('tonkho')  # Sau khi cập nhật thành công, chuyển hướng về danh sách sản phẩm tồn kho.
    success_message = "Sản phẩm được cập nhật thành công"  # Thông báo thành công khi cập nhật sản phẩm.

    def get_context_data(self, **kwargs):  # Thêm dữ liệu context cho template.
        context = super().get_context_data(**kwargs)  # Lấy dữ liệu context mặc định từ lớp cha.
        context["title"] = 'Chỉnh sửa thông tin hàng hóa'  # Thêm tiêu đề trang vào context.
        context["savebtn"] = 'Cập nhật'  # Thêm nhãn nút "Cập nhật" vào context.
        context["delbtn"] = 'Xóa'  # Thêm nhãn nút "Xóa" vào context.
        return context


class TonKhoDeleteView(View):  # Lớp view để xóa (thực chất là đánh dấu đã xóa) một sản phẩm tồn kho.
    template_name = "delete_stock.html"  # Template hiển thị trang xác nhận xóa sản phẩm.
    success_message = "Xóa hàng hóa thành công"  # Thông báo thành công khi xóa sản phẩm.
    success_url = reverse_lazy('tonkho')  # Sau khi xóa thành công, chuyển hướng về danh sách sản phẩm tồn kho.

    def get(self, request, pk):  # Xử lý yêu cầu GET (hiển thị trang xác nhận xóa).
        ton_kho = get_object_or_404(TonKho,
                                    pk=pk)  # Lấy sản phẩm tồn kho theo ID, nếu không tìm thấy thì trả về lỗi 404.
        return render(request, self.template_name, {'object': ton_kho})  # Hiển thị trang xác nhận xóa.

    def post(self, request, pk):  # Xử lý yêu cầu POST (người dùng xác nhận xóa).
        ton_kho = get_object_or_404(TonKho, pk=pk)  # Lấy sản phẩm tồn kho theo ID.
        ton_kho.da_xoa = True  # Đánh dấu sản phẩm là đã xóa (thực tế không xóa khỏi cơ sở dữ liệu mà chỉ thay đổi trạng thái).
        ton_kho.save()  # Lưu lại thay đổi vào cơ sở dữ liệu.
        messages.success(request, self.success_message)  # Hiển thị thông báo thành công.
        return redirect(self.success_url)  # Chuyển hướng về danh sách sản phẩm tồn kho.


class DanhMucListView(FilterView):  # Lớp view để hiển thị danh sách danh mục sản phẩm với khả năng lọc.
    model = DanhMuc  # Mô hình DanhMuc được sử dụng để lấy danh mục sản phẩm.
    filterset_class = DanhMucFilter  # Bộ lọc áp dụng lên danh mục sản phẩm.
    queryset = DanhMuc.objects.filter(da_xoa=False)  # Lọc các danh mục chưa bị xóa.
    template_name = 'categories.html'  # Template hiển thị danh sách danh mục sản phẩm.
    context_object_name = 'danh_muc_list'  # Tên biến context chứa danh sách danh mục sản phẩm trong template.


class DanhMucCreateView(SuccessMessageMixin, CreateView):  # Lớp view để tạo mới một danh mục sản phẩm.
    model = DanhMuc  # Mô hình DanhMuc được sử dụng để tạo danh mục sản phẩm.
    form_class = DanhMucForm  # Form sử dụng để nhập dữ liệu cho danh mục sản phẩm.
    template_name = "edit_category.html"  # Template hiển thị form thêm danh mục.
    success_url = reverse_lazy('danhmuc')  # Sau khi tạo thành công, chuyển hướng về danh sách danh mục sản phẩm.
    success_message = "Danh mục mới đã được thêm thành công"  # Thông báo thành công khi tạo danh mục mới.


class DanhMucUpdateView(SuccessMessageMixin, UpdateView):  # Lớp view để cập nhật thông tin danh mục sản phẩm.
    model = DanhMuc  # Mô hình DanhMuc được sử dụng để cập nhật danh mục.
    form_class = DanhMucForm  # Form sử dụng để chỉnh sửa thông tin danh mục.
    template_name = "edit_category.html"  # Template hiển thị form chỉnh sửa danh mục.
    success_url = reverse_lazy('danhmuc')  # Sau khi cập nhật thành công, chuyển hướng về danh sách danh mục sản phẩm.
    success_message = "Danh mục đã được cập nhật thành công"  # Thông báo thành công khi cập nhật danh mục.


class DanhMucDeleteView(View):  # Lớp view để xóa (thực chất là đánh dấu đã xóa) một danh mục sản phẩm.
    template_name = "delete_category.html"  # Template hiển thị trang xác nhận xóa danh mục.
    success_message = "Danh mục đã được xóa thành công"  # Thông báo thành công khi xóa danh mục.
    success_url = reverse_lazy('danhmuc')  # Sau khi xóa thành công, chuyển hướng về danh sách danh mục sản phẩm.

    def get(self, request, pk):  # Xử lý yêu cầu GET (hiển thị trang xác nhận xóa).
        danh_muc = get_object_or_404(DanhMuc, pk=pk)  # Lấy danh mục theo ID, nếu không tìm thấy thì trả về lỗi 404.
        return render(request, self.template_name, {'object': danh_muc})  # Hiển thị trang xác nhận xóa.

    def post(self, request, pk):  # Xử lý yêu cầu POST (người dùng xác nhận xóa).
        danh_muc = get_object_or_404(DanhMuc, pk=pk)  # Lấy danh mục theo ID.
        danh_muc.da_xoa = True  # Đánh dấu danh mục là đã xóa (không xóa khỏi cơ sở dữ liệu).
        danh_muc.save()  # Lưu lại thay đổi vào cơ sở dữ liệu.
        messages.success(request, self.success_message)  # Hiển thị thông báo thành công.
        return redirect(self.success_url)  # Chuyển hướng về danh sách danh mục sản phẩm.


def danhmuc_chi_tiet(request, pk):  # Hàm view hiển thị chi tiết một danh mục sản phẩm.
    danh_muc = get_object_or_404(DanhMuc, pk=pk)  # Lấy danh mục theo ID, nếu không tìm thấy trả về lỗi 404.
    san_pham_list = danh_muc.ton_khos.filter(da_xoa=False)  # Lấy các sản phẩm thuộc danh mục này chưa bị xóa.
    return render(request, 'danhmuc_chi_tiet.html', {
        'danh_muc': danh_muc,  # Truyền danh mục vào template.
        'san_pham_list': san_pham_list,  # Truyền danh sách sản phẩm vào template.
    })

def hang_hoa_chi_tiet(request, pk):
    # Lấy thông tin hàng hóa
    hang_hoa = get_object_or_404(TonKho, pk=pk)
    tong_so_luong = SanPhamNhapKho.objects.filter(ton_kho=hang_hoa).aggregate(Sum('so_luong'))['so_luong__sum'] or 0
    # Lấy danh sách các lần nhập hàng liên quan
    danh_sach_nhap_hang = SanPhamNhapKho.objects.filter(ton_kho=hang_hoa).order_by('-phieu__thoi_gian')

    context = {
        'hang_hoa': hang_hoa,
        'tong_so_luong': tong_so_luong,
        'danh_sach_nhap_hang': danh_sach_nhap_hang,
    }
    return render(request, 'hang_hoa_chi_tiet.html', context)


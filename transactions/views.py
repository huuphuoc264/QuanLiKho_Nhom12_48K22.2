from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PhieuNhapKho,
    NhaCungCap,
    SanPhamNhapKho,
    PhieuBanHang,
    SanPhamBan,
)
from .forms import (
    ChonNhaCungCapForm,
    SanPhamNhapKhoFormset,
    NhaCungCapForm,
    PhieuBanHangForm,
    SanPhamBanFormset,
)
from inventory.models import TonKho
from django.urls import reverse_lazy

# Views liên quan đến Nhà cung cấp

# Hiển thị danh sách nhà cung cấp
class NhaCungCapListView(ListView):
    model = NhaCungCap  # Chỉ định mô hình NhaCungCap để lấy dữ liệu từ bảng này.
    template_name = "suppliers/suppliers_list.html"  # Đường dẫn đến template hiển thị danh sách nhà cung cấp.
    queryset = NhaCungCap.objects.filter(da_xoa=False)  # Lọc nhà cung cấp không bị xóa (da_xoa=False).
    paginate_by = 10  # Mỗi trang hiển thị 10 nhà cung cấp.
    context_object_name = 'danh-sach-nha-cung-cap'  # Đặt tên context là 'danh-sach-nha-cung-cap' để dễ sử dụng trong template.

# Thêm nhà cung cấp mới
class NhaCungCapCreateView(SuccessMessageMixin, CreateView):
    model = NhaCungCap  # Mô hình NhaCungCap được sử dụng để thêm mới.
    form_class = NhaCungCapForm  # Form để thêm hoặc chỉnh sửa nhà cung cấp.
    success_url = reverse_lazy('danh-sach-nha-cung-cap')  # Chuyển hướng đến danh sách nhà cung cấp sau khi thành công.
    success_message = "Nhà cung cấp đã được thêm thành công"  # Thông báo thành công khi thêm mới.
    template_name = "suppliers/edit_supplier.html"  # Template hiển thị form.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Lấy dữ liệu context mặc định từ lớp cha.
        context["title"] = 'Thêm Nhà Cung Cấp'  # Thêm tiêu đề cho trang.
        context["savebtn"] = 'Lưu'  # Thêm nhãn cho button lưu.
        return context

# Cập nhật thông tin nhà cung cấp
class NhaCungCapUpdateView(SuccessMessageMixin, UpdateView):
    model = NhaCungCap  # Mô hình NhaCungCap để cập nhật.
    form_class = NhaCungCapForm  # Form để chỉnh sửa thông tin nhà cung cấp.
    success_url = reverse_lazy('danh-sach-nha-cung-cap')  # Chuyển hướng đến danh sách nhà cung cấp sau khi cập nhật.
    success_message = "Chi tiết nhà cung cấp đã được cập nhật thành công"  # Thông báo thành công.
    template_name = "suppliers/edit_supplier.html"  # Template hiển thị form chỉnh sửa.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Lấy dữ liệu context mặc định.
        context["title"] = 'Chỉnh sửa Nhà Cung Cấp'  # Thêm tiêu đề cho trang.
        context["savebtn"] = 'Cập nhật'  # Thêm nhãn cho button cập nhật.
        context["delbtn"] = 'Xóa'  # Thêm nhãn cho button xóa.
        return context

# Xóa nhà cung cấp
class NhaCungCapDeleteView(View):
    template_name = "suppliers/delete_supplier.html"  # Template xác nhận xóa nhà cung cấp.
    success_message = "Nhà cung cấp đã được xóa thành công"  # Thông báo thành công khi xóa.

    def get(self, request, pk):
        nhacungcap = get_object_or_404(NhaCungCap, pk=pk)  # Lấy nhà cung cấp theo pk.
        return render(request, self.template_name, {'object': nhacungcap})  # Hiển thị trang xác nhận xóa.

    def post(self, request, pk):
        nhacungcap = get_object_or_404(NhaCungCap, pk=pk)  # Lấy nhà cung cấp theo pk.
        nhacungcap.da_xoa = True  # Đánh dấu nhà cung cấp là đã xóa.
        nhacungcap.save()  # Lưu lại thay đổi.
        messages.success(request, self.success_message)  # Thông báo thành công.
        return redirect('danh-sach-nha-cung-cap')  # Chuyển hướng về trang danh sách nhà cung cấp.

# Hiển thị chi tiết nhà cung cấp
class NhaCungCapChiTietView(View):
    def get(self, request, name):
        nhacungcap = get_object_or_404(NhaCungCap, ten=name)  # Lấy nhà cung cấp theo tên.
        danh_sach_phieu = PhieuNhapKho.objects.filter(nha_cung_cap=nhacungcap).order_by('-thoi_gian')  # Lấy các phiếu nhập kho liên quan đến nhà cung cấp.
        page = request.GET.get('page', 1)  # Lấy số trang từ GET request (mặc định là trang 1).
        paginator = Paginator(danh_sach_phieu, 10)  # Phân trang cho danh sách phiếu nhập kho.
        try:
            phieu_nhap = paginator.page(page)  # Lấy trang dữ liệu theo số trang.
        except PageNotAnInteger:
            phieu_nhap = paginator.page(1)  # Nếu số trang không hợp lệ, hiển thị trang 1.
        except EmptyPage:
            phieu_nhap = paginator.page(paginator.num_pages)  # Nếu trang yêu cầu vượt quá số trang, hiển thị trang cuối.
        context = {
            'nhacungcap': nhacungcap,  # Truyền nhà cung cấp vào context.
            'phieu_nhap': phieu_nhap  # Truyền danh sách phiếu nhập kho vào context.
        }
        return render(request, 'suppliers/supplier.html', context)  # Render template với context.

# Views liên quan đến Phiếu Nhập Kho

# Hiển thị danh sách phiếu nhập kho
class PhieuNhapKhoListView(ListView):
    model = PhieuNhapKho  # Mô hình Phiếu Nhập Kho.
    template_name = "purchases/purchases_list.html"  # Template hiển thị danh sách phiếu nhập kho.
    context_object_name = 'phieu_nhap_list'  # Tên context cho danh sách phiếu nhập kho.
    ordering = ['-thoi_gian']  # Sắp xếp theo thời gian giảm dần.
    paginate_by = 10  # Phân trang với 10 mục trên mỗi trang.

# Chọn nhà cung cấp để tạo phiếu nhập kho mới
class ChonNhaCungCapView(View):
    form_class = ChonNhaCungCapForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nhacungcap_id = request.POST.get("nha_cung_cap")
            nhacungcap = get_object_or_404(NhaCungCap, id=nhacungcap_id)
            return redirect('phieu-nhap-moi', nhacungcap.pk)
        return render(request, self.template_name, {'form': form})

# Tạo phiếu nhập kho mới và thêm sản phẩm
class PhieuNhapKhoCreateView(View):
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        # Khởi tạo formset rỗng để người dùng thêm sản phẩm nhập kho mới
        formset = SanPhamNhapKhoFormset(queryset=SanPhamNhapKho.objects.none())
        nhacungcap = get_object_or_404(NhaCungCap, pk=pk)
        context = {
            'formset': formset,
            'nhacungcap': nhacungcap,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        print(request.POST)
        # Lấy dữ liệu từ POST request
        formset = SanPhamNhapKhoFormset(request.POST)
        nhacungcap = get_object_or_404(NhaCungCap, pk=pk)

        # Kiểm tra xem formset có hợp lệ không
        if formset.is_valid():
            print("Formset hợp lệ.")
            # Tạo phiếu nhập kho mới với nhà cung cấp và người thực hiện là người dùng hiện tại
            phieu_nhap = PhieuNhapKho(nha_cung_cap=nhacungcap, user=request.user)
            phieu_nhap.save()

            # Lưu các sản phẩm trong phiếu nhập kho
            for form in formset:
                # Sử dụng `commit=False` để chưa lưu vào database cho tới khi hoàn tất xử lý
                sanpham_nhap = form.save(commit=False)

                # Kiểm tra nếu sản phẩm không bị bỏ trống
                if sanpham_nhap.ton_kho:
                    sanpham_nhap.phieu = phieu_nhap
                    sanpham_nhap.user = request.user  # Lưu người thực hiện thao tác

                    # Tính thành tiền cho sản phẩm nhập có xét đến chiết khấu
                    he_so_chiet_khau = (100 - sanpham_nhap.phan_tram_chiet_khau) / 100
                    sanpham_nhap.thanh_tien = sanpham_nhap.don_gia * sanpham_nhap.so_luong * he_so_chiet_khau

                    # Cập nhật số lượng tồn kho
                    tonkho = get_object_or_404(TonKho, pk=sanpham_nhap.ton_kho.pk)
                    tonkho.so_luong += sanpham_nhap.so_luong
                    tonkho.save()

                    # Lưu thông tin sản phẩm nhập vào phiếu nhập kho
                    sanpham_nhap.save()

            # Thông báo thành công và chuyển hướng đến trang chi tiết phiếu nhập kho
            messages.success(request, "Các mặt hàng đã được thêm vào phiếu nhập thành công")
            return redirect('phieu-nhap-xem', so_phieu=phieu_nhap.so_phieu)
        else:
            print("Formset không hợp lệ:")
            print(formset.errors)  # In lỗi của từng form trong formset
            print(formset.non_form_errors())  # In lỗi không thuộc form cụ thể
        # Nếu formset không hợp lệ, render lại form với các lỗi hiển thị
        context = {
            'formset': formset,
            'nhacungcap': nhacungcap,
        }
        return render(request, self.template_name, context)


# Xóa phiếu nhập kho
class PhieuNhapKhoDeleteView(SuccessMessageMixin, DeleteView):
    model = PhieuNhapKho
    template_name = "purchases/delete_purchase.html"
    success_url = reverse_lazy('phieu-nhap')

    def delete(self, *args, **kwargs):
        # Lấy phiếu nhập kho cần xóa
        self.object = self.get_object()
        # Lấy danh sách các sản phẩm liên quan đến phiếu nhập kho này
        sanpham_list = SanPhamNhapKho.objects.filter(phieu=self.object)
        for sanpham in sanpham_list:
            # Cập nhật số lượng tồn kho sau khi xóa sản phẩm
            tonkho = get_object_or_404(TonKho, ten=sanpham.ton_kho.ten)
            if not tonkho.da_xoa:  # Kiểm tra sản phẩm tồn kho chưa bị xóa
                tonkho.so_luong -= sanpham.so_luong  # Giảm số lượng tồn kho đi
                tonkho.save()  # Lưu lại thông tin tồn kho mới
        # Thông báo thành công khi phiếu nhập kho được xóa
        messages.success(self.request, "Phiếu nhập kho đã được xóa thành công")
        # Tiến hành xóa phiếu nhập kho
        return super().delete(*args, **kwargs)

# Views liên quan đến Phiếu Bán Hàng

# Hiển thị danh sách phiếu bán hàng
class PhieuBanHangListView(ListView):
    model = PhieuBanHang
    template_name = "sales/sales_list.html"
    context_object_name = 'phieu_ban_list'
    ordering = ['-thoi_gian']
    paginate_by = 10

# Tạo phiếu bán hàng mới và thêm sản phẩm
# Tạo phiếu bán hàng mới và thêm sản phẩm
class PhieuBanHangCreateView(View):
    template_name = 'sales/new_sale.html'

    def get(self, request):
        # Tạo form thông tin cho phiếu bán hàng và danh sách sản phẩm bán
        form = PhieuBanHangForm()
        formset = SanPhamBanFormset(queryset=SanPhamBan.objects.none())
        tonkho_list = TonKho.objects.filter(da_xoa=False)

        context = {
            'form': form,
            'formset': formset,
            'tonkho_list': tonkho_list
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Nhận thông tin từ người dùng
        form = PhieuBanHangForm(request.POST)
        formset = SanPhamBanFormset(request.POST)

        # Kiểm tra tính hợp lệ của form và formset
        if form.is_valid() and formset.is_valid():
            # Tạo phiếu bán hàng mới từ form và lưu thông tin người thực hiện
            phieu_ban = form.save(commit=False)
            phieu_ban.user = request.user  # Lưu người thực hiện thao tác
            phieu_ban.save()

            # Thiết lập formset liên kết với phiếu bán hàng vừa tạo
            formset.instance = phieu_ban

            # Duyệt qua từng sản phẩm trong formset
            for form in formset:
                # Sử dụng `commit=False` để chưa lưu vào database cho tới khi hoàn tất xử lý
                sanpham_ban = form.save(commit=False)

                # Kiểm tra nếu sản phẩm không bị bỏ trống
                if sanpham_ban.ton_kho:
                    sanpham_ban.phieu = phieu_ban
                    sanpham_ban.user = request.user  # Lưu người thực hiện thao tác

                    # Lấy thông tin sản phẩm từ tồn kho
                    tonkho = get_object_or_404(TonKho, pk=sanpham_ban.ton_kho.pk)

                    # Kiểm tra số lượng có đủ để bán không
                    if tonkho.so_luong >= sanpham_ban.so_luong:
                        # Trừ số lượng sản phẩm trong kho
                        tonkho.so_luong -= sanpham_ban.so_luong
                        tonkho.save()

                        # Tính thành tiền cho sản phẩm bán có xét đến chiết khấu
                        chiet_khau = sanpham_ban.phan_tram_chiet_khau / 100
                        sanpham_ban.thanh_tien = sanpham_ban.don_gia * sanpham_ban.so_luong * (1 - chiet_khau)

                        # Lưu thông tin sản phẩm bán vào phiếu bán hàng
                        sanpham_ban.save()
                    else:
                        # Nếu không đủ số lượng trong kho, thêm lỗi vào formset và quay lại trang
                        form.add_error(
                            'so_luong',
                            f"Không đủ sản phẩm '{sanpham_ban.ton_kho.ten}' trong kho để bán."
                        )
                        return render(request, self.template_name, {
                            'form': form,
                            'formset': formset,
                            'tonkho_list': TonKho.objects.filter(da_xoa=False)
                        })

            # Thông báo thành công khi tạo phiếu bán hàng
            messages.success(request, "Phiếu bán hàng đã được tạo thành công")
            return redirect('phieu-ban-xem', so_phieu=phieu_ban.so_phieu)

        # Nếu form không hợp lệ, quay lại trang và hiển thị thông báo lỗi
        else:
            return render(request, self.template_name, {
                'form': form,
                'formset': formset,
                'tonkho_list': TonKho.objects.filter(da_xoa=False)
            })

class PhieuBanHangDeleteView(SuccessMessageMixin, DeleteView):
    model = PhieuBanHang
    template_name = "sales/delete_sale.html"
    success_url = reverse_lazy('phieu-ban')

    def delete(self, *args, **kwargs):
        # Lấy phiếu bán hàng cần xóa
        self.object = self.get_object()
        # Lấy danh sách sản phẩm thuộc phiếu bán hàng này
        sanpham_list = SanPhamBan.objects.filter(phieu=self.object)
        for sanpham in sanpham_list:
            # Cập nhật tồn kho sau khi xóa sản phẩm trong phiếu bán hàng
            tonkho = get_object_or_404(TonKho, pk=sanpham.ton_kho.pk)
            if not tonkho.da_xoa:  # Kiểm tra sản phẩm tồn kho chưa bị xóa
                tonkho.so_luong += sanpham.so_luong  # Cộng lại số lượng tồn kho
                tonkho.save()

        # Thông báo thành công khi phiếu bán hàng bị xóa
        messages.success(self.request, "Phiếu bán hàng đã được xóa thành công")
        # Tiến hành xóa phiếu bán hàng
        return super().delete(*args, **kwargs)

# Views để hiển thị chi tiết các phiếu nhập kho và phiếu bán hàng
class PhieuNhapKhoView(View):
    model = PhieuNhapKho
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, so_phieu):
        context = {
            'phieu': get_object_or_404(PhieuNhapKho, so_phieu=so_phieu),
            'sanpham_list': SanPhamNhapKho.objects.filter(phieu=so_phieu),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

class PhieuBanHangView(View):
    model = PhieuBanHang
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, so_phieu):
        phieu_ban = get_object_or_404(PhieuBanHang, so_phieu=so_phieu)
        sanpham_list = SanPhamBan.objects.filter(phieu=phieu_ban)
        context = {
            'phieu': phieu_ban,
            'sanpham_list': sanpham_list,
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)


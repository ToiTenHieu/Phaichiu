from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .models import Book
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        occupation = request.POST.get("occupation")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Mật khẩu nhập lại không khớp!")
            return redirect("/accounts/register/")

        # Kiểm tra username đã tồn tại
        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
            return redirect("/accounts/register/")
        # Tạo User
        user = User.objects.create_user(username=username, email=email, password=password)
        # Tạo UserProfile với tất cả các trường
        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            gender=gender ,
            date_of_birth=date_of_birth or None,
            address=address
        )

        messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
        return redirect("/accounts/login/")

    else:
        # GET → render template form đăng ký
        return render(request, "accounts/register.html")



from .models import UserProfile, Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User

@login_required
def librarian_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role != 'librarian':
        return redirect('home')

    # 👉 Nếu nhấn nút Thêm Người Dùng
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        name = request.POST.get("name")
        occupation = request.POST.get("occupation")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")

        # 1. Tạo User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # 2. Tạo UserProfile
        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            role='user'
        )

        return redirect(reverse("librarian_dashboard") + "?section=quanLyNguoiDung")
    
    # 👉 Nếu GET: load tất cả dữ liệu
    users_only = UserProfile.objects.filter(role='user')
    books = Book.objects.all()
    categories = Book.objects.values_list('category', flat=True).distinct()

    librarian_name = profile.name or profile.user.username

    context = {
        'users': users_only,
        'books': books,
        'categories': categories,
        'librarian_name': librarian_name,
        'profile': profile,
    }

    return render(request, 'accounts/librarian_dashboard.html', context)

from django.contrib.auth.models import Group

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # 🔑 Kiểm tra role trong UserProfile
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'librarian':
                return redirect("librarian_dashboard")   # giao diện thủ thư
            elif user.is_superuser:
                return redirect("/admin/")               # admin
            else:
                return redirect("home")                  # người dùng thường
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "accounts/home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, UserProfileForm

@login_required
def profile_view(request):
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect("profile_view")
        else:
            messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại.")
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


# views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        # Truyền user trước, data=POST sau
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # giữ session login
            messages.success(request, 'Password changed successfully!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

from .models import UserProfile


def danh_sach_nguoi_dung(request):
    users = UserProfile.objects.select_related('user').all()  # lấy tất cả UserProfile kèm User
    return render(request, 'users_list.html', {'users': users})


def catalog(request):
    return render(request, "accounts/catalog.html")  # tạo template catalog.html
def services(request):
    return render(request, "accounts/services.html")  # tạo template services.html
def contact(request):
    return render(request, "accounts/contact.html")  # tạo template contact.html
from django.shortcuts import get_object_or_404, render, redirect
from .models import UserProfile  # model chứa phone, address, gender,...

def edit_user(request, user_id):
    profile = get_object_or_404(UserProfile, pk=user_id)
    if request.method == "POST":
        profile.name = request.POST.get('name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.date_of_birth = request.POST.get('date_of_birth')
        profile.gender = request.POST.get('gender')
        profile.save()
        return redirect(reverse("librarian_dashboard") + "?section=quanLyNguoiDung")
    return render(request, 'accounts/edit_user.html', {'user': profile})
@csrf_exempt  # hoặc dùng csrf token header trong fetch
def delete_user_api(request, user_id):
    if request.method == "DELETE":
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        user_profile.delete()
        return JsonResponse({"message": "Người dùng đã được xóa thành công."})
    
    return JsonResponse({"error": "Phương thức không hợp lệ."}, status=400)
from django.template.defaultfilters import slugify

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book

@csrf_exempt
def add_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        author = data.get("author")
        category = data.get("category")
        quantity = data.get("quantity")
        publish_year = data.get("publishYear")
        description = data.get("description")

        # Lưu vào DB
        book = Book.objects.create(
            title=name,
            author=author,
            category=category,
            quantity=quantity,
            year=publish_year,
            description=description
        )

        return JsonResponse({"message": "Thêm sách thành công", "id": book.book_id}, status=201)
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book

@csrf_exempt
def update_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "GET":
        # Trả về dữ liệu sách để load vào form
        return JsonResponse({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "quantity": book.quantity,
            "description": book.description,
            "status": book.status,
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            book.title = data.get("title", book.title)
            book.author = data.get("author", book.author)
            book.year = data.get("year", book.year)
            book.category = data.get("category", book.category)
            book.quantity = data.get("quantity", book.quantity)
            book.description = data.get("description", book.description)
            book.status = data.get("status", book.status)
            book.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Book
import json

# accounts/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Book
import json

# GET all books
def book_list(request):
    if request.method == "GET":
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

# GET or PUT a single book
@csrf_exempt
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "GET":
        return JsonResponse({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "quantity": book.quantity,
            "status": book.status,
            "description": book.description,
        })

    elif request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.year = data.get("year", book.year)
        book.category = data.get("category", book.category)
        book.quantity = data.get("quantity", book.quantity)
        book.status = data.get("status", book.status)
        book.description = data.get("description", book.description)
        book.save()

        return JsonResponse({"message": "Book updated successfully"})

    elif request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Book deleted successfully"}, status=200)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


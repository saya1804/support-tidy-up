from django.shortcuts import render, redirect
from django.views import View
from app.forms import SignupForm, LoginForm, UserUpdateForm, PasswordUpdateForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Category, SubCategory
from .forms import CategoryForm, SubCategoryForm

# Create your views here.


class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")
    

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", context={
            "form":form
        })
    def post(self, request):
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", context={
            "form":form
        })
    

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home")
        return render(request, "login.html", context={
            "form":form
        })


class HomeView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "home.html")


class UserUpdateView(View):
    def get(self, request):
        return render(request, "user_update.html")
    def post(self, request):
        print(request.POST)
        form = UserUpdateForm(request.POST)
        form = UserUpdateForm(instance=request.user)
        if form.is_valid():
            form. save()
            messages.success(request, "アカウント情報が更新されました。")
            return redirect("home")
        return render(request, "user_update.html", context={
            "form":form,
        })

class PasswordUpdateView(View):
    def get(self, request):
        return render(request, "password_update.html")
    def post(self, request):
        print(request.POST)
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            new_password = form.cleaned_data.get("new_password")

            user = request.user
            if not user.check_password(old_password):
                form.add_error("old_password", "現在のパスワードが間違っています。")
                return render(request, "password_update.html", context={
                    "form":form
                })
            
            user.set_password(new_password)
            user.save
            update_session_auth_hash(request, user)
            messages.success(request, "パスワードが変更されました。")
            return redirect("home")
        return render(request, "password_update.html", context={
            "form":form
        })

class UndecidedBoxView(View):
    def get(self, request):
        return render(request, "undecided_box.html")

class BelongingsManagementView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_form = CategoryForm()
        subcategory_form = SubCategoryForm()

        return render(request, "belongings_management.html",  context={
            "categories": categories,
            "category_form": category_form,
            "subcategory_form": subcategory_form,
        })
    def post(self, request):
        categories = Category.objects.all()
        category_form = CategoryForm(request.POST)
        subcategory_form = SubCategoryForm(request.POST)
        if "add_category" in request.POST:
            if category_form.is_valid():
                category_form.save()
                return redirect("belongings_management")
        elif "add_subcategory" in request.POST:
            if subcategory_form.is_valid():
                category_id = request.POST.get('category_id')
                print(f"Category ID: {request.POST.get('category_id')}")
                if category_id:
                    category = Category.objects.get(id=category_id)
                    subcategory = subcategory_form.save(commit=False)
                    subcategory.category = category  
                    subcategory.save()
                    return redirect("belongings_management")
                else:
                    print("No category_id provided!") 
        return render(request, "belongings_management.html",  context={
            "categories": categories,
            "category_form": category_form,
            "subcategory_form": subcategory_form,
        })
    
class DeclutteringSettingView(View):
    def get(self, request):
        return render(request, "decluttering_setting.html")
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm, UserUpdateForm, PasswordUpdateForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Belonging, Category, SubCategory
from .forms import CategoryForm, SubCategoryForm, BelongingForm
from django.http import JsonResponse
from django.urls import reverse

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


class UserUpdateView(LoginRequiredMixin, View):
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

class PasswordUpdateView(LoginRequiredMixin, View):
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

class UndecidedBoxView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "undecided_box.html")

class BelongingsManagementView(LoginRequiredMixin, View):
    def get(self, request):
        belongings = Belonging.objects.filter(is_deleted=False)
        for belonging in belongings:
            stars = []
            favorite_level = belonging.favorite_level
            for i in range(1, 6):
                if i <= favorite_level:
                    stars.append("★")
                else:
                    stars.append("☆")
                belonging.stars = "".join(stars)
        decluttering_items = Belonging.objects.filter(is_in_decluttering=True)
        categories = Category.objects.filter(is_deleted=False)
        subcategories = SubCategory.objects.filter(is_deleted=False)
        category_form = CategoryForm()
        subcategory_form = SubCategoryForm()
        selected_subcategory = None
        if 'subcategory_id' in request.GET:
            selected_subcategory = SubCategory.objects.get(id=request.GET['subcategory_id'])

        subcategory_links = []
        for subcategory in subcategories:
            subcategory_links.append({
                'id': subcategory.id,
                'name': subcategory.name,
                'url': reverse('add_belonging', kwargs={'subcategory_id': subcategory.id})
            })

        return render(request, "belongings_management.html", context={
            "belongings": belongings,
            "decluttering_items": decluttering_items,
            "categories": categories,
            "subcategories": subcategories,
            "category_form": category_form,
            "subcategory_form": subcategory_form,
            "selected_subcategory": selected_subcategory,
            "subcategory_links": subcategory_links,
        })

    def post(self, request):
        belongings = Belonging.objects.filter(is_deleted=False)
        categories = Category.objects.filter(is_deleted=False)
        category_form = CategoryForm(request.POST)
        subcategory_form = SubCategoryForm(request.POST)

        if "add_category" in request.POST:
            if category_form.is_valid():
                category_form.save()
                return redirect("belongings_management")
            
        elif "add_subcategory" in request.POST:
            if subcategory_form.is_valid():
                subcategory = subcategory_form.save(commit=False)
                category_id = request.POST.get('category_id')
                subcategory.category = Category.objects.get(id=category_id)
                subcategory.save()
                return redirect("belongings_management")

        elif "edit_category" in request.POST:
            category_id = request.POST.get('id')
            category_name = request.POST.get('name')
            category = Category.objects.get(id=category_id)
            category.name = category_name
            category.save()
            return redirect("belongings_management")

        elif "edit_subcategory" in request.POST:
            subcategory_id = request.POST.get('subcategory_id')
            subcategory_name = request.POST.get('subcategory_name')
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.name = subcategory_name
            subcategory.save()
            return redirect("belongings_management")

        elif "delete_category" in request.POST:
            category_id = request.POST.get('delete_category')
            category = Category.objects.get(id=category_id)
            category.is_deleted = True
            category.save()
            return redirect("belongings_management")

        elif "delete_subcategory" in request.POST:
            subcategory_id = request.POST.get('delete_subcategory')
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.is_deleted = True
            subcategory.save()
            return redirect("belongings_management")

        return render(request, "belongings_management.html", context={
            "belongings": belongings,
            "categories": categories,
            "category_form": category_form,
            "subcategory_form": subcategory_form,
        })

    def get_belongings_for_subcategory(request, subcategory_id):
        subcategory =SubCategory.objects.get(id=subcategory_id)
        belongings = Belonging.objects.filter(subcategory=subcategory, is_deleted=False)
        belonging_data = []
        for belonging in belongings:
            belonging_data.append({
                'name': belonging.name,
                'image_url': belonging.image.url
            })
        return JsonResponse({'belongings': belonging_data})
    
class MoveToDeclutteringListView(View):
    def post(self, request, belonging_id):
        belonging = get_object_or_404(Belonging, id=belonging_id)
        belonging.is_in_decluttering = True
        belonging.save()
        return redirect("belongings_management")
    
class DeleteBelongingView(View):
    def post(self, request, belonging_id):
        belonging = get_object_or_404(Belonging, id=belonging_id)
        belonging.is_deleted = True
        belonging.save()
        return redirect("belongings_management")
    
class AddBelongingView(LoginRequiredMixin, View):
    def get(self, request, subcategory_id):
        subcategory = SubCategory.objects.get(id=subcategory_id)
        form = BelongingForm()
        return render(request, "add_belonging.html", {
            'form': form,
            'subcategory': subcategory,
        })
    def post(self, request):
        form = BelongingForm(request.POST, request.FILES)
        if form. is_valid():
            form.save()
            return redirect("belongings_management")
        return render(request,"add_belonging.html", {'form': form})

class EditBelongingView(LoginRequiredMixin, View):
    def get(self, request, belonging_id):
        belonging = get_object_or_404(Belonging, id=belonging_id)
        form = BelongingForm(instance=belonging)
        return render(request, "edit_belonging.html", {'form': form, 'belonging': belonging})
    def post(self, request, belonging_id):
        belonging = get_object_or_404(Belonging, id=belonging_id)
        form = BelongingForm(request.POST, instance=belonging)
        if form.is_valid():
            form.save()
            return redirect("belongings_management")
        return render(request, "edit_belonging.html", {'form': form, 'belonging': belonging})
     
class DeclutteringSettingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "decluttering_setting.html")
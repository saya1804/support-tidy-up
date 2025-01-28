from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate
from .models import Category, SubCategory

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        print(email, password)
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            self.add_error(None, "認証に失敗しました。メールアドレスまたはパスワードが間違っています。")

            if '__all__' in self.errors:
                del self.errors['__all__']

            raise forms.ValidationError("認証に失敗しました。メールアドレスまたはパスワードが間違っています")

        return cleaned_data
    
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["username", "email"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            return user
        
class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    confirm_password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("新規パスワードと確認用パスワードが一致しません。")
        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            if instance and instance.category:
                self.fields['category'].initial = instance.category.id
                self.fields['category'].widget.attrs['readonly'] = True
                self.fields['category'].required = False

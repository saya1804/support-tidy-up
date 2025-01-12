"""
URL configuration for support_tidy_up project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import PortfolioView, SignupView, LoginView, HomeView, UserUpdateView, PasswordUpdateView, UndecidedBoxView, BelongingsManagementView, DeclutteringSettingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PortfolioView.as_view(), name="portfolio"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('home/', HomeView.as_view(), name="home"),
    path('uesr_update/', UserUpdateView.as_view(), name="user_update"),
    path('password_update/', PasswordUpdateView.as_view(), name="password_update"),
    path('undecided_box/', UndecidedBoxView.as_view(), name="undecided_box"),
    path('belongings_management/', BelongingsManagementView.as_view(), name="belongings_management"),
    path('decluttering_setting/', DeclutteringSettingView.as_view(), name="decluttering_setting"),
]

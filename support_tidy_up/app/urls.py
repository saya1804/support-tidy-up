from django.urls import path
from . views import PortfolioView, SignupView, LoginView, HomeView, UserUpdateView, PasswordUpdateView, UndecidedBoxView, BelongingsManagementView, DeclutteringSettingView

urlpatterns = [
    path('', PortfolioView.as_view(), name="portfolio"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('home/', HomeView.as_view(), name="home"),
    path('uesr_update/', UserUpdateView.as_view(), name="user_update"),
    path('password_update/', PasswordUpdateView.as_view(), name="password_update"),
    path('undecided_box/', UndecidedBoxView.as_view(), name="undecided_box"),
    path('BelongingsManagement/', BelongingsManagementView.as_view(), name="belongings_management"),
    path('decluttering_setting/', DeclutteringSettingView.as_view(), name="decluttering_setting"),
]
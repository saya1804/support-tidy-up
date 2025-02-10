from django.urls import path
from . views import PortfolioView, SignupView, LoginView, HomeView, UserUpdateView, PasswordUpdateView, UndecidedBoxView, BelongingsManagementView, DeclutteringSettingView, GetBelongingsForSubcategoryView, AddBelongingView, EditBelongingView, MoveToDeclutteringListView, DeleteBelongingView

urlpatterns = [
    path('', PortfolioView.as_view(), name="portfolio"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('home/', HomeView.as_view(), name="home"),
    path('uesr_update/', UserUpdateView.as_view(), name="user_update"),
    path('password_update/', PasswordUpdateView.as_view(), name="password_update"),
    path('undecided_box/', UndecidedBoxView.as_view(), name="undecided_box"),
    path('belongings_management/', BelongingsManagementView.as_view(), name="belongings_management"),
    path('decluttering_setting/', DeclutteringSettingView.as_view(), name="decluttering_setting"),
    path('get_belongings_for_subcategory/<int:subcategory_id>/', GetBelongingsForSubcategoryView.as_view(), name="get_belongings_for_subcategory"),
    path('add_belonging/<int:subcategory_id>/', AddBelongingView.as_view(), name="add_belonging"),
    path('edit_belonging/<int:belonging_id>/', EditBelongingView.as_view(), name="edit_belonging"),
    path('move_to_decluttering_list/<int:belonging_id>/', MoveToDeclutteringListView.as_view(), name="move_to_decluttering_list"),
    path('delete_belonging/<int:belonging_id>/', DeleteBelongingView.as_view(), name="delete_belonging"),
]
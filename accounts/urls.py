from importlib import import_module

from allauth.socialaccount import providers
from allauth.socialaccount import views as allauth_views
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

from . import views, forms

urlpatterns = [
    # Authentication
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Personal cabinet
    path('personal-cabinet/', views.PersonalCabinetView.as_view(), name='personal_cabinet'),
    path('<str:slug>/personal-info/', views.PersonalInfoUpdateView.as_view(), name='personal_info'),
    path('<str:slug>/personal-safety/', views.PersonalSafetyView.as_view(), name='personal_safety'),
    path('addresses/', views.AddressesListView.as_view(), name='addresses_list'),
    path('addresses/add/', views.AddAddressView.as_view(), name='add_address'),
    path('addresses/edit/<int:pk>/', views.EditAddressView.as_view(), name='edit_address'),
    path('addresses/delete/<int:pk>/', views.delete_address, name="delete_address"),
    path('addresses/set-default/<int:pk>/', views.set_default_address, name='set_default'),
    path('avatar/change/', views.user_avatar_change, name='avatar_change'),
    path('avatar/delete/', views.user_avatar_delete, name='avatar_delete'),
    path('<str:slug>/delete/', views.AccountDeleteView.as_view(), name='delete_account'),

    # Password change
    path('password/change/',
         PasswordChangeView.as_view(template_name='accounts/password_change/password_change_form.html',
                                    form_class=forms.CustomPasswordChangeForm), name='password_change'),
    path('password/change/done/',
         PasswordChangeDoneView.as_view(template_name='accounts/password_change/password_change_done.html'),
         name='password_change_done'),

    # Password reset
    path('password/reset/', PasswordResetView.as_view(template_name='accounts/password_reset/password_reset_form.html',
                                                      subject_template_name='accounts/password_reset/password_reset_subject.txt',
                                                      email_template_name='accounts/password_reset/password_reset_email.html'),
         name='password_reset'),
    path('password/reset/done',
         PasswordResetDoneView.as_view(template_name='accounts/password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('password/reset/confirm/<str:uidb64>/<str:token>',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset/password_reset_confirm.html',
                                          form_class=forms.CustomSetPasswordForm), name='password_reset_confirm'),
    path('password/reset/complete',
         PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),

    # Django-allauth
    path('social/signup/', allauth_views.signup, name='socialaccount_signup'),
]

# Provider urlpatterns, as separate attribute (from django-allauth).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns

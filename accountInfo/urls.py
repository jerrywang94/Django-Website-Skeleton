from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import user_passes_test

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), 'dashboard')

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    #   Uses the login_forbidden to either redirect user to dashboard if
    #   already logged in or proceed to login page.
    url(r'^login/$', login_forbidden(auth_views.login), {'template_name': 'accountInfo/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^user/password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect' : '/user/password/reset/done/'}, name="password_reset"),
    url(r'^user/password/reset/done/$',
        auth_views.password_reset_done, name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect' : '/user/password/done/'}, name="password_reset_confirm"),
    url(r'^user/password/done/$',
        auth_views.password_reset_complete),
    url(r'^password_change/$', views.pass_change, name='pass_change'),
]

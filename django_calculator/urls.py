"""django_calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from accounts.views import LogInView, SignUpView, Home

urlpatterns=[
    path('', LogInView.as_view(), name='login'),
    path('login/', LogInView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('home/', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

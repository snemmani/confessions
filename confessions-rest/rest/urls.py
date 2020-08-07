"""confessions_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('confession/', views.ConfessionListView.as_view(), name='confessions_cl'),
    path('confession/<int:confession_id>', views.ConfessionDetailView.as_view(), name='confessions_rud'),
    path('confession/<int:confession_id>/comment', views.CommentListView.as_view(), name='comment_cl'),
    path('comment/<int:comment_id>', views.CommentDetailView.as_view(), name='comment_rud')
]

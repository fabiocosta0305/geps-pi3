"""projetointegrador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from geps.views import home, cadUser, insertUser, loginUser, validLoginUser, dashboard, logouts, changePassword, validChangePassword, policy, cadInstituicao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('cadUser/', cadUser),
    path('cadInstituicao/', cadInstituicao),
    path('insertUser/', insertUser),
    path('loginUser/', loginUser),
    path('validLoginUser/', validLoginUser),
    path('dashboard/', dashboard),
    path('logouts/', logouts),
    path('changePassword/', changePassword),
    path('validChangePassword/', validChangePassword),
    path('policy/', policy),
]

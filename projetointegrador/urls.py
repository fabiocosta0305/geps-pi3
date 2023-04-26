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
from django.contrib.auth import views as auth_views

from geps.utils.funcoes import enviandoEmail

from geps.views import home, cadUser, insertUser, loginUser, validLoginUser, \
    dashboard, logouts, changePassword, validChangePassword, policy, cadInstituicao, \
    insertInst, formPesquisaDocente, pesquisaDocente, buscaDocente, gravaStatusDocente, \
    formDispDocente, gravaBairrosDocente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('cadUser/', cadUser),
    path('cadInstituicao/', cadInstituicao),
    path('insertUser/', insertUser),
    path('insertInst/', insertInst),
    path('loginUser/', loginUser),
    path('validLoginUser/', validLoginUser),
    path('dashboard/', dashboard),
    path('logouts/', logouts),
    path('changePassword/', changePassword),
    path('validChangePassword/', validChangePassword),
    path('policy/', policy),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_complete'),
    path('formPesquisaDocente/', formPesquisaDocente),
    path('pesquisaDocente/', pesquisaDocente),
    path('buscaDocente', buscaDocente, name='buscaDocente'),
    path('gravaStatusDocente/', gravaStatusDocente),
    path('formDispDocente/', formDispDocente),
    path('gravaBairrosDocente/', gravaBairrosDocente),
    path('enviandoEmail/', enviandoEmail, name='enviandoEmail'),
]

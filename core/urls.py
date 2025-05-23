from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def documentacao_view(request):
    return HttpResponse("<h1>Bem-vindo à página de Documentação</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.home.urls')),  # Inclui URLs do app home na raiz
    path('avisos/', include('core.avisos.urls')),
    path('user/', include('core.user.urls')),
    # Removida a linha duplicada: path('user/', include('core.home.urls')),
    path('documentacao/', documentacao_view),  # Adiciona a rota para documentacao
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

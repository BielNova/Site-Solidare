from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # Import necessário para criar uma resposta simples

def documentacao_view(request):
    return HttpResponse("<h1>Bem-vindo à página de Documentação</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.home.urls')),  # Inclui URLs do app home na raiz
    path('avisos/', include('core.avisos.urls')),
    path('user/', include('core.user.urls')),
    path('frequencia/', include('core.frequencia.urls', namespace='frequencia')),
    path('documentacao/', include('core.documentacao.urls', namespace='documentacao')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

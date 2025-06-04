from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # Import necessário para criar uma resposta simples


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.home.urls')),  # Inclui URLs do app home na raiz
    path('avisos/', include('core.avisos.urls')),
    path('user/', include(('core.user.urls', 'user'))),
    # path('frequencia/', include('core.frequencia.urls', namespace='frequencia')),
    # path('documentacao/', include('core.documentacao.urls', namespace='documentacao')),
    path('professor/', include('core.professor.urls', namespace='professor')),
    path('processo_seletivo/', include('processo_seletivo.urls')),
    path('aluno/', include('core.aluno.urls', namespace='aluno')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('avisos/', include('core.avisos.urls')),  # Modifique aqui para incluir o caminho correto
]

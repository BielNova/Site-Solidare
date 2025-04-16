from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('avisos/', include('avisos.urls')),  # <-- Adiciona essa linha
]

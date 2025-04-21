from django.contrib import admin
from django.urls import path, include 
 # <-- IMPORTANTE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.home.urls')),  # Inclui URLs do app home na raiz]
    path('avisos/', include('core.avisos.urls')),  # Modifique aqui para incluir o caminho correto
    path('user/', include('core.user.urls')),
    path('user/', include('core.home.urls')),  # Modifique aqui para incluir o caminho correto

 ]
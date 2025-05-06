from django.urls import path
from .views import AvisoListView, AvisoDetailView, AvisoCreateView

app_name = 'avisos'


urlpatterns = [
    path('', AvisoListView.as_view(), name='aviso_list'),
    path('novo/', AvisoCreateView.as_view(), name='aviso_create'),
    path('<int:pk>/', AvisoDetailView.as_view(), name='aviso_detail'),
]

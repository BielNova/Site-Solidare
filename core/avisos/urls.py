from django.urls import path
from .views import AvisoListView, AvisoDetailView, AvisoCreateView

urlpatterns = [
    path('', AvisoListView.as_view(), name='aviso-lista'),
    path('<int:pk>/', AvisoDetailView.as_view(), name='aviso-detalhe'),
    path('novo/', AvisoCreateView.as_view(), name='aviso-novo'),
]

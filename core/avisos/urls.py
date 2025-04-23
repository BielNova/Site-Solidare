from django.urls import path
from .views import AvisoListView, AvisoDetailView, AvisoCreateView

urlpatterns = [
    path('', AvisoListView.as_view(), name='aviso-list'),
    path('<int:pk>/', AvisoDetailView.as_view(), name='aviso-detail'),
    path('novo/', AvisoCreateView.as_view(), name='aviso-create'),
]

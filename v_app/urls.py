from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.new_search, name='new_search')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



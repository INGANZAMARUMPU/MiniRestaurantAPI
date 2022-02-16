from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from . import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('resto.urls')),
    re_path("^(?!media)(?!admin)(?!api)(?!static).*$", views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
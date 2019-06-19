from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include

from django.views.generic.base import TemplateView


urlpatterns = [
    path('api/questions/', include('questions.urls')),
    path('api/users/', include('users.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path('(.*)', TemplateView.as_view(template_name='base.html'), name="base"),
]
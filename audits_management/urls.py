
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('audits/', include('audits.urls', namespace='audits')),
    path('', include('users.urls')),
]

admin.site.index_title = "Site Audits Management"
admin.site.site_header = "Audits Management Admin"
admin.site.site_title ="Audits"


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

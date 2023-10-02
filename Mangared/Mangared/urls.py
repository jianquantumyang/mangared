from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('',include('frontend.urls'))
]
#admin.site.site_header = "Manga red Администрация"
#admin.site.index_title = "Manga red"


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


urlpatterns += staticfiles_urlpatterns()



admin.site.index_title = "manga.red"

admin.site.site_header = "manga.red Admin"
admin.site.site_title = "manga.red Admin Portal"
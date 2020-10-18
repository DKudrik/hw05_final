from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500


urlpatterns = [
    path("admin/", admin.site.urls),
    path("about-us/", views.flatpage, {"url": "/about-us/"}, name="about"),
    path("about-author/", views.flatpage, name="author"),
    path("about-spec/", views.flatpage, name="spec"),
    path("about/", include("django.contrib.flatpages.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("terms/", views.flatpage, {"url": "/terms/"}, name="terms"),
    path("", include("posts.urls")),
]

handler404 = "posts.views.page_not_found"  #noqa
handler500 = "posts.views.server_error"  #noqa

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
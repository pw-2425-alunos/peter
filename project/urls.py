from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views

from ninja import NinjaAPI
from dnd.api import router as dnd_router

api = NinjaAPI()

api.add_router("/dnd/", dnd_router)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("portfolio.urls")),
    path("accounts/", include("accounts.urls")),
    path("artigos/", include("artigos.urls")),
    path("export-db/", views.export_database, name="export_db"),
    path("accounts/", include("allauth.urls")),

    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
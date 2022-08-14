
from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('jet/', include("jet.urls",namespace='jet')),
    # path('jet/dashboard/', include("jet.dashboard.urls",namespace='jet-dashboard')),


    path("",include("pages.urls",namespace="pages")),
    path("accounts/",include("accounts.urls",namespace="accounts")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



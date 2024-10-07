
from django.contrib import admin
from django.urls import path , include 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('UserLogin.urls')),
    path('CadCasa/',include('Casa.urls')),
    path('MainPage/',include('HomePage.urls')),
    path('Pagamento/',include('pagamento.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
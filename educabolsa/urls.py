from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('appbolsa/', include('appbolsa.urls')),
                  path('', RedirectView.as_view(url='appbolsa/', permanent=True)),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('social-auth/', include('social_django.urls', namespace='social')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

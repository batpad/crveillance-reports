"""coast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from road.views import home, places, place, month, day, video, reports, report, add_report
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('places/', places),
    path('place/<slug:slug>', place),
    path('place/<slug:place_slug>/<int:year>/<int:month>', month),
    path('place/<slug:place_slug>/<int:year>/<int:month>/<int:day>', day),
    path('video/<int:id>', video),
    path('reports/', reports),
    path('report/<str:typ>/<int:id>', report),
    path('add_report', add_report)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

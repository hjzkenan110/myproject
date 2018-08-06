from query import views as query  # new
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('timelion', query.query_timelion),
    path('admin/', admin.site.urls),
]

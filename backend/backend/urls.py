from query import views as query  # new
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('timelion', query.query_timelion),
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='ajax.html')),
    path('', TemplateView.as_view(template_name='index.html')),

]

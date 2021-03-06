from query import views as query  # new
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('increase-timelion', query.increase_timelion),
    path('tpostnum-rank', query.tpostnum_rank),
    # path('series_timelion', query.increase_timelion),
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='ajax.html')),
    path('', TemplateView.as_view(template_name='new.html')),
    path('series-timelion', query.series_timelion),
    # path('/index', TemplateView.as_view(template_name='new.html'))
]

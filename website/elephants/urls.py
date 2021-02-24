from django.urls import path

from . import views

#be sure to give every path a name variable so when we create links in the html templates we can reference these urls
app_name = 'elephants'
urlpatterns = [
    path('', views.index, name='index'),
    path('feeders', views.feeders, name='feeders'),
    path('scheduling', views.scheduling, name='scheduling'),
    path('presetscheduling', views.preset_scheduling, name='presetscheduling'),
    path('preset-manager', views.default_presets_manager, name='preset_manager'),
    path('markpreset', views.markpreset, name='markpreset'),
    path('custom', views.custom, name='custom'),
    path('presets', views.presets, name='presets'),
    path('schedule', views.schedule, name='schedule'),
]
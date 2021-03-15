from django.urls import path

from . import views

#be sure to give every path a name variable so when we create links in the html templates we can reference these urls
app_name = 'elephants'
urlpatterns = [
    path('', views.index, name='index'),
    path('feeders', views.feeders, name='feeders'),
    path('presetscheduling', views.preset_scheduling, name='presetscheduling'),
    path('custom', views.custom, name='custom'),
    path('presets', views.presets, name='presets'),
    path('schedule/', views.schedule, name='schedule'),
    path('editpreset', views.edit_preset_page, name='editpresetpage'),
    path('deletepresetschedule', views.delete_preset_schedule, name='deletepresetschedule'),
    path('launchpreset', views.execute_preset, name='executepreset'),
    path('activeschedules', views.active_schedules, name='activeschedules'),
    path('deleteschedulefromactive', views.delete_schedule_activeschedulepage, name="deleteschedulefromactive"),
    path('markinactivefromactive', views.mark_inactive_from_active, name="markinactivefromactive"),
]
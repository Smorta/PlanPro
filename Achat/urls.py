from django.conf.urls import url
from django.urls import include, path
from Achat import views

urlpatterns = [
	url(r'^Home/$',views.index,name='index'),
	url(r'^Achat/$',views.achat,name='achat'),
	url(r'^Chantier/New/$',views.Chantier_new,name='Chantier_new'),
	url(r'^Chantier/Modif/(?P<chant_id>[0-9]+)/$',views.Chantier_modif,name='Chantier_Modif'),
	url(r'^Phase/New/(?P<chant_id>[0-9]+)(?P<typePhase>\w+)/$', views.Phase_new,name='Phase_new'),
	url(r'^Phase/Modif(?P<phase_id>[0-9]+)/$',views.Phase_modif,name='Phase_modif'),
	url(r'^Phase/Save(?P<phase_id>[0-9]+)/$',views.Phase_save,name='Phase_save'),
	url(r'^Phase/Delete(?P<phase_id>[0-9]+)/$',views.phaseDelete,name='Phase_delete'),
	url(r'^Chantier/Delete(?P<chant_id>[0-9]+)/$',views.chantierDelete,name='Chantier_delete'),
	url(r'^TimelineChant/(?P<Year>\w+)/(?P<Month>\w+)/(?P<Day>\w+)$', views.scheduleChant, name='timelineChant'),
	url(r'^TimelineAcheteur/(?P<Year>\w+)/(?P<Month>\w+)/(?P<Day>\w+)$',views.scheduleAcheteur,name='timelineAchat'),
	url(r'^RefreshTimelineChant/$', views.refreshScheduleChant, name = 'RefreshScheduleChant'),
	url(r'^RefreshTimelineAchat/$', views.refreshScheduleAchat, name = 'RefreshScheduleAchat'),
	url(r'^ResizeTask/$', views.resizeTask, name = 'ResizeTask'),
	path(r'^SetDateTimelineAchat/<str:Data>/$', views.setDateTimelineAchat, name = 'SetDateTimelineAchat')
]
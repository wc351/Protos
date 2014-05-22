from django.conf.urls import patterns, include, url
from DP import views

urlpatterns = patterns('',
                       url(r'^$', views.MainView.as_view(), name='main_page'),
                       url(r'^projectdashboard/(?P<project_pk>\d+)/$', views.ProjectDashboard.as_view(), name='project_dashboard'),
                       url(r'^createproject/$', views.CreateProject.as_view(), name='create_project'),

                       url(r'^createsite/(?P<project_pk>\d+)/$', views.CreateSite.as_view(), name='create_Site'),

                       url(r'^createlocation/(?P<project_pk>\d+)/$', views.CreateLocation.as_view(), name='location'),


                       url(r'^createmeasurement/(?P<project_pk>\d+)/$', views.CreateMeasure.as_view(), name='measurement'),

                       url(r'^enterdata/(?P<project_pk>\d+)/$', views.EnterData.as_view(), name='enter_data'),
                       url(r'^viewdata/(?P<project_pk>\d+)/$', views.ViewData.as_view(), name='view_data'),
                       url(r'^layout_test/(?P<project_pk>\d+)/$', views.Layout_Test.as_view(), name='layout_test'),

                       url(r'^managefields/(?P<project_pk>\d+)/$', views.ManageFields.as_view(), name='managefields'),

                       url(r'^fieldupdate/(?P<project_pk>\d+)/(?P<f_type>\d+)/(?P<field_pk>\d+)/$', views.FieldUpdate2.as_view(), name='fieldupdate'),
                       url(r'^viewfield/(?P<project_pk>\d+)/(?P<f_type>\d+)/(?P<field_pk>\d+)/$', views.ViewField.as_view(), name='fieldview'),
                       url(r'^fielddelete/(?P<project_pk>\d+)/(?P<f_type>\d+)/(?P<field_pk>\d+)/$', views.DeleteFieldObjects.as_view(), name='delete'),

                       url(r'^createoos/(?P<project_pk>\d+)/$', views.CreateOOS.as_view(), name='oos'),
                       url(r'^oosupdate/(?P<project_pk>\d+)/(?P<oos_type>\d+)/(?P<oos_fields_pk>\d+)/$', views.OOSUpdate.as_view(), name='oosupdate'),
                       url(r'^oosview/(?P<project_pk>\d+)/(?P<oos_type>\d+)/(?P<oos_fields_pk>\d+)/$', views.OOSView.as_view(), name='oosview'),
                       url(r'^oosdelete/(?P<project_pk>\d+)/(?P<oos_type>\d+)/(?P<oos_fields_pk>\d+)/$', views.DeleteOOSObjects.as_view(), name='oosupdate'),

                       url(r'^editproject/$', views.EditProject.as_view(), name='editproject'),

                       )


#
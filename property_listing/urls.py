from django.urls import path
from . import views
from .views import count, countview


urlpatterns = [
    path('create/type1', views.create_type1, name='create_type1'),
    path('create/type2', views.create_type2, name='create_type2'),
    path('create/type3', views.create_type3, name='create_type3'),
    
    path('getfull/type1', views.getfull_type1, name='getfull_type1'),
    path('getfull/type2', views.getfull_type2, name='getfull_type2'),
    path('getfull/type3', views.getfull_type3, name='getfull_type3'),
    path('largecard/type1', views.largecard_type1, name='largecard_type1'),
    path('largecard/type2', views.largecard_type2, name='largecard_type2'),
    path('largecard/type3', views.largecard_type3, name='largecard_type3'),
    path('smallcard/type1', views.smallcard_type1, name='smallcard_type1'),
    path('smallcard/type2', views.smallcard_type2, name='smallcard_type2'),
    path('smallcard/type3', views.smallcard_type3, name='smallcard_type3'),
    path('<int:pk>/unlist/type1', views.unlist_type1, name='unlist_type1'),
    path('<int:pk>/unlist/type2', views.unlist_type2, name='unlist_type2'),
    path('<int:pk>/unlist/type3', views.unlist_type3, name='unlist_type3'),
    path('api/location/', views.get_user_location, name='get_user_location'),
    path('location/',views.location_page,name='location_page'),
   

    #crm views
    path('<int:id>/crmstatus/type1', views.update_crm_status_type1, name='update_crm_status_type1'),
    path('<int:id>/crmstatus/type2', views.update_crm_status_type2, name='update_crm_status_type2'),
    path('<int:id>/crmstatus/type3', views.update_crm_status_type3, name='update_crm_status_type3'),
    path('crm/type1', views.crm_card_type1, name='crm_card_type1'),
    path('crm/type2', views.crm_card_type2, name='crm_card_type2'),
    path('crm/type3', views.crm_card_type3, name='crm_card_type3'),
    path('crm/<int:pk>/contacted/type1',views.update_contacted_status_type1),
    path('crm/<int:pk>/contacted/type2',views.update_contacted_status_type2),
    path('crm/<int:pk>/contacted/type3',views.update_contacted_status_type3),

    #selling property views
    path('<int:property_id>/sell/type1', views.sell_property_type1, name='sell_property_type1'),
    path('<int:property_id>/sell/type2', views.sell_property_type2, name='sell_property_type2'),
    path('<int:property_id>/sell/type3', views.sell_property_type3, name='sell_property_type3'),

    #edit property views
    path('edit/type1/<int:pk>/', views.update_property_type1, name='update_property_type1'),
    path('edit/type2/<int:pk>/', views.update_property_type2, name='update_property_type2'),
    path('edit/type3/<int:pk>/', views.update_property_type3, name='update_property_type3'),

    #all props views
    path('getfull/all', views.get_all_properties, name='get_all_properties'),
    path('smallcard/all', views.get_all_smallcard_properties , name='get_all_smallcard_properties'),
    path('largecard/all', views.get_all_largecard_properties , name='get_all_largecard_properties'),
	path('crm/all', views.crm_card_combined, name='crm_card_combined'),
 
 
    path('api/count/', count.as_view(), name='count'),
    path('api/countview/', countview.as_view(), name='countview'),
]


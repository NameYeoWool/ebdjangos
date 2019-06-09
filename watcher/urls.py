from django.urls import path
from . import views


urlpatterns = [
    path('save/',views.seatInfo_save),
    path('room/seat/<str:name>/',views.room_seat),
    path('room/new/', views.room_new, name='room_new'),
    path('room/detail/<str:name>/', views.room_detail, name='room_detail'),
    path('room/edit/<str:name>/', views.room_edit, name='room_edit'),
    path('room/remove/<str:name>/', views.room_remove, name='room_remove'),
    path('room/info/<str:pcname>/', views.room_info),
    path('room/seat/', views.room_seat),
    path('room/image/<str:name>',views.room_image),
    path('room/<str:region>/', views.room_region),
    path('events',views.eventInfo),
    path('logs',views.logs),
    # path('room/food/<str:name>/',views.room_food),
    path('room/food/<str:name>/',views.foodUpload,name='room_food'),
    path('room/food/<str:name>/list/',views.food_list, name='food_list'),
    path('room/food/<str:name>/<str:number>/',views.food_image),
    path('room/review/<str:name>/list/',views.review_list,name='review_list'),
    path('room/review/new/',views.review_new,name='review_new'),
    path('', views.room_list, name='room_list'),
]

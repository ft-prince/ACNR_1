from django.urls import path
from . import views
from .views import screen_slider

urlpatterns = [
    path('home', views.home, name='home'),
    path('screens/', views.ScreenListView.as_view(), name='screen_list'),
    path('screens/<int:pk>/', views.ScreenDetailView.as_view(), name='screen_detail'),
    path('screens/create/', views.ScreenCreateView.as_view(), name='screen_create'),
    path('screens/<int:pk>/update/', views.ScreenUpdateView.as_view(), name='screen_update'),
    path('screens/<int:pk>/delete/', views.ScreenDeleteView.as_view(), name='screen_delete'),
    path('screens/<int:screen_id>/add_content/', views.add_content_to_screen, name='add_content_to_screen'),
    path('pdfs/', views.PDFFileListView.as_view(), name='pdf_list'),
    path('pdfs/<int:pk>/', views.PDFFileDetailView.as_view(), name='pdf_detail'),
    path('pdfs/create/', views.PDFFileCreateView.as_view(), name='pdf_create'),
    path('pdfs/<int:pk>/update/', views.PDFFileUpdateView.as_view(), name='pdf_update'),
    path('pdfs/<int:pk>/delete/', views.PDFFileDeleteView.as_view(), name='pdf_delete'),
    path('videos/', views.VideoFileListView.as_view(), name='video_list'),
    path('videos/<int:pk>/', views.VideoFileDetailView.as_view(), name='video_detail'),
    path('videos/create/', views.VideoFileCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/update/', views.VideoFileUpdateView.as_view(), name='video_update'),
    path('videos/<int:pk>/delete/', views.VideoFileDeleteView.as_view(), name='video_delete'),
    path('pdf/<int:screen_id>/', views.pdf_slideshow_view, name='pdf_slider'),
    path('video/<int:screen_id>/', views.slideshow_view, name='slideshow'),
    path('plans/', views.production_plan_list, name='production_plan_list'),
    path('plans2/', views.production_plan_list2, name='production_plan_list2'),
    # path('images/', views.display_images, name='display_images'),
    # path('images/', views.slider_view, name='slider'),
    path('images/', views.image_slider_view, name='image_slider'),
    path('<int:screen_id>/', screen_slider, name='screen_slider'),
    path('', views.DailyProductionPlanListView.as_view(), name='production_plan_list'),
    path('mydaily/<int:pk>/', views.DailyProductionPlanDetailView.as_view(), name='production_plan_detail'),
    path('add/', views.add_production_plan, name='add_production_plan'),
    path('search-units/', views.search_units, name='search_units'),
    path('line/<int:assembly_line_number>/<str:date>/', views.assembly_line_production, name='assembly_line_production'),
    path('production_list', views.production_list, name='production_list'),


    

]

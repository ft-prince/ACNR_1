from django.urls import path
from . import views
from .views import screen_slider
# from .views import     weekly_data_list_view, weekly_data_create_view, weekly_data_update_view, weekly_data_delete_view
from .views import update_actual_value
from .views import export_production_plan_pdf, export_production_plan_to_excel,export_production_plan_total_pdf,export_production_plan_total_to_excel 


from .views import (
    WeeklyProductionPlanListView,
    WeeklyProductionPlanDetailView,
    update_weekly_daily_plan,
    add_weekly_production_plan,
    add_weekly_daily_plan,
    search_weekly_units,
    weekly_production_summary,
    export_weekly_plan_pdf,
    export_weekly_plan_to_excel
)

urlpatterns = [
    path('home', views.home, name='home'),
    path('screens/', views.ScreenListView.as_view(), name='screen_list'),
    path('screens/<int:pk>/', views.ScreenDetailView.as_view(), name='screen_detail'),
    path('screens/create/', views.ScreenCreateView.as_view(), name='screen_create'),
    path('screens/<int:pk>/update/', views.ScreenUpdateView.as_view(), name='screen_update'),
    path('screens/<int:pk>/delete/', views.ScreenDeleteView.as_view(), name='screen_delete'),
    path('screens/<int:screen_id>/add_content/', views.add_content_to_screen, name='add_content_to_screen'),
   path('delete-media/<str:type>/<int:id>/', views.delete_media, name='delete_media'),
    # path('pdfs/', views.PDFFileListView.as_view(), name='pdf_list'),
    # path('pdfs/<int:pk>/', views.PDFFileDetailView.as_view(), name='pdf_detail'),
    # path('pdfs/create/', views.PDFFileCreateView.as_view(), name='pdf_create'),
    # path('pdfs/<int:pk>/update/', views.PDFFileUpdateView.as_view(), name='pdf_update'),
    # path('pdfs/<int:pk>/delete/', views.PDFFileDeleteView.as_view(), name='pdf_delete'),
    path('videos/', views.VideoFileListView.as_view(), name='video_list'),
    path('videos/<int:pk>/', views.VideoFileDetailView.as_view(), name='video_detail'),
    path('videos/create/', views.VideoFileCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/update/', views.VideoFileUpdateView.as_view(), name='video_update'),
    path('videos/<int:pk>/delete/', views.VideoFileDeleteView.as_view(), name='video_delete'),
    # path('pdf/<int:screen_id>/', views.pdf_slideshow_view, name='pdf_slider'),
    # path('video/<int:screen_id>/', views.slideshow_view, name='slideshow'),
    # path('plans/', views.production_plan_list, name='production_plan_list'),
    # path('plans2/', views.production_plan_list2, name='production_plan_list2'),
    # path('images/', views.display_images, name='display_images'),
    # path('images/', views.slider_view, name='slider'),
    # path('images/', views.image_slider_view, name='image_slider'),
    path('<int:screen_id>/', screen_slider, name='screen_slider'),
 # For Total 
    path('', views.DailyProductionPlanListView.as_view(), name='production_plan_list'),
    path('mydaily/<int:pk>/', views.DailyProductionPlanDetailView.as_view(), name='production_plan_detail'),
    path('add/', views.add_production_plan, name='add_production_plan'),
    path('search-units/', views.search_units, name='search_units'),
    path('total/<int:assembly_line_number>/', views.assembly_line_production, name='assembly_line_production'),
# ----------------------------------------------------------------
# For Linewise
    path('linewise/', views.ProductionPlanListView.as_view(), name='production_plan_list_linewise'),
    path('linewise/<int:pk>/', views.ProductionPlanDetailView.as_view(), name='production_plan_detail_linewise'),
    path('add_linewise/', views.add_production_plan_linewise, name='add_production_plan_linewise'),
    path('search-units-linewise/', views.search_units_linewise, name='search_units_linewise'),
    path('line/<int:assembly_line_number>/', views.assembly_line_production_linewise, name='assembly_line_production_linewise'),
    path('update-actual/<int:plan_id>/', views.update_actual_value, name='update_actual_value'),
    path('update-actual-total/<int:plan_id>/', views.update_daily_actual_value_total, name='update_actual_value_total'),


# ----------------------------------------------------------------
# exporting

    path('export-production-plan-pdf/', export_production_plan_pdf, name='export_production_plan_pdf'),
    path('export-production-plan/', export_production_plan_to_excel, name='export_production_plan'),

#  for total execution
    path('export-production-plan-total-pdf/', export_production_plan_total_pdf, name='export_production_plan_total_pdf'),
    path('export-production-total-plan/', export_production_plan_total_to_excel, name='export_production_total_plan'),


# Weekly

    # List view of weekly production plans
    path('weekly/', WeeklyProductionPlanListView.as_view(), name='weekly_production_plan_list'),
    
    # Detail view of a specific weekly production plan
    path('weekly/plan/<int:pk>/', WeeklyProductionPlanDetailView.as_view(), name='weekly_production_plan_detail'),
    
    # Endpoint to update a daily plan
    path('weekly/plan/update/<int:plan_id>/', update_weekly_daily_plan, name='update_weekly_daily_plan'),
    
    # View to add a new weekly production plan
    path('weekly/plan/add/', add_weekly_production_plan, name='add_weekly_production_plan'),
    
    # View to add a new daily plan to a weekly production plan
    path('weekly/plan/daily/add/', add_weekly_daily_plan, name='add_weekly_daily_plan'),
    
    # Endpoint for searching units
    path('weekly/units/search/', search_weekly_units, name='search_weekly_units'),
    
    # View to get a summary of a weekly production plan
    path('weekly/plan/summary/<int:week_id>/', weekly_production_summary, name='weekly_production_summary'),
    
    # Endpoint to export the weekly plan as a PDF
    path('weekly/plan/export/pdf/<int:week_id>/', export_weekly_plan_pdf, name='export_weekly_plan_pdf'),
    
    # Endpoint to export the weekly plan to an Excel file
    path('weekly/plan/export/excel/<int:week_id>/', export_weekly_plan_to_excel, name='export_weekly_plan_to_excel'),

# ----------------------------------------------------------------
    # path('weekly/', views.plan_list, name='plan_list'),
    # path('plan/<int:pk>/', plan_detail, name='plan_detail'),
    # path('plan/new/', plan_create, name='plan_create'),
    # path('plan/<int:pk>/edit/', plan_update, name='plan_update'),
    # path('plan/<int:pk>/delete/', plan_delete, name='plan_delete'),

    # path('<int:unit_id>/weekly-data/', weekly_data_list_view, name='weekly_data_list'),
    # path('<int:unit_id>/weekly-data/create/', weekly_data_create_view, name='weekly_data_create'),
    # path('weekly-data/<int:pk>/update/', weekly_data_update_view, name='weekly_data_update'),
    # path('weekly-data/<int:pk>/delete/', weekly_data_delete_view, name='weekly_data_delete'),

    # path('weekly/', views.WeeklyPlanListView.as_view(), name='weekly_plan_list'),
    # path('weekly/<int:pk>/', views.WeeklyPlanDetailView.as_view(), name='weekly_plan_detail'),
    # path('weekly/create/', views.WeeklyPlanCreateView.as_view(), name='weekly_plan_create'),
    # path('weekly/<int:pk>/update/', views.WeeklyPlanUpdateView.as_view(), name='weekly_plan_update'),
    # path('weekly/<int:pk>/delete/', views.WeeklyPlanDeleteView.as_view(), name='weekly_plan_delete'),
]

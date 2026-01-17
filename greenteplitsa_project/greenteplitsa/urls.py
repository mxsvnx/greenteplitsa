from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),

    path("greenteplitsas/", views.GreenteplitsaListView.as_view(), name="greenteplitsa_list"),
    path("greenteplitsas/add/", views.GreenteplitsaCreateView.as_view(), name="greenteplitsa_add"),
    path("greenteplitsas/<int:pk>/edit/", views.GreenteplitsaUpdateView.as_view(), name="greenteplitsa_edit"),
    path("greenteplitsas/<int:pk>/delete/", views.GreenteplitsaDeleteView.as_view(), name="greenteplitsa_delete"),
    path("crops/", views.CropListView.as_view(), name="crop_list"),
    path("crops/add/", views.CropCreateView.as_view(), name="crop_add"),
    path("crops/<int:pk>/edit/", views.CropUpdateView.as_view(), name="crop_edit"),
    path("crops/<int:pk>/delete/", views.CropDeleteView.as_view(), name="crop_delete"),
    path("cycles/", views.CropCycleListView.as_view(), name="cycle_list"),
    path("cycles/add/", views.CropCycleCreateView.as_view(), name="cycle_add"),
    path("cycles/<int:pk>/edit/", views.CropCycleUpdateView.as_view(), name="cycle_edit"),
    path("cycles/<int:pk>/delete/", views.CropCycleDeleteView.as_view(), name="cycle_delete"),
    path("cycles/<int:pk>/", views.CropCycleDetailView.as_view(), name="cycle_detail"),
    path("cycles/<int:pk>/generate-plan/", views.generate_cycle_plan, name="cycle_generate_plan"),
    path("cycles/<int:pk>/logs/add/", views.add_work_log, name="cycle_add_log"),
    path("schedules/", views.CropScheduleListView.as_view(), name="schedule_list"),
    path("schedules/add/", views.CropScheduleCreateView.as_view(), name="schedule_add"),
    path("schedules/<int:pk>/edit/", views.CropScheduleUpdateView.as_view(), name="schedule_edit"),
    path("schedules/<int:pk>/delete/", views.CropScheduleDeleteView.as_view(), name="schedule_delete"),


]

from django.contrib import admin

from .models import Crop, CropCycle, CropSchedule, Greenteplitsa, WorkLog, WorkPlan, WorkType


@admin.register(Greenteplitsa)
class GreenteplitsaAdmin(admin.ModelAdmin):
    list_display = ("name", "greenteplitsa_type", "area_m2", "location", "is_active")
    list_filter = ("greenteplitsa_type", "is_active")
    search_fields = ("name", "location")


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "variety")
    search_fields = ("name", "variety")


@admin.register(CropSchedule)
class CropScheduleAdmin(admin.ModelAdmin):
    list_display = ("crop", "sow_start", "sow_end", "harvest_start", "harvest_end")
    search_fields = ("crop__name", "crop__variety")


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(CropCycle)
class CropCycleAdmin(admin.ModelAdmin):
    list_display = ("greenteplitsa", "crop", "start_date", "end_date", "status", "created_by")
    list_filter = ("status", "greenteplitsa")
    search_fields = ("greenteplitsa__name", "crop__name", "crop__variety", "created_by__username")


@admin.register(WorkPlan)
class WorkPlanAdmin(admin.ModelAdmin):
    list_display = ("cycle", "work_type", "planned_date", "planned_end_date")
    list_filter = ("work_type",)
    search_fields = ("cycle__greenteplitsa__name", "cycle__crop__name")


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ("cycle", "work_type", "actual_date", "water_liters", "fertilizer_kg", "yield_kg", "created_by")
    list_filter = ("work_type",)
    search_fields = ("cycle__greenteplitsa__name", "cycle__crop__name", "created_by__username")

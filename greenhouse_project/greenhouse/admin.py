from django.contrib import admin

from .models import Crop, CropCycle, CropSchedule, Greenhouse, WorkLog, WorkPlan, WorkType


@admin.register(Greenhouse)
class GreenhouseAdmin(admin.ModelAdmin):
    list_display = ("name", "greenhouse_type", "area_m2", "location", "is_active")
    list_filter = ("greenhouse_type", "is_active")
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
    list_display = ("greenhouse", "crop", "start_date", "end_date", "status", "created_by")
    list_filter = ("status", "greenhouse")
    search_fields = ("greenhouse__name", "crop__name", "crop__variety", "created_by__username")


@admin.register(WorkPlan)
class WorkPlanAdmin(admin.ModelAdmin):
    list_display = ("cycle", "work_type", "planned_date", "planned_end_date")
    list_filter = ("work_type",)
    search_fields = ("cycle__greenhouse__name", "cycle__crop__name")


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ("cycle", "work_type", "actual_date", "water_liters", "fertilizer_kg", "yield_kg", "created_by")
    list_filter = ("work_type",)
    search_fields = ("cycle__greenhouse__name", "cycle__crop__name", "created_by__username")

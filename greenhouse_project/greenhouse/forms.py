from django import forms

from .models import Greenhouse
from .models import Crop
from .models import CropCycle
from .models import WorkLog
from .models import CropSchedule


class GreenhouseForm(forms.ModelForm):
    class Meta:
        model = Greenhouse
        fields = ("name", "greenhouse_type", "area_m2", "location", "is_active")


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ("name", "variety", "description")


class CropCycleForm(forms.ModelForm):
    class Meta:
        model = CropCycle
        fields = ("greenhouse", "crop", "start_date", "end_date", "status")


class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = (
            "work_type",
            "actual_date",
            "water_liters",
            "fertilizer_kg",
            "labor_hours",
            "yield_kg",
            "comment",
        )


class CropScheduleForm(forms.ModelForm):
    class Meta:
        model = CropSchedule
        fields = (
            "crop",
            "sow_start", "sow_end",
            "watering_start", "watering_end",
            "fertilizing_start", "fertilizing_end",
            "harvest_start", "harvest_end",
        )

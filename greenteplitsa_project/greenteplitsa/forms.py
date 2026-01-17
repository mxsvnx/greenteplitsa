from django import forms

from .models import Greenteplitsa
from .models import Crop
from .models import CropCycle
from .models import WorkLog
from .models import CropSchedule


class GreenteplitsaForm(forms.ModelForm):
    class Meta:
        model = Greenteplitsa
        fields = ("name", "greenteplitsa_type", "area_m2", "location", "is_active")


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ("name", "variety", "description")


class CropCycleForm(forms.ModelForm):
    class Meta:
        model = CropCycle
        fields = ("greenteplitsa", "crop", "start_date", "end_date", "status")


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

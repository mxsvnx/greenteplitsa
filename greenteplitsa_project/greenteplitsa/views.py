from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.shortcuts import redirect
from django.db.models import Sum
from django.contrib import messages


from .forms import CropCycleForm, CropForm, CropScheduleForm, GreenteplitsaForm, WorkLogForm
from .mixins import ChiefAgronomistRequiredMixin
from .models import Crop, CropCycle, CropSchedule, Greenteplitsa, WorkPlan, WorkType


class DashboardView(TemplateView):
    template_name = "greenhouse/dashboard.html"


class GreenteplitsaListView(LoginRequiredMixin, ListView):
    model = Greenteplitsa
    template_name = "greenhouse/greenteplitsa_list.html"
    context_object_name = "greenteplitsas"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_superuser or user.groups.filter(name="chief_agronomist").exists()
        return context


class GreenteplitsaCreateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, CreateView):
    model = Greenteplitsa
    form_class = GreenteplitsaForm
    template_name = "greenhouse/greenteplitsa_form.html"
    success_url = reverse_lazy("greenteplitsa_list")


class GreenteplitsaUpdateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, UpdateView):
    model = Greenteplitsa
    form_class = GreenteplitsaForm
    template_name = "greenhouse/greenteplitsa_form.html"
    success_url = reverse_lazy("greenteplitsa_list")


class GreenteplitsaDeleteView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, DeleteView):
    model = Greenteplitsa
    template_name = "greenhouse/greenteplitsa_confirm_delete.html"
    success_url = reverse_lazy("greenteplitsa_list")


class CropListView(LoginRequiredMixin, ListView):
    model = Crop
    template_name = "greenhouse/crop_list.html"
    context_object_name = "crops"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_superuser or user.groups.filter(name="chief_agronomist").exists()
        return context


class CropCreateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, CreateView):
    model = Crop
    form_class = CropForm
    template_name = "greenhouse/crop_form.html"
    success_url = reverse_lazy("crop_list")


class CropUpdateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, UpdateView):
    model = Crop
    form_class = CropForm
    template_name = "greenhouse/crop_form.html"
    success_url = reverse_lazy("crop_list")


class CropDeleteView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, DeleteView):
    model = Crop
    template_name = "greenhouse/crop_confirm_delete.html"
    success_url = reverse_lazy("crop_list")


class CropCycleListView(LoginRequiredMixin, ListView):
    model = CropCycle
    template_name = "greenhouse/cycle_list.html"
    context_object_name = "cycles"
    paginate_by = 20

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("greenteplitsa", "crop", "created_by")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_superuser or user.groups.filter(name="chief_agronomist").exists()
        return context


class CropCycleCreateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, CreateView):
    model = CropCycle
    form_class = CropCycleForm
    template_name = "greenhouse/cycle_form.html"
    success_url = reverse_lazy("cycle_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CropCycleUpdateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, UpdateView):
    model = CropCycle
    form_class = CropCycleForm
    template_name = "greenhouse/cycle_form.html"
    success_url = reverse_lazy("cycle_list")


class CropCycleDeleteView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, DeleteView):
    model = CropCycle
    template_name = "greenhouse/cycle_confirm_delete.html"
    success_url = reverse_lazy("cycle_list")


class CropCycleDetailView(LoginRequiredMixin, DetailView):
    model = CropCycle
    template_name = "greenhouse/cycle_detail.html"
    context_object_name = "cycle"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("greenteplitsa", "crop", "created_by")
            .prefetch_related("plans__work_type", "logs__work_type")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_superuser or user.groups.filter(name="chief_agronomist").exists()
        context["plans"] = self.object.plans.order_by("planned_date", "id")
        context["logs"] = self.object.logs.order_by("-actual_date", "-id")
        totals = self.object.logs.aggregate(
            total_water=Sum("water_liters"),
            total_fertilizer=Sum("fertilizer_kg"),
            total_labor=Sum("labor_hours"),
            total_yield=Sum("yield_kg"),
        )
        context["totals"] = totals
        context["work_types"] = WorkType.objects.order_by("name")
        return context


def generate_cycle_plan(request, pk: int):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")

    if not (user.is_superuser or user.groups.filter(name="chief_agronomist").exists()):
        messages.error(request, "Недостаточно прав для генерации плана.")
        return redirect("cycle_detail", pk=pk)


    if request.method != "POST":
        return redirect("cycle_detail", pk=pk)

    cycle = CropCycle.objects.select_related("crop").get(pk=pk)

    schedule = getattr(cycle.crop, "schedule", None)
    if schedule is None:
        messages.warning(request, "Для культуры не задан график. Сначала создайте график, затем повторите генерацию.")
        return redirect("cycle_detail", pk=pk)


    WorkPlan.objects.filter(cycle=cycle).delete()

    mapping = [
        (WorkType.CODE_SOWING, schedule.sow_start, schedule.sow_end),
        (WorkType.CODE_WATERING, schedule.watering_start, schedule.watering_end),
        (WorkType.CODE_FERTILIZING, schedule.fertilizing_start, schedule.fertilizing_end),
        (WorkType.CODE_HARVEST, schedule.harvest_start, schedule.harvest_end),
    ]

    work_types = {wt.code: wt for wt in WorkType.objects.filter(code__in=[m[0] for m in mapping])}

    plans = []
    for code, start, end in mapping:
        if start is None:
            continue
        wt = work_types.get(code)
        if wt is None:
            continue
        plans.append(
            WorkPlan(
                cycle=cycle,
                work_type=wt,
                planned_date=start,
                planned_end_date=end,
            )
        )

    if plans:
        WorkPlan.objects.bulk_create(plans)

    return redirect("cycle_detail", pk=pk)


def add_work_log(request, pk: int):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")

    if not (user.is_superuser or user.groups.filter(name="chief_agronomist").exists()):
        return redirect("cycle_detail", pk=pk)

    cycle = CropCycle.objects.get(pk=pk)

    if request.method == "POST":
        form = WorkLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.cycle = cycle
            log.created_by = user
            log.save()
    return redirect("cycle_detail", pk=pk)


class CropScheduleListView(LoginRequiredMixin, ListView):
    model = CropSchedule
    template_name = "greenhouse/schedule_list.html"
    context_object_name = "schedules"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related("crop")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_superuser or user.groups.filter(name="chief_agronomist").exists()
        return context


class CropScheduleCreateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, CreateView):
    model = CropSchedule
    form_class = CropScheduleForm
    template_name = "greenhouse/schedule_form.html"
    success_url = reverse_lazy("schedule_list")


class CropScheduleUpdateView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, UpdateView):
    model = CropSchedule
    form_class = CropScheduleForm
    template_name = "greenhouse/schedule_form.html"
    success_url = reverse_lazy("schedule_list")


class CropScheduleDeleteView(LoginRequiredMixin, ChiefAgronomistRequiredMixin, DeleteView):
    model = CropSchedule
    template_name = "greenhouse/schedule_confirm_delete.html"
    success_url = reverse_lazy("schedule_list")

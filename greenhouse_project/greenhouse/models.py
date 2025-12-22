from django.conf import settings
from django.db import models


class Greenhouse(models.Model):
    TYPE_VEGETABLES = "vegetables"
    TYPE_GREENS = "greens"
    TYPE_BERRIES = "berries"
    TYPE_OTHER = "other"

    TYPE_CHOICES = (
        (TYPE_VEGETABLES, "Овощи"),
        (TYPE_GREENS, "Зелень"),
        (TYPE_BERRIES, "Ягоды"),
        (TYPE_OTHER, "Другое"),
    )

    name = models.CharField("Название", max_length=128, unique=True)
    greenhouse_type = models.CharField(
        "Тип продукции",
        max_length=32,
        choices=TYPE_CHOICES,
        default=TYPE_VEGETABLES,
    )
    area_m2 = models.DecimalField("Площадь, м²", max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField("Расположение", max_length=128, blank=True)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Теплица"
        verbose_name_plural = "Теплицы"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Crop(models.Model):
    name = models.CharField("Культура", max_length=128)
    variety = models.CharField("Сорт", max_length=128, blank=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Овощная культура"
        verbose_name_plural = "Овощные культуры"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(fields=("name", "variety"), name="uniq_crop_name_variety")
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.variety}".strip()


class CropSchedule(models.Model):
    crop = models.OneToOneField(
        Crop,
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Культура",
    )

    sow_start = models.DateField("Посев: начало", null=True, blank=True)
    sow_end = models.DateField("Посев: окончание", null=True, blank=True)

    watering_start = models.DateField("Полив: начало", null=True, blank=True)
    watering_end = models.DateField("Полив: окончание", null=True, blank=True)
    watering_interval_days = models.PositiveSmallIntegerField("Полив: интервал (дней)", null=True, blank=True)

    fertilizing_start = models.DateField("Удобрения: начало", null=True, blank=True)
    fertilizing_end = models.DateField("Удобрения: окончание", null=True, blank=True)
    fertilizing_interval_days = models.PositiveSmallIntegerField("Удобрения: интервал (дней)", null=True, blank=True)

    harvest_start = models.DateField("Сбор: начало", null=True, blank=True)
    harvest_end = models.DateField("Сбор: окончание", null=True, blank=True)

    class Meta:
        verbose_name = "График культуры"
        verbose_name_plural = "Графики культур"

    def __str__(self) -> str:
        return f"График: {self.crop}"


class CropCycle(models.Model):
    STATUS_PLANNED = "planned"
    STATUS_ACTIVE = "active"
    STATUS_FINISHED = "finished"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PLANNED, "Запланирован"),
        (STATUS_ACTIVE, "В работе"),
        (STATUS_FINISHED, "Завершён"),
        (STATUS_CANCELED, "Отменён"),
    )

    greenhouse = models.ForeignKey(
        Greenhouse,
        on_delete=models.PROTECT,
        related_name="cycles",
        verbose_name="Теплица",
    )
    crop = models.ForeignKey(
        Crop,
        on_delete=models.PROTECT,
        related_name="cycles",
        verbose_name="Культура",
    )
    start_date = models.DateField("Начало цикла")
    end_date = models.DateField("Окончание цикла", null=True, blank=True)
    status = models.CharField("Статус", max_length=16, choices=STATUS_CHOICES, default=STATUS_PLANNED)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_cycles",
        verbose_name="Кто создал",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Цикл выращивания"
        verbose_name_plural = "Циклы выращивания"
        ordering = ("-start_date", "-id")

    def __str__(self) -> str:
        return f"{self.greenhouse} — {self.crop} ({self.start_date})"


class WorkType(models.Model):
    CODE_SOWING = "sowing"
    CODE_WATERING = "watering"
    CODE_FERTILIZING = "fertilizing"
    CODE_HARVEST = "harvest"

    code = models.CharField("Код", max_length=32, unique=True)
    name = models.CharField("Название", max_length=128)

    class Meta:
        verbose_name = "Тип работы"
        verbose_name_plural = "Типы работ"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class WorkPlan(models.Model):
    cycle = models.ForeignKey(
        CropCycle,
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name="Цикл",
    )
    work_type = models.ForeignKey(
        WorkType,
        on_delete=models.PROTECT,
        related_name="plans",
        verbose_name="Тип работы",
    )
    planned_date = models.DateField("Плановая дата")
    planned_end_date = models.DateField("Плановое окончание", null=True, blank=True)
    notes = models.TextField("Примечание", blank=True)

    class Meta:
        verbose_name = "План работ"
        verbose_name_plural = "Планы работ"
        ordering = ("planned_date", "id")

    def __str__(self) -> str:
        return f"{self.cycle}: {self.work_type} ({self.planned_date})"


class WorkLog(models.Model):
    cycle = models.ForeignKey(
        CropCycle,
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name="Цикл",
    )
    plan = models.ForeignKey(
        WorkPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs",
        verbose_name="План",
    )
    work_type = models.ForeignKey(
        WorkType,
        on_delete=models.PROTECT,
        related_name="logs",
        verbose_name="Тип работы",
    )
    actual_date = models.DateField("Фактическая дата")

    water_liters = models.DecimalField("Вода, л", max_digits=12, decimal_places=2, null=True, blank=True)
    fertilizer_kg = models.DecimalField("Удобрения, кг", max_digits=12, decimal_places=3, null=True, blank=True)
    labor_hours = models.DecimalField("Трудозатраты, ч", max_digits=8, decimal_places=2, null=True, blank=True)
    yield_kg = models.DecimalField("Урожай, кг", max_digits=12, decimal_places=3, null=True, blank=True)

    comment = models.TextField("Комментарий", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_worklogs",
        verbose_name="Кто внёс",
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Факт работ"
        verbose_name_plural = "Факты работ"
        ordering = ("-actual_date", "-id")

    def __str__(self) -> str:
        return f"{self.cycle}: {self.work_type} ({self.actual_date})"

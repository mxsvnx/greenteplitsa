from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from greenhouse.models import WorkType


class Command(BaseCommand):
    help = "Seed initial data for greenhouse app (work types and agronomist group)."

    def handle(self, *args, **options):
        work_types = [
            (WorkType.CODE_SOWING, "Посев"),
            (WorkType.CODE_WATERING, "Полив"),
            (WorkType.CODE_FERTILIZING, "Внесение удобрений"),
            (WorkType.CODE_HARVEST, "Сбор урожая"),
        ]

        created_count = 0
        updated_count = 0

        for code, name in work_types:
            obj, created = WorkType.objects.update_or_create(
                code=code,
                defaults={"name": name},
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        group, _ = Group.objects.get_or_create(name="chief_agronomist")

        ct = ContentType.objects.get(app_label="greenhouse", model="greenhouse")
        perms = Permission.objects.filter(content_type=ct)
        group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS(
            f"WorkType: created={created_count}, updated={updated_count}. "
            f"Group 'chief_agronomist' synced with greenhouse permissions."
        ))

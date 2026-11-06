from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Crea los perfiles Administrador y Operador del panel propio."

    def handle(self, *args, **options):
        administrador, _ = Group.objects.get_or_create(name="Administrador")
        operador, _ = Group.objects.get_or_create(name="Operador")
        modelos = ["producto", "categoria", "cliente", "boleta", "detalleboleta"]
        administrador.permissions.set(
            Permission.objects.filter(
                Q(content_type__app_label="core", content_type__model__in=modelos)
                | Q(content_type__app_label="auth", content_type__model="user")
            )
        )
        permisos_operador = ["view_" + modelo for modelo in modelos]
        for modelo in ["cliente", "boleta", "detalleboleta"]:
            permisos_operador.extend(["add_" + modelo, "change_" + modelo])
        operador.permissions.set(
            Permission.objects.filter(
                content_type__app_label="core", codename__in=permisos_operador
            )
        )
        for usuario in User.objects.filter(is_active=True):
            if usuario.is_superuser:
                usuario.groups.add(administrador)
            elif not usuario.groups.exists():
                usuario.groups.add(operador)
        self.stdout.write(
            self.style.SUCCESS(
                "Grupos y permisos de Administrador y Operador preparados. Las contraseñas se conservaron."
            )
        )

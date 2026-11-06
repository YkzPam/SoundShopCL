from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea los perfiles Administrador y Operador del panel propio."

    def handle(self, *args, **options):
        administrador, _ = Group.objects.get_or_create(name="Administrador")
        operador, _ = Group.objects.get_or_create(name="Operador")
        for usuario in User.objects.filter(is_active=True):
            if usuario.is_superuser:
                usuario.groups.add(administrador)
            elif not usuario.groups.exists():
                usuario.groups.add(operador)
        self.stdout.write(self.style.SUCCESS("Grupos Administrador y Operador preparados. Las contraseñas se conservaron."))

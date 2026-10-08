"""Faker en lotes para las cuatro cargas indicadas por el docente."""
from time import perf_counter
from uuid import uuid4
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker
from core.models import Cliente


class Command(BaseCommand):
    help = "Agrega clientes ficticios y verifica cuántos quedaron almacenados."

    def add_arguments(self, parser):
        parser.add_argument("--cantidad", type=int, required=True)

    def handle(self, *args, **options):
        cantidad = options["cantidad"]
        if cantidad < 1 or cantidad > 1_000_000:
            raise CommandError("La cantidad debe estar entre 1 y 1.000.000.")
        fake = Faker("es_CL")
        prefijo = uuid4().hex[:12]
        antes = Cliente.objects.count()
        inicio = perf_counter()
        lote = []
        self.stdout.write(f"Base: {Cliente.objects.db}; antes: {antes}; solicitados: {cantidad}.")

        # Una transacción permite revertir la carga completa si ocurre un error.
        # Cada lote guarda hasta 1.000 objetos; no mantiene el millón en memoria.
        with transaction.atomic():
            for numero in range(1, cantidad + 1):
                lote.append(Cliente(
                    nombre=fake.name()[:100],
                    correo=f"{prefijo}-{numero}@example.test",
                    telefono=fake.phone_number()[:20],
                    activo=True,
                ))
                if len(lote) == 1000 or numero == cantidad:
                    Cliente.objects.bulk_create(lote, batch_size=1000)
                    lote = []
                if numero % 100_000 == 0:
                    self.stdout.write(f"Preparados: {numero} / {cantidad}")

        despues = Cliente.objects.count()
        guardados = Cliente.objects.filter(correo__startswith=prefijo + "-").count()
        primero = Cliente.objects.get(correo=f"{prefijo}-1@example.test")
        ultimo = Cliente.objects.get(correo=f"{prefijo}-{cantidad}@example.test")
        if despues - antes != cantidad or guardados != cantidad:
            raise CommandError("La cantidad almacenada no coincide con la solicitada.")
        segundos = perf_counter() - inicio
        self.stdout.write(self.style.SUCCESS(
            f"VERIFICADO: añadidos={guardados}; antes={antes}; después={despues}; "
            f"segundos={segundos:.2f}; primer_id={primero.id}; ultimo_id={ultimo.id}."
        ))

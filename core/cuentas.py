"""Cuentas temporales para E1, sin base de datos ni credenciales en cookies.

Solo para el servidor local de un proceso. Reiniciarlo elimina las cuentas.
No sustituye autenticación persistente, recuperación de cuenta ni despliegue seguro.
"""

from hashlib import sha256

from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import caches


def clave_correo(correo):
    return sha256(correo.strip().casefold().encode()).hexdigest()


def crear_cuenta(nombre, correo, contrasena):
    return caches['cuentas'].add(
        'cuenta:' + clave_correo(correo),
        {'nombre': nombre, 'clave': make_password(contrasena)}, timeout=None,
    )


def verificar_cuenta(correo, contrasena):
    cuenta = caches['cuentas'].get('cuenta:' + clave_correo(correo))
    if cuenta and check_password(contrasena, cuenta['clave']):
        return {'nombre': cuenta['nombre']}
    if not cuenta:
        make_password(contrasena)  # Coste similar para correos desconocidos.
    return None

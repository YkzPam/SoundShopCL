from .decorators import es_administrador


def permisos_panel(request):
    # La interfaz utiliza el mismo criterio que las vistas protegidas.
    administrador = es_administrador(request.user)
    operador = request.user.is_authenticated and request.user.is_active and request.user.groups.filter(name="Operador").exists()
    perfil = "Administrador" if administrador else "Operador" if operador else "Sin perfil autorizado"
    return {"es_administrador": administrador, "perfil_actual": perfil}

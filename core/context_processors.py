from core.models import Notificacion

def notificaciones_context(request):
    if request.user.is_authenticated and request.user.is_superuser:
        notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False).order_by('-fecha')[:5]
        notificaciones_count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        return {
            'notificaciones': notificaciones,
            'notificaciones_count': notificaciones_count,
        }
    return {}
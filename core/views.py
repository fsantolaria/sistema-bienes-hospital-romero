from django.contrib.auth import authenticate, login, logout, get_user_model
import pandas as pd
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CargaMasivaForm, BienPatrimonialForm
from core.models import BienPatrimonial
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_date
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from core.models.notificacion import Notificacion
from django.http import JsonResponse


def _role_route_name(user) -> str:
    """Devuelve el nombre de la ruta según el rol del usuario."""
    if user.is_superuser:
        return 'home_admin'
    if hasattr(user, 'tipo_usuario'):
        return 'home_admin' if user.tipo_usuario == 'admin' else 'home_operador'
    return 'home_operador'



# ============= VISTAS =============

def permisos_context(user):
    """Booleans útiles para templates y lógica."""
    if not getattr(user, "is_authenticated", False):
        return {"es_admin": False, "puede_eliminar": False, "puede_gestionar_operadores": False}

    if hasattr(user, "tipo_usuario"):
        es_admin = user.tipo_usuario == "admin" or user.is_superuser
    else:
        es_admin = user.is_superuser

    return {
        "es_admin": es_admin,
        "puede_eliminar": es_admin,
        "puede_gestionar_operadores": es_admin,
    }


# ============================
# AUTENTICACIÓN / INICIO
# ============================

def inicio(request):

    if request.user.is_authenticated:
        return redirect(_role_route_name(request.user))
    return render(request, 'inicio.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(_role_route_name(request.user))

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        tipo_usuario = request.POST.get('tipo_usuario')
        user = authenticate(request, username=usuario, password=contrasena)
        if user is not None:
            # Validar tipo de usuario
            if tipo_usuario == 'admin':
                if user.is_superuser or (hasattr(user, 'tipo_usuario') and user.tipo_usuario == 'admin'):
                    login(request, user)
                    messages.success(request, f'¡Bienvenido {user.username}!')
                    return redirect(_role_route_name(user))
                else:
                    messages.error(request, 'El tipo de usuario seleccionado no coincide con el usuario ingresado.')
                    return render(request, 'login.html', {'login_error': True, 'request': request})
            elif tipo_usuario == 'empleado':
                # Los superusuarios NO pueden loguear como operador
                if user.is_superuser:
                    messages.error(request, 'Un administrador no puede ingresar como operador.')
                    return render(request, 'login.html', {'login_error': True, 'request': request})
                if hasattr(user, 'tipo_usuario') and user.tipo_usuario == 'empleado':
                    login(request, user)
                    messages.success(request, f'¡Bienvenido {user.username}!')
                    return redirect(_role_route_name(user))
                else:
                    messages.error(request, 'El tipo de usuario seleccionado no coincide con el usuario ingresado.')
                    return render(request, 'login.html', {'login_error': True, 'request': request})
            else:
                messages.error(request, 'Tipo de usuario no válido.')
                return render(request, 'login.html', {'login_error': True, 'request': request})
        # Authentication failed: add a message and a context flag so the template
        # can show the inline error next to the form (not only global messages)
        messages.error(request, 'Usuario o contraseña incorrectos')
        return render(request, 'login.html', {'login_error': True, 'request': request})

    return render(request, 'login.html')


@login_required
def home_operador(request):
    context = permisos_context(request.user)
    return render(request, 'home_operador.html', context)


def registro(request):
    return render(request, 'registro.html')


def bien_confirm_delete(request):
    return render(request, 'bien_confirm_delete.html')


def base(request):
    return render(request, 'base.html')


@login_required
def bienes(request):
    if request.method == "POST":
        form = BienPatrimonialForm(request.POST)
        if form.is_valid():
            bien = form.save()
            # ...existing code...
            nombre_bien = getattr(bien, 'nombre', None) or getattr(bien, 'descripcion', 'Sin nombre')
            Notificacion.objects.create(
                usuario=request.user,
                mensaje=f"Se registró el bien '{nombre_bien}' (Clave: {bien.clave_unica}) correctamente.",
                leida=False
            )
            messages.success(request, "Bien creado correctamente.")
            return redirect("lista_bienes")
        messages.error(request, "Revisá los datos del formulario.")
    else:
        form = BienPatrimonialForm()

    context = permisos_context(request.user)
    context.update({"form": form})
    return render(request, "bienes.html", context)


def logout_view(request):
    logout(request)
    list(get_messages(request))  # limpiar mensajes previos
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio')


# ============================
# ÁREA PRIVADA (requiere login)
# ============================

@login_required
def home_admin(request):
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('home_operador')
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')[:5]
    notificaciones_count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
    perms.update({
        'notificaciones': notificaciones,
        'notificaciones_count': notificaciones_count,
    })
    return render(request, 'home_admin.html', perms)


# ============= OPERADORES =============
Operador = get_user_model()

@login_required
def operadores(request):
    # Lista solo “operadores” (no staff) ordenados por nombre
    operadores_qs = Operador.objects.filter(is_staff=False).order_by('first_name', 'last_name', 'username')
    ctx = {
        "operadores": operadores_qs,
        "usar_operador_model": False,  # por si tus templates usan este flag
    }
    return render(request, "operadores.html", ctx)


def recuperar_password(request):
    if request.method == "POST":
        # Acá podrías enviar el correo o guardar el pedido en la base
        messages.success(request, "✅ Solicitud enviada correctamente.")
        return redirect('recuperar_password')  # vuelve a la misma página

    return render(request, 'recuperar_password.html')


@login_required
def alta_operadores(request):
    if request.method == "POST":
        nombre      = (request.POST.get("nombre") or "").strip()
        apellido    = (request.POST.get("apellido") or "").strip()
        pais        = (request.POST.get("pais") or "").strip()
        numero_doc  = (request.POST.get("numero_doc") or "").strip()  # OJO: guión bajo
        email       = (request.POST.get("email") or "").strip()
        estado      = (request.POST.get("estado") or "habilitado").strip()
        password    = (request.POST.get("password") or "").strip()

        # 1) Username generado con nombre+apellido (sin espacios/acentos) y único
        base_username = slugify(f"{nombre}.{apellido}") or (email.split("@")[0] if email else "")
        if not base_username:
            messages.error(request, "No se pudo generar un usuario. Completá Nombre/Apellido o Email.")
            return redirect("alta_operadores")

        username = base_username
        i = 1
        while Operador.objects.filter(username=username).exists():
            i += 1
            username = f"{base_username}{i}"

        # 2) is_active según “estado”
        is_active = (estado == "habilitado")

        # 3) Crear usuario operador
        operador = Operador(
            username=username,
            email=email or None,
            first_name=nombre,
            last_name=apellido,
            is_staff=False,         # no es admin
            is_superuser=False,     # no es superuser
            is_active=is_active,
        )
        # Asignar tipo_usuario y setear password ANTES de guardar
        operador.tipo_usuario = 'empleado'
        if password:
            operador.set_password(password)
        else:
            operador.set_password(username)  # fallback: username como password si no se ingresa
        # Campos extra si tu User los tiene:
        if hasattr(operador, "pais"):
            operador.pais = pais
        if hasattr(operador, "numero_doc"):
            operador.numero_doc = numero_doc
        if hasattr(operador, "estado"):
            operador.estado = estado  # guarda cadena 'habilitado' / 'no-habilitado'
        # Intentar guardar el usuario con reintentos en caso de colisiones únicas
        saved = False
        attempts = 0
        while not saved and attempts < 10:
            try:
                operador.save()
                saved = True
            except IntegrityError:
                # Probablemente una colisión en username; generar una variante y reintentar
                attempts += 1
                i += 1
                username = f"{base_username}{i}"
                operador.username = username
        if not saved:
            messages.error(request, "No se pudo crear el usuario debido a un conflicto de nombre. Intentá de nuevo más tarde o con otro nombre.")
            return redirect("alta_operadores")

        # Notificación de creación de operador
        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Se creó el operador '{operador.username}'.",
            leida=False
        )

        messages.success(request, f"Operador {nombre} {apellido} creado. Usuario: {operador.username}")
        return redirect("operadores")  # ← vuelve al listado

    # GET
    return render(request, "alta_operadores.html", {"usar_operador_model": False})


@login_required
def editar_operador(request, pk):
    operador = get_object_or_404(Operador, pk=pk, is_staff=False)

    if request.method == "POST":
        nombre      = (request.POST.get("nombre") or "").strip()
        apellido    = (request.POST.get("apellido") or "").strip()
        email       = (request.POST.get("email") or "").strip()
        estado      = (request.POST.get("estado") or "habilitado").strip()
        pais        = (request.POST.get("pais") or "").strip()
        numero_doc  = (request.POST.get("numero_doc") or "").strip()
        password    = (request.POST.get("password") or "").strip()

        operador.first_name = nombre
        operador.last_name  = apellido
        operador.email      = email or None

        # is_active / estado
        operador.is_active  = (estado == "habilitado")
        if hasattr(operador, "estado"):
            operador.estado = estado

        # extras si existen
        if hasattr(operador, "pais"):
            operador.pais = pais
        if hasattr(operador, "numero_doc"):
            operador.numero_doc = numero_doc

        if password:
            operador.set_password(password)

        operador.save()
        messages.success(request, "Operador actualizado correctamente.")
        return redirect("operadores")

    # GET
    ctx = {
        "operador": operador,
        "usar_operador_model": False,
    }
    return render(request, "editar_operadores.html", ctx)

@login_required
def reportes_view(request):
    context = permisos_context(request.user)
    context.update({"reportes": []})
    return render(request, 'reportes.html', context)


# ============================
# BIENES - LISTA GENERAL
# ============================

@login_required
def lista_bienes(request):
    # Si es operador, redirigir a la vista limitada
    user = request.user
    perms = permisos_context(user)
    if not perms['es_admin']:
        return redirect('lista_bienes_operador')
    # Vista original para admin y otros
    # --------- Parámetros de búsqueda / filtros / orden ----------
    q        = (request.GET.get("q") or "").strip()
    f_origen = request.GET.get("f_origen") or ""
    f_estado = request.GET.get("f_estado") or ""
    f_desde  = request.GET.get("f_desde") or ""
    f_hasta  = request.GET.get("f_hasta") or ""
    orden    = request.GET.get("orden") or "-fecha"

    bienes_queryset = (
        BienPatrimonial.objects
        .select_related("expediente")
        .order_by("clave_unica")
    )

    if q:
        bienes_queryset = bienes_queryset.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(observaciones__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(origen__icontains=q) |
            Q(estado__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente__numero_compra__icontains=q)
        )

    # Filtros
    if f_origen == "__NULL__":
        bienes_queryset = bienes_queryset.filter(origen__isnull=True)
    elif f_origen:
        bienes_queryset = bienes_queryset.filter(origen=f_origen)

    if f_estado == "__NULL__":
        bienes_queryset = bienes_queryset.filter(estado__isnull=True)
    elif f_estado:
        bienes_queryset = bienes_queryset.filter(estado=f_estado)

    if f_desde:
        d = parse_date(f_desde)
        if d:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__gte=d)
    if f_hasta:
        h = parse_date(f_hasta)
        if h:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__lte=h)

    # Orden
    if orden == "fecha":
        bienes_queryset = bienes_queryset.order_by("fecha_adquisicion", "clave_unica")
    elif orden == "-fecha":
        bienes_queryset = bienes_queryset.order_by("-fecha_adquisicion", "clave_unica")
    elif orden == "precio":
        bienes_queryset = bienes_queryset.order_by("valor_adquisicion", "clave_unica")
    elif orden == "-precio":
        bienes_queryset = bienes_queryset.order_by("-valor_adquisicion", "clave_unica")
    else:
        bienes_queryset = bienes_queryset.order_by("clave_unica")

    # Paginación segura (30 por página)
    per_page = 30
    paginator = Paginator(bienes_queryset, per_page)

    # Página solicitada (como int) con fallback a 1
    page_raw = request.GET.get("page", "1")
    try:
        page_number = int(page_raw)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    # Enlaces prev/next SIN provocar excepciones en el template
    try:
        prev_page = page_obj.previous_page_number()
    except Exception:
        prev_page = None
    try:
        next_page = page_obj.next_page_number()
    except Exception:
        next_page = None

    # Range con elipsis (1 … n-2 n-1 n n+1 n+2 … last)
    current = page_obj.number
    last = paginator.num_pages
    window = 2
    nums = set([1, last] + list(range(max(1, current - window), min(last, current + window) + 1)))
    page_range = []
    last_added = 0
    for i in range(1, last + 1):
        if i in nums:
            page_range.append(i)
            last_added = i
        else:
            # insertar elipsis solo una vez entre bloques
            if last_added != "…":
                page_range.append("…")
                last_added = "…"

    # Querystring para mantener filtros en links de paginación
    qs = request.GET.copy()
    qs.pop("page", None)
    querystring = qs.urlencode()

    # --------- Contexto ----------
    context = permisos_context(request.user)
    context.update({
        "q": q,
        "bienes": page_obj.object_list,   # lo que itera la tabla
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "page_range": page_range,
        "prev_page": prev_page,
        "next_page": next_page,
        "querystring": querystring,
    })
    return render(request, "bienes/lista_bienes.html", context)
def lista_bienes_operador(request):
    """Vista limitada para operador: solo puede ver y editar bienes."""
    # Parámetros de búsqueda / filtros / orden
    q        = (request.GET.get("q") or "").strip()
    f_origen = request.GET.get("f_origen") or ""
    f_estado = request.GET.get("f_estado") or ""
    f_desde  = request.GET.get("f_desde") or ""
    f_hasta  = request.GET.get("f_hasta") or ""
    orden    = request.GET.get("orden") or "-fecha"

    bienes_queryset = (
        BienPatrimonial.objects
        .select_related("expediente")
        .order_by("clave_unica")
    )
    if q:
        bienes_queryset = bienes_queryset.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(observaciones__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(origen__icontains=q) |
            Q(estado__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente__numero_compra__icontains=q)
        )
    # Filtros
    if f_origen == "__NULL__":
        bienes_queryset = bienes_queryset.filter(origen__isnull=True)
    elif f_origen:
        bienes_queryset = bienes_queryset.filter(origen=f_origen)
    if f_estado == "__NULL__":
        bienes_queryset = bienes_queryset.filter(estado__isnull=True)
    elif f_estado:
        bienes_queryset = bienes_queryset.filter(estado=f_estado)
    if f_desde:
        d = parse_date(f_desde)
        if d:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__gte=d)
    if f_hasta:
        h = parse_date(f_hasta)
        if h:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__lte=h)
    # Orden
    if orden == "fecha":
        bienes_queryset = bienes_queryset.order_by("fecha_adquisicion", "clave_unica")
    elif orden == "-fecha":
        bienes_queryset = bienes_queryset.order_by("-fecha_adquisicion", "clave_unica")
    elif orden == "precio":
        bienes_queryset = bienes_queryset.order_by("valor_adquisicion", "clave_unica")
    elif orden == "-precio":
        bienes_queryset = bienes_queryset.order_by("-valor_adquisicion", "clave_unica")
    else:
        bienes_queryset = bienes_queryset.order_by("clave_unica")
    # Paginación
    per_page = 30
    paginator = Paginator(bienes_queryset, per_page)
    page_raw = request.GET.get("page", "1")
    try:
        page_number = int(page_raw)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1
    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    # Enlaces prev/next
    try:
        prev_page = page_obj.previous_page_number()
    except Exception:
        prev_page = None
    try:
        next_page = page_obj.next_page_number()
    except Exception:
        next_page = None
    # Range con elipsis
    current = page_obj.number
    last = paginator.num_pages
    window = 2
    nums = set([1, last] + list(range(max(1, current - window), min(last, current + window) + 1)))
    page_range = []
    last_added = 0
    for i in range(1, last + 1):
        if i in nums:
            page_range.append(i)
            last_added = i
        else:
            if last_added != "…":
                page_range.append("…")
                last_added = "…"
    qs = request.GET.copy()
    qs.pop("page", None)
    querystring = qs.urlencode()
    context = permisos_context(request.user)
    context.update({
        "q": q,
        "bienes": page_obj.object_list,
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "page_range": page_range,
        "prev_page": prev_page,
        "next_page": next_page,
        "querystring": querystring,
    })
    return render(request, "bienes/lista_bienes_operador.html", context)
    # --------- Parámetros de búsqueda / filtros / orden ----------
    q        = (request.GET.get("q") or "").strip()
    f_origen = request.GET.get("f_origen") or ""
    f_estado = request.GET.get("f_estado") or ""
    f_desde  = request.GET.get("f_desde") or ""
    f_hasta  = request.GET.get("f_hasta") or ""
    orden    = request.GET.get("orden") or "-fecha"

    # --------- Query base ----------
    bienes_queryset = (
        BienPatrimonial.objects
        .select_related("expediente")
        .order_by("clave_unica")
    )

    if q:
        bienes_queryset = bienes_queryset.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(observaciones__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(origen__icontains=q) |
            Q(estado__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente__numero_compra__icontains=q)
        )

    # Filtros
    if f_origen == "__NULL__":
        bienes_queryset = bienes_queryset.filter(origen__isnull=True)
    elif f_origen:
        bienes_queryset = bienes_queryset.filter(origen=f_origen)

    if f_estado == "__NULL__":
        bienes_queryset = bienes_queryset.filter(estado__isnull=True)
    elif f_estado:
        bienes_queryset = bienes_queryset.filter(estado=f_estado)

    if f_desde:
        d = parse_date(f_desde)
        if d:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__gte=d)
    if f_hasta:
        h = parse_date(f_hasta)
        if h:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__lte=h)

    # Orden
    if orden == "fecha":
        bienes_queryset = bienes_queryset.order_by("fecha_adquisicion", "clave_unica")
    elif orden == "-fecha":
        bienes_queryset = bienes_queryset.order_by("-fecha_adquisicion", "clave_unica")
    elif orden == "precio":
        bienes_queryset = bienes_queryset.order_by("valor_adquisicion", "clave_unica")
    elif orden == "-precio":
        bienes_queryset = bienes_queryset.order_by("-valor_adquisicion", "clave_unica")
    else:
        bienes_queryset = bienes_queryset.order_by("clave_unica")

    # --------- Paginación segura (30 por página) ----------
    per_page = 30
    paginator = Paginator(bienes_queryset, per_page)

    # Página solicitada (como int) con fallback a 1
    page_raw = request.GET.get("page", "1")
    try:
        page_number = int(page_raw)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    # Enlaces prev/next SIN provocar excepciones en el template
    try:
        prev_page = page_obj.previous_page_number()
    except Exception:
        prev_page = None
    try:
        next_page = page_obj.next_page_number()
    except Exception:
        next_page = None

    # Range con elipsis (1 … n-2 n-1 n n+1 n+2 … last)
    current = page_obj.number
    last = paginator.num_pages
    window = 2
    nums = set([1, last] + list(range(max(1, current - window), min(last, current + window) + 1)))
    page_range = []
    last_added = 0
    for i in range(1, last + 1):
        if i in nums:
            page_range.append(i)
            last_added = i
        else:
            # insertar elipsis solo una vez entre bloques
            if last_added != "…":
                page_range.append("…")
                last_added = "…"

    # Querystring para mantener filtros en links de paginación
    qs = request.GET.copy()
    qs.pop("page", None)
    querystring = qs.urlencode()

    # --------- Contexto ----------
    context = permisos_context(request.user)
    context.update({
        "q": q,
        "bienes": page_obj.object_list,   # lo que itera la tabla
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "page_range": page_range,
        "prev_page": prev_page,
        "next_page": next_page,
        "querystring": querystring,
    })
    return render(request, "bienes/lista_bienes.html", context)

# ============================
# CRUD SIMPLE
# ============================

@login_required
def editar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    if request.method == 'POST':
        form = BienPatrimonialForm(request.POST, instance=bien)
        if form.is_valid():
            form.save()
            # Notificación de edición de bien
            Notificacion.objects.create(
                usuario=request.user,
                mensaje=f"Se editó el bien '{bien.nombre}' (Clave: {bien.clave_unica}).",
                leida=False
            )
            messages.success(request, "Bien patrimonial actualizado correctamente.")
            # Redirigir según tipo de usuario
            if hasattr(request.user, 'tipo_usuario') and request.user.tipo_usuario == 'empleado':
                return redirect('lista_bienes_operador')
            return redirect('lista_bienes')
    else:
        form = BienPatrimonialForm(instance=bien)
    context = permisos_context(request.user)
    context.update({'form': form, 'bien': bien})
    return render(request, 'bienes/editar_bien.html', context)


@login_required
def eliminar_bien(request, pk):
    perms = permisos_context(request.user)
    if not perms["puede_eliminar"]:
        messages.error(request, "No tienes permisos para eliminar bienes.")
        return redirect('lista_bienes')

    bien = get_object_or_404(BienPatrimonial, pk=pk)
    # Notificación de baja de bien
    Notificacion.objects.create(
        usuario=request.user,
        mensaje=f"Se dio de baja el bien '{bien.nombre}' (Clave: {bien.clave_unica}).",
        leida=False
    )
    bien.delete()
    messages.success(request, "Bien eliminado correctamente.")
    return redirect('lista_bienes')


# ============================
# CARGA MASIVA
# ============================

@login_required
def carga_masiva_bienes(request):
    if request.method != 'POST':
        context = permisos_context(request.user)
        context.update({'form': CargaMasivaForm()})
        return render(request, 'carga_masiva.html', context)

    form = CargaMasivaForm(request.POST, request.FILES)
    if not form.is_valid():
        context = permisos_context(request.user)
        context.update({'form': form})
        return render(request, 'carga_masiva.html', {'form': form})

    try:
        archivo = request.FILES['archivo_excel']
        sector_form = (form.cleaned_data.get('sector') or '').strip()

        df = pd.read_excel(archivo, dtype=str)
        df.columns = [str(c).strip().lower() for c in df.columns]

        def s(v: object) -> str:
            if v is None:
                return ''
            txt = str(v).strip()
            return '' if txt.lower() == 'nan' else txt

        def get_first(row, names) -> str:
            for n in names:
                if n in df.columns:
                    return s(row.get(n))
            return ''

        def to_int1(v) -> int:
            txt = s(v)
            if not txt:
                return 1
            try:
                val = int(float(txt))
                return max(val, 1)
            except (ValueError, TypeError):
                return 1

        def parse_money(v):
            txt = s(v)
            if not txt:
                return None
            txt = txt.replace('$', '').replace(' ', '')
            if ',' in txt and txt.rfind(',') > txt.rfind('.'):
                txt = txt.replace('.', '').replace(',', '.')
            else:
                txt = txt.replace(',', '')
            try:
                return Decimal(txt)
            except InvalidOperation:
                return None

        def parse_date_any(v):
            txt = s(v)
            if not txt:
                return None
            try:
                dt = pd.to_datetime(txt, errors='coerce', dayfirst=True)
                if pd.isna(dt):
                    return None
                return dt.date()
            except (ValueError, TypeError):
                return None

        def map_origen(v):
            t = s(v).lower()
            if not t:
                return None
            if 'compra' in t or 'minister' in t:
                return 'COMPRA'
            if 'donac' in t:
                return 'DONACION'
            if 'omisi' in t:
                return 'OMISION'
            if 'transfer' in t or 'traslad' in t:
                return 'TRANSFERENCIA'
            return None

        def map_estado(v):
            t = s(v).lower()
            if not t:
                return None
            if 'manten' in t:
                return 'MANTENIMIENTO'
            if 'baja' in t:
                return 'BAJA'
            if 'inac' in t:
                return 'INACTIVO'
            if 'activ' in t:
                return 'ACTIVO'
            return None

        creados, actualizados, errores = 0, 0, []
        from core.models import Expediente

        for i, row in df.iterrows():
            try:
                with transaction.atomic():  # savepoint por fila
                    numero_id   = get_first(row, ['n de id','n_de_id','numero_identificacion','id_patrimonial','nº de id','no de id'])
                    nro_exp     = get_first(row, ['n de expediente','n_de_expediente','numero_expediente','nº de expediente','no de expediente','expediente'])
                    nro_compra  = get_first(row, ['n de compra','n_de_compra','numero_compra','nº de compra','no de compra'])
                    nro_serie   = get_first(row, ['n de serie','n_de_serie','numero_serie','nº de serie','no de serie'])
                    descripcion = get_first(row, ['descripcion','descripción','descripcion_del_bien'])

                    cantidad    = to_int1(get_first(row, ['cantidad']))
                    servicios   = s(get_first(row, ['servicios','sector']) or sector_form) or 'Sin especificar'
                    cuenta_cod  = get_first(row, ['cuenta codigo','cuenta_código','cuenta_codigo'])
                    nomencl     = get_first(row, ['nomenclatura de bienes','nomenclatura_de_bienes','nomenclatura_bienes'])
                    observ      = get_first(row, ['observaciones','obs'])

                    origen_txt  = get_first(row, ['origen'])
                    estado_txt  = get_first(row, ['estado'])
                    precio_raw  = get_first(row, ['precio','valor','importe'])

                    fecha_alta  = parse_date_any(get_first(row, ['fecha de alta','fecha_de_alta','fecha_alta']))
                    fecha_baja  = parse_date_any(get_first(row, ['fecha de baja','fecha_de_baja','fecha_baja']))

                    origen_val = map_origen(origen_txt)   # puede ser None
                    estado_val = map_estado(estado_txt)   # puede ser None

                    precio = parse_money(precio_raw)
                    if origen_val != 'COMPRA':
                        precio = None

                    if not fecha_alta:
                        fecha_alta = date.today()

                    expediente_obj = None
                    if nro_exp:
                        expediente_obj, _ = Expediente.objects.get_or_create(
                            numero_expediente=nro_exp
                        )
                        if nro_compra:
                            expediente_obj.numero_compra = nro_compra
                            expediente_obj.save(update_fields=['numero_compra'])

                    nombre = (descripcion[:200] if descripcion else (nro_serie or 'SIN NOMBRE'))

                    defaults = {
                        'nombre': nombre,
                        'descripcion': descripcion or '',
                        'cantidad': cantidad,
                        'servicios': servicios,
                        'numero_serie': nro_serie,
                        'cuenta_codigo': cuenta_cod,
                        'nomenclatura_bienes': nomencl,
                        'observaciones': observ,
                        'valor_adquisicion': precio,
                        'fecha_adquisicion': fecha_alta,
                        'fecha_baja': fecha_baja,
                        'expediente': expediente_obj,
                    }

                    # Si el mapeo dio None, omitimos la clave para que aplique el default del modelo
                    if origen_val is not None:
                        defaults['origen'] = origen_val
                    if estado_val is not None:
                        defaults['estado'] = estado_val

                    numero_id = (numero_id or '').strip()
                    numero_id_val = numero_id or None  # None (no '')

                    if numero_id_val is not None:
                        _, created = BienPatrimonial.objects.update_or_create(
                            numero_identificacion=numero_id_val,
                            defaults=defaults
                        )
                    elif nro_serie and descripcion:
                        _, created = BienPatrimonial.objects.update_or_create(
                            numero_serie=nro_serie,
                            descripcion=descripcion or '',
                            defaults=defaults
                        )
                    else:
                        BienPatrimonial.objects.create(**defaults)
                        created = True

                    creados += int(created)
                    actualizados += int(not created)

            except (ValueError, ValidationError, IntegrityError) as e:
                errores.append(f"Fila {i + 2}: {e}")

        if creados or actualizados:
            messages.success(request, f'Creados: {creados}, Actualizados: {actualizados}. Errores: {len(errores)}')
        else:
            messages.warning(request, 'No se crearon ni actualizaron bienes.')

        if errores:
            messages.error(request, 'Algunas filas fallaron: ' + ' | '.join(errores[:8]))

        # Notificación de carga masiva
        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Se realizó una carga masiva: {creados} bienes registrados. Errores: {len(errores)}.",
            leida=False
        )

        return redirect('lista_bienes')

    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError) as e:
        messages.error(request, f'Error al procesar el archivo: {e}')
        return redirect('lista_bienes')


# ============================
# ELIMINACIONES MASIVAS
# ============================

@login_required
@require_POST
def eliminar_bienes_seleccionados(request):
    perms = permisos_context(request.user)
    if not perms["puede_eliminar"]:
        messages.error(request, "No tienes permisos para eliminar bienes.")
        return redirect('lista_bienes')

    ids = request.POST.getlist('seleccionados')
    if not ids:
        messages.warning(request, "No seleccionaste bienes para eliminar.")
        return redirect('lista_bienes')

    eliminados = BienPatrimonial.objects.filter(pk__in=ids).delete()[0]
    messages.success(request, f"Eliminados: {eliminados}")
    return redirect('lista_bienes')


# ============================
# BAJAS
# ============================

@login_required
def lista_baja_bienes(request):
    q = (request.GET.get("q") or "").strip()
    orden = request.GET.get("orden") or "-fecha_baja"

    bienes_baja = BienPatrimonial.objects.select_related("expediente").filter(estado="BAJA")

    if q:
        bienes_baja = bienes_baja.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(observaciones__icontains=q) |
            Q(descripcion_baja__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente_baja__icontains=q)
        )

    if orden == "fecha_baja":
        bienes_baja = bienes_baja.order_by("fecha_baja", "clave_unica")
    elif orden == "-fecha_baja":
        bienes_baja = bienes_baja.order_by("-fecha_baja", "clave_unica")
    elif orden == "precio":
        bienes_baja = bienes_baja.order_by("valor_adquisicion", "clave_unica")
    elif orden == "-precio":
        bienes_baja = bienes_baja.order_by("-valor_adquisicion", "clave_unica")
    else:
        bienes_baja = bienes_baja.order_by("-fecha_baja", "clave_unica")

    # ===== Paginación =====
    try:
        per_page = int(request.GET.get("per_page") or 30)
    except ValueError:
        per_page = 30

    paginator = Paginator(bienes_baja, per_page)

    page_str = request.GET.get("page") or "1"
    try:
        page_number = int(page_str)
    except ValueError:
        page_number = 1
    if page_number < 1:
        page_number = 1

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
        page_number = 1

    # Querystring sin page=
    qd = request.GET.copy()
    qd.pop("page", None)
    querystring = qd.urlencode()

    # Rango comprimido (…)
    current = page_obj.number
    total = paginator.num_pages
    window = 2
    page_range = []
    for num in range(1, total + 1):
        if num == 1 or num == total or (current - window) <= num <= (current + window):
            page_range.append(num)
        elif page_range and page_range[-1] != "…":
            page_range.append("…")

    prev_page = current - 1 if page_obj.has_previous() else None
    next_page = current + 1 if page_obj.has_next() else None

    context = permisos_context(request.user)
    context.update({
        "bienes": page_obj.object_list,
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": paginator.num_pages > 1,
        "page_range": page_range,
        "prev_page": prev_page,
        "next_page": next_page,
        "querystring": querystring,
    })
    return render(request, "bienes/lista_baja_bienes.html", context)


@login_required
@require_POST
def dar_baja_bien(request, pk):
    """
    Marca un bien como BAJA sin eliminarlo del listado general.
    Aparece en ambas listas: lista_bienes (con estado 'BAJA') y lista_baja_bienes.
    """
    bien = get_object_or_404(BienPatrimonial, pk=pk)

    fecha_baja = parse_date(request.POST.get("fecha_baja") or "") or date.today()
    expediente_baja = (request.POST.get("expediente_baja") or "").strip()
    descripcion_baja = (request.POST.get("descripcion_baja") or "").strip()

    # Cambiar estado y registrar datos de baja
    bien.estado = "BAJA"
    bien.fecha_baja = fecha_baja
    if hasattr(bien, "expediente_baja"):
        bien.expediente_baja = expediente_baja
    if hasattr(bien, "descripcion_baja"):
        bien.descripcion_baja = descripcion_baja

    bien.save(update_fields=["estado", "fecha_baja", "expediente_baja", "descripcion_baja"])

    messages.success(
        request,
        f"Bien {bien.clave_unica or bien.pk} dado de baja correctamente. Ahora aparece en la lista general con estado BAJA."
    )
    return redirect("lista_bienes")


@login_required
@require_POST
@transaction.atomic
def restablecer_bien(request, pk):
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, "No tienes permisos para restablecer bienes.")
        return redirect("lista_baja_bienes")

    bien = get_object_or_404(BienPatrimonial, pk=pk)

    bien.estado = "ACTIVO"
    if hasattr(bien, "fecha_baja"):
        bien.fecha_baja = None
    if hasattr(bien, "expediente_baja"):
        bien.expediente_baja = None
    if hasattr(bien, "descripcion_baja"):
        bien.descripcion_baja = ""

    update_fields = ["estado"]
    if hasattr(bien, "fecha_baja"):
        update_fields.append("fecha_baja")
    if hasattr(bien, "expediente_baja"):
        update_fields.append("expediente_baja")
    if hasattr(bien, "descripcion_baja"):
        update_fields.append("descripcion_baja")

    bien.save(update_fields=update_fields)
    messages.success(request, f"Bien {bien.clave_unica or bien.pk} restablecido a ACTIVO.")
    return redirect("lista_bienes")


@login_required
@require_POST
@transaction.atomic
def eliminar_bien_definitivo(request, pk):
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, "No tienes permisos para eliminar bienes definitivamente.")
        return redirect("lista_baja_bienes")

    bien = get_object_or_404(BienPatrimonial, pk=pk)
    identificador = bien.clave_unica or bien.pk
    bien.delete()
    messages.success(request, f"Bien {identificador} eliminado definitivamente.")
    return redirect("lista_baja_bienes")


@login_required
def marcar_notificaciones_leidas(request):
    if request.method == "POST":
        Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False}, status=400)


@login_required
@require_POST
def eliminar_notificacion(request, pk):
    """Elimina (o archiva) una notificación del usuario.

    Endpoint pensado para llamadas AJAX desde la UI. Devuelve JSON {ok: True}
    si la operación fue exitosa.
    """
    notif = get_object_or_404(Notificacion, pk=pk)
    # Sólo el propietario o superuser puede eliminar
    if notif.usuario != request.user and not request.user.is_superuser:
        return JsonResponse({"ok": False, "error": "forbidden"}, status=403)
    notif.delete()
    return JsonResponse({"ok": True})


@login_required
@require_POST
def marcar_notificacion_leida(request, pk):
    """Marcar una notificación como leída (llamada AJAX)."""
    notif = get_object_or_404(Notificacion, pk=pk)
    if notif.usuario != request.user and not request.user.is_superuser:
        return JsonResponse({"ok": False, "error": "forbidden"}, status=403)
    notif.leida = True
    notif.save(update_fields=["leida"])
    return JsonResponse({"ok": True})

def crear_notificacion(usuario, mensaje):
    # Crear la notificación
    Notificacion.objects.create(usuario=usuario, mensaje=mensaje)
    # Limitar a 5 notificaciones por usuario, borrar las más antiguas
    notificaciones = Notificacion.objects.filter(usuario=usuario).order_by('-fecha')
    if notificaciones.count() > 5:
        for n in notificaciones[5:]:
            n.delete()

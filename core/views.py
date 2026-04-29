from django.contrib.auth import authenticate, login, logout, get_user_model
import pandas as pd
import hashlib
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CargaMasivaForm, BienPatrimonialForm, OperadorForm
from core.models import BienPatrimonial, ArchivoCargaMasiva
from django.db.models import Q, F
from django.views.decorators.http import require_POST
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_date
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from core.models.notificacion import Notificacion
from core.constants import MAX_NOTIFICACIONES
from django.http import JsonResponse, HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.template.loader import render_to_string
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from xml.sax.saxutils import escape
from core.models import Usuario
 
def _role_route_name(user) -> str:
    """Devuelve el nombre de la ruta según el rol del usuario."""
    if user.is_superuser:
        return "home_admin"
    if hasattr(user, "tipo_usuario"):
        if user.tipo_usuario == "admin":
            return "home_admin"
        elif user.tipo_usuario == "supervisor":
            return "home_supervisor"
        else:
            return "home_operador"
    return "home_operador"
 
 
def permisos_context(user):
    """Booleans útiles para templates y lógica."""
    if not getattr(user, "is_authenticated", False):
        return {
            "es_admin": False,
            "es_supervisor": False,
            "puede_eliminar": False,
            "puede_gestionar_operadores": False,
            "notificaciones": [],
            "notificaciones_count": 0,
        }
 
    if hasattr(user, "tipo_usuario"):
        es_admin = user.tipo_usuario == "admin" or user.is_superuser
        es_supervisor = user.tipo_usuario == "supervisor"
    else:
        es_admin = user.is_superuser
        es_supervisor = False

    notificaciones = list(
        Notificacion.objects
        .filter(usuario=user, eliminada=False)
        .order_by("-fecha")
        [:50]
    )
    notificaciones_count = Notificacion.objects.filter(
        usuario=user, leida=False, eliminada=False
    ).count()

    return {
        "es_admin": es_admin,
        "es_supervisor": es_supervisor,
        "puede_eliminar": es_admin,
        "puede_gestionar_operadores": es_admin,
        "notificaciones": notificaciones,
        "notificaciones_count": notificaciones_count,
    }
# ============================
# AUTENTICACIÓN / INICIO
# ============================

def inicio(request):
    if request.user.is_authenticated:
        return redirect(_role_route_name(request.user))
    return render(request, "inicio.html")
 
 
def login_view(request):
    if request.user.is_authenticated:
        return redirect(_role_route_name(request.user))
 
    next_raw = request.POST.get("next") or request.GET.get("next")
    next_url = next_raw if (next_raw and next_raw != "None") else None
    tipo_default = (request.GET.get("tipo") or "").strip()
 
    if request.method == "POST":
        usuario = request.POST.get("usuario", "").strip()
        contrasena = request.POST.get("contrasena", "")
        tipo_usuario = (request.POST.get("tipo_usuario") or tipo_default or "").strip()
 
        user = authenticate(request, username=usuario, password=contrasena)
 
        def _rerender_error(msg):
            messages.error(request, msg)
            ctx = {
                "login_error": True,
                "usuario_value": usuario,
                "tipo_value": tipo_usuario,
                "tipo_default": tipo_default,
                "next": next_url,
                "request": request,
            }
            return render(request, "login.html", ctx, status=401)
 
        if user is None:
            return _rerender_error("Usuario o contraseña incorrectos")
 
        if not tipo_usuario:
            if getattr(user, "is_superuser", False):
                tipo_usuario = "admin"
            elif hasattr(user, "tipo_usuario") and user.tipo_usuario in ("admin", "operador", "supervisor"):
                tipo_usuario = user.tipo_usuario
            else:
                return _rerender_error("No se pudo determinar el tipo de usuario. Volvé a intentar.")
 
        if tipo_usuario == "admin":
            if user.is_superuser or (hasattr(user, "tipo_usuario") and user.tipo_usuario == "admin"):
                login(request, user)
            else:
                return _rerender_error("El tipo de usuario seleccionado no coincide con el usuario ingresado.")
        elif tipo_usuario == "supervisor":
            if user.is_superuser:
                return _rerender_error("Un administrador no puede ingresar como supervisor.")
            if hasattr(user, "tipo_usuario") and user.tipo_usuario == "supervisor":
                login(request, user)
            else:
                return _rerender_error("El tipo de usuario seleccionado no coincide con el usuario ingresado.")
        elif tipo_usuario == "operador":
            if user.is_superuser:
                return _rerender_error("Un administrador no puede ingresar como operador.")
            if hasattr(user, "tipo_usuario") and user.tipo_usuario == "operador":
                login(request, user)
            else:
                return _rerender_error("El tipo de usuario seleccionado no coincide con el usuario ingresado.")
        else:
            return _rerender_error("Tipo de usuario no válido.")

        # Notificar a admins del inicio de sesión
        tipo_label = {"admin": "Administrador", "supervisor": "Supervisor", "operador": "Operador"}.get(tipo_usuario, tipo_usuario.capitalize())
        crear_notificacion_admins(
            f"{tipo_label} '{user.username}' inició sesión"
        )

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect(_role_route_name(user))

 
    return render(
        request,
        "login.html",
        {
            "next": next_url,
            "tipo_default": tipo_default,
        },
    )
 
 
@login_required
def home_operador(request):
    context = permisos_context(request.user)
    context['logout_on_back'] = True
    return render(request, "home_operador.html", context)
 
 
def registro(request):
    return render(request, "registro.html")
 
 
def bien_confirm_delete(request):
    return render(request, "bien_confirm_delete.html")
 
 
def base(request):
    return render(request, "base.html")
 
 
@login_required
def bienes(request):
    perms = permisos_context(request.user)
    if request.method == "POST":
        form = BienPatrimonialForm(request.POST)
        if form.is_valid():
            bien = form.save()
            nombre_bien = getattr(bien, "nombre", None) or getattr(bien, "descripcion", "Sin nombre")
            crear_notificacion_admins(
                f"Se registró el bien '{nombre_bien}' (Clave: {bien.clave_unica}) correctamente."
            )
            messages.success(request, f"Bien '{nombre_bien}' registrado correctamente.")
            return redirect("bienes")
        # Mensaje de error
        else:
            messages.error(request, "Error al ejecutar la carga")
    else:
        form = BienPatrimonialForm()
 
    context = perms
    context.update({"form": form})
    return render(request, "bienes.html", context)
 
 
def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada exitosamente")
    return redirect("login")
 
 
# ============================
# ÁREA PRIVADA
# ============================
 
@login_required
def home_admin(request):
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("home_operador")
    perms['logout_on_back'] = True
    return render(request, "home_admin.html", perms)


@login_required
def home_supervisor(request):
    perms = permisos_context(request.user)
    if not perms["es_supervisor"]:
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("home_operador")
    return render(request, "home_supervisor.html", perms)



# ============================
# OPERADORES
# ============================
 
Operador = get_user_model()
 
 
@login_required
def operadores(request):
    operadores_qs = Operador.objects.filter(is_staff=False).order_by(
        "first_name", "last_name", "username"
    )
    ctx = {
        "operadores": operadores_qs,
        "usar_operador_model": False,
    }
    ctx.update(permisos_context(request.user))
    return render(request, "operadores.html", ctx)
 
 
def recuperar_password(request):
    if request.method == "POST":
        identificador = (request.POST.get("usuario_o_email") or "").strip()
        if not identificador:
            messages.error(request, "Ingresá tu usuario o email para enviar la solicitud.")
            return render(
                request,
                "recuperar_password.html",
                {"usuario_o_email": identificador},
                status=400,
            )
 
        crear_notificacion_admins(
            f"El operador '{identificador}' solicitó recuperación de contraseña."
        )
        messages.success(request, "Solicitud enviada correctamente.")
        return redirect("recuperar_password")
    return render(request, "recuperar_password.html")
 
 
@login_required
def alta_operadores(request):
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("home_operador")
    if request.method == "POST":
        nombre = " ".join((request.POST.get("nombre") or "").strip().split())
        apellido = " ".join((request.POST.get("apellido") or "").strip().split())
        pais = (request.POST.get("pais") or "").strip()
        dni = (request.POST.get("dni") or "").strip()
        email = (request.POST.get("email") or "").strip()
        estado = (request.POST.get("estado") or "habilitado").strip()
        password = (request.POST.get("password") or "").strip()
 
        form = OperadorForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "alta_operadores.html",
                {"usar_operador_model": False, "form": form},
            )
 
        if not nombre or not apellido:
            messages.error(request, "Debés completar nombre y apellido.")
            return render(
                request,
                "alta_operadores.html",
                {"usar_operador_model": False, "form": form},
            )
 
        numero_doc = form.cleaned_data["dni"]
 
        nombre     = (request.POST.get("nombre") or "").strip()
        apellido   = (request.POST.get("apellido") or "").strip()
        pais       = (request.POST.get("pais") or "").strip()
        numero_doc = (request.POST.get("numero_doc") or "").strip()
        email      = (request.POST.get("email") or "").strip()
        estado     = (request.POST.get("estado") or "habilitado").strip()
        password   = (request.POST.get("password") or "").strip()
 
        # Validación DNI duplicado
        if numero_doc and Usuario.objects.filter(numero_doc=numero_doc).exists():
            messages.error(request, f"Ya existe un operador con el DNI {numero_doc}.")
            return redirect("alta_operadores")
 
        base_username = slugify(f"{nombre}.{apellido}") or (email.split("@")[0] if email else "")
        if not base_username:
            messages.error(request, "No se pudo generar un usuario. Completá Nombre/Apellido o Email.")
            return render(
                request,
                "alta_operadores.html",
                {"usar_operador_model": False, "form": form},
            )
 
        username = base_username
        i = 1
        while Operador.objects.filter(username=username).exists():
            i += 1
            username = f"{base_username}{i}"
 
        is_active = estado == "habilitado"
 
        operador = Operador(
            username=username,
            email=email or None,
            first_name=nombre,
            last_name=apellido,
            is_staff=False,
            is_superuser=False,
            is_active=is_active,
        )
        operador.tipo_usuario = form.cleaned_data["tipo_usuario"]


        if password:
            operador.set_password(password)
        else:
            operador.set_password(username)
 
        if hasattr(operador, "pais"):
            operador.pais = pais
        if hasattr(operador, "numero_doc"):
            operador.numero_doc = numero_doc
        if hasattr(operador, "estado"):
            operador.estado = estado
 
        saved = False
        attempts = 0
        while not saved and attempts < 10:
            try:
                operador.save()
                saved = True
            except IntegrityError:
                attempts += 1
                i += 1
                username = f"{base_username}{i}"
                operador.username = username
 
        if not saved:
            messages.error(
                request,
                "No se pudo crear el usuario debido a un conflicto de nombre. Intentá de nuevo más tarde o con otro nombre.",
            )
            return render(
                request,
                "alta_operadores.html",
                {"usar_operador_model": False, "form": form},
            )
 
        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Se creó el operador '{operador.username}'.",
            leida=False,
        )
 
        messages.success(request, f"Operador {nombre} {apellido} creado. Usuario: {operador.username}")
        return redirect("operadores")
 
    form = OperadorForm(initial={
        'nombre': '',
        'apellido': '',
        'pais': 'Argentina',
        'dni': '',
        'email': '',
        'tipo_usuario': 'operador',
        'estado': 'habilitado',
        'password': '',
    })
    ctx = permisos_context(request.user)
    ctx.update({"usar_operador_model": False, "form": form})
    return render(request, "alta_operadores.html", ctx)
 
@login_required
def editar_operador(request, pk):
    operador = get_object_or_404(Operador, pk=pk, is_staff=False)
 
    if request.method == "POST":
        nombre = " ".join((request.POST.get("nombre") or "").strip().split())
        apellido = " ".join((request.POST.get("apellido") or "").strip().split())
        email = (request.POST.get("email") or "").strip()
        estado = (request.POST.get("estado") or "habilitado").strip()
        pais = (request.POST.get("pais") or "").strip()
        dni = (request.POST.get("dni") or "").strip()
        tipo_usuario = (request.POST.get("tipo_usuario") or "empleado").strip()
        password = (request.POST.get("password") or "").strip()
 
        form = OperadorForm(request.POST, operador_pk=operador.pk)
        if not form.is_valid():
            ctx = permisos_context(request.user)
            ctx.update({"operador": operador, "usar_operador_model": False, "form": form})
            return render(request, "editar_operadores.html", ctx)
 
        numero_doc = form.cleaned_data["dni"]
 
        if not nombre or not apellido:
            messages.error(request, "Debés completar nombre y apellido.")
            ctx = permisos_context(request.user)
            ctx.update({"operador": operador, "usar_operador_model": False, "form": form})
            return render(request, "editar_operadores.html", ctx)
 
        hubo_cambio = False
 
        if operador.first_name != nombre:
            operador.first_name = nombre
            hubo_cambio = True
        else:
            operador.first_name = nombre
 
        if operador.last_name != apellido:
            operador.last_name = apellido
            hubo_cambio = True
        else:
            operador.last_name = apellido
 
        email_normalizado = email or None
        if operador.email != email_normalizado:
            operador.email = email_normalizado
            hubo_cambio = True
        else:
            operador.email = email_normalizado
 
        is_active_nuevo = estado == "habilitado"
        if operador.is_active != is_active_nuevo:
            operador.is_active = is_active_nuevo
            hubo_cambio = True
        else:
            operador.is_active = is_active_nuevo
 
        if hasattr(operador, "estado"):
            if operador.estado != estado:
                operador.estado = estado
                hubo_cambio = True
            else:
                operador.estado = estado
 
        if hasattr(operador, "pais"):
            if operador.pais != pais:
                operador.pais = pais
                hubo_cambio = True
            else:
                operador.pais = pais
 
        if hasattr(operador, "numero_doc"):
            if operador.numero_doc != numero_doc:
                operador.numero_doc = numero_doc
                hubo_cambio = True
            else:
                operador.numero_doc = numero_doc

        if hasattr(operador, "tipo_usuario"):
            if operador.tipo_usuario != tipo_usuario:
                operador.tipo_usuario = tipo_usuario
                hubo_cambio = True
            else:
                operador.tipo_usuario = tipo_usuario


        if password:
            operador.set_password(password)
            hubo_cambio = True
 
        if hubo_cambio:
            operador.save()
            # Mensaje de éxito
            messages.success(request, f"✅ Operador '{operador.username}' actualizado correctamente.", extra_tags='editar')
            try:
                crear_notificacion(request.user, f"Se editó el operador '{operador.username}'.")
            except Exception:
                pass
            messages.success(request, f"Operador '{operador.username}' editado correctamente.")
 
        return redirect("operadores")
 
    form = OperadorForm(initial={
        'nombre': operador.first_name,
        'apellido': operador.last_name,
        'email': operador.email or '',
        'dni': operador.numero_doc or '',
        'pais': getattr(operador, 'pais', '') or '',
        'tipo_usuario': getattr(operador, 'tipo_usuario', 'operador') or 'operador',
        'estado': 'habilitado' if operador.is_active else 'no-habilitado',
    }, operador_pk=operador.pk)
 
    ctx = permisos_context(request.user)
    ctx.update({
        "operador": operador,
        "usar_operador_model": False,
        "form": form,
    })
    return render(request, "editar_operadores.html", ctx)
 
 
@login_required
@require_POST
def eliminar_operador(request, pk):
    perms = permisos_context(request.user)
    if not perms.get("puede_gestionar_operadores", False):
        messages.error(request, "❌ No tienes permisos para eliminar operadores.")
        return redirect("operadores")
 
    operador = get_object_or_404(Operador, pk=pk, is_staff=False)
 
    if operador == request.user:
        messages.error(request, "❌ No podés eliminar tu propio usuario.")
        return redirect("operadores")
 
    identificador = operador.username
    nombre_completo = f"{operador.first_name} {operador.last_name}".strip()
    operador.delete()
 
    try:
        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Se eliminó el operador '{identificador}'.",
            leida=False,
        )
    except Exception:
        pass
 
    messages.success(request, f"Operador '{identificador}' eliminado correctamente.")
    return redirect("operadores")
 
 
@login_required
@require_POST
def dar_baja_operador(request, pk):
    perms = permisos_context(request.user)
    if not perms.get("puede_gestionar_operadores", False):
        messages.error(request, "No tienes permisos para dar de baja operadores.")
        return redirect("operadores")
 
    operador = get_object_or_404(Operador, pk=pk, is_staff=False)
 
    if operador == request.user:
        messages.error(request, "No podés darte de baja a vos mismo.")
        return redirect("operadores")
 
    operador.is_active = False
 
    if hasattr(operador, "estado"):
        try:
            operador.estado = "no-habilitado"
        except Exception:
            pass
 
    operador.save()
 
    try:
        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Se dio de baja al operador '{operador.username}'.",
            leida=False,
        )
    except Exception:
        pass
 
    messages.success(request, f"Operador {operador.username} dado de baja correctamente.")
    return redirect("operadores")
 
 
# ============================
# REPORTES
# ============================
 
@login_required
def reportes_pdf(request):
    scope = (request.GET.get("scope") or "24h").lower()
    now = timezone.now()
 
    if scope == "24h":
        since_dt = now - timedelta(hours=24)
        since_date = since_dt.date()
        bienes = (
            BienPatrimonial.objects
            .select_related("expediente")
            .filter(Q(fecha_adquisicion__gte=since_date) | Q(fecha_baja__gte=since_date))
            .order_by("-fecha_baja", "-fecha_adquisicion", "pk")
        )
        notifs = Notificacion.objects.filter(fecha__gte=since_dt).order_by("-fecha")
        rango_desc = "Últimas 24 horas"
    else:
        bienes = (
            BienPatrimonial.objects
            .select_related("expediente")
            .order_by("-fecha_adquisicion", "pk")
        )
        notifs = Notificacion.objects.none()
        rango_desc = "Todos"
 
    ctx = {
        "bienes": bienes,
        "notifs": notifs,
        "rango_desc": rango_desc,
        "generado_en": now,
        "usuario": request.user,
        **permisos_context(request.user),
    }
 
    try:
        from weasyprint import HTML, CSS
 
        html_str = render_to_string("reportes_pdf.html", ctx, request=request)
        pdf_bytes = HTML(
            string=html_str,
            base_url=request.build_absolute_uri("/"),
        ).write_pdf(
            stylesheets=[
                CSS(
                    string="""
                @page { size: A4; margin: 1.5cm; }
                body { font-family: sans-serif; font-size: 12px; }
                h1,h2,h3 { margin: 0 0 .4rem 0; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 6px; vertical-align: top; }
                thead th { background: #f2f2f2; }
                .muted { color: #666; }
            """
                )
            ]
        )
        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'inline; filename="reporte_{scope}.pdf"'
        return resp
 
    except Exception:
        def money(v):
            if not v:
                return "—"
            return f"${int(round(float(v))):,}".replace(",", ".")
 
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        meta_style = styles["Normal"]
 
        p_cell = ParagraphStyle(
            "p_cell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            wordWrap="CJK",
            spaceAfter=0,
        )
        p_head = ParagraphStyle(
            "p_head",
            parent=p_cell,
            fontName="Helvetica-Bold",
        )
 
        def P(texto, head: bool = False):
            if texto is None or texto == "":
                texto = "—"
            txt = escape(str(texto)).replace("\n", "<br/>")
            return Paragraph(txt, p_head if head else p_cell)
 
        bio = io.BytesIO()
        doc = SimpleDocTemplate(
            bio,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )
        elems = []
 
        title = f"Reporte de Bienes Patrimoniales – {rango_desc}"
        meta = f"Generado: {timezone.localtime(now).strftime('%d/%m/%Y %H:%M')} · Usuario: {request.user.username}"
        elems.append(Paragraph(title, title_style))
        elems.append(Paragraph(meta, meta_style))
        elems.append(Spacer(1, 8))
 
        data = [[
            P("ID", True), P("Clave", True), P("Descripción", True), P("Servicios", True),
            P("Estado", True), P("Alta", True), P("Baja", True), P("Valor", True),
        ]]
 
        for b in bienes:
            estado = b.get_estado_display() if hasattr(b, "get_estado_display") else (b.estado or "—")
            alta = b.fecha_adquisicion.strftime("%d/%m/%Y") if b.fecha_adquisicion else "—"
            baja = b.fecha_baja.strftime("%d/%m/%Y") if b.fecha_baja else "—"
            data.append([
                P(b.pk or ""),
                P(b.clave_unica or "—"),
                P(b.descripcion or "—"),
                P(b.servicios or "—"),
                P(estado),
                P(alta),
                P(baja),
                P(money(b.valor_adquisicion)),
            ])
 
        page_w, _ = A4
        usable_w = page_w - (doc.leftMargin + doc.rightMargin)
        base_col_cm = [1.2, 2.0, 9.0, 2.2, 2.0, 2.0, 2.0, 1.6]
        base_col_pts = [w * cm for w in base_col_cm]
        scale = float(usable_w) / float(sum(base_col_pts))
        col_widths = [w * scale for w in base_col_pts]
 
        table = Table(data, repeatRows=1, colWidths=col_widths)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("ALIGN", (0, 1), (0, -1), "CENTER"),
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
        ])
 
        for i in range(1, len(data)):
            if i % 2 == 0:
                ts.add("BACKGROUND", (0, i), (-1, i), colors.whitesmoke)
 
        table.setStyle(ts)
        elems.append(table)
 
        if notifs:
            elems.append(Spacer(1, 10))
            elems.append(Paragraph("Acciones registradas", styles["Heading3"]))
            notif_data = [[P("Fecha", True), P("Mensaje", True)]]
            for n in notifs:
                notif_data.append([
                    P(timezone.localtime(n.fecha).strftime("%d/%m/%Y %H:%M")),
                    P(n.mensaje),
                ])
            nt_col_w = [3.2 * cm, usable_w - 3.2 * cm]
            nt = Table(notif_data, repeatRows=1, colWidths=nt_col_w)
            nt.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            elems.append(nt)
 
        doc.build(elems)
        pdf_bytes = bio.getvalue()
        bio.close()
 
        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'inline; filename="reporte_{scope}_fallback.pdf"'
        return resp
 
 
@login_required
def reportes_view(request):
    scope = (request.GET.get("scope") or "24h").lower()
    now = timezone.now()
 
    if scope == "24h":
        since_dt = now - timedelta(hours=24)
        since_date = since_dt.date()
        bienes = (
            BienPatrimonial.objects
            .select_related("expediente")
            .filter(
                Q(fecha_adquisicion__gte=since_date) |
                Q(fecha_baja__gte=since_date)
            )
            .order_by("-fecha_baja", "-fecha_adquisicion", "pk")
        )
    else:
        bienes = (
            BienPatrimonial.objects
            .select_related("expediente")
            .order_by("-fecha_adquisicion", "pk")
        )
 
    try:
        per_page = int(request.GET.get("per_page") or 30)
    except ValueError:
        per_page = 30
 
    paginator = Paginator(bienes, per_page)
    page_raw = request.GET.get("page") or "1"
 
    try:
        page_number = int(page_raw)
    except ValueError:
        page_number = 1
 
    if page_number < 1:
        page_number = 1
 
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
 
    try:
        prev_page = page_obj.previous_page_number()
    except Exception:
        prev_page = None
 
    try:
        next_page = page_obj.next_page_number()
    except Exception:
        next_page = None
 
    current = page_obj.number
    total = paginator.num_pages
    window = 2
    page_range = []
 
    for num in range(1, total + 1):
        if num == 1 or num == total or (current - window) <= num <= (current + window):
            page_range.append(num)
        elif page_range and page_range[-1] != "…":
            page_range.append("…")
 
    qd = request.GET.copy()
    qd.pop("page", None)
    querystring = qd.urlencode()
 
    ctx = permisos_context(request.user)
    ctx.update({
        "bienes": page_obj.object_list,
        "scope": scope,
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "page_range": page_range,
        "prev_page": prev_page,
        "next_page": next_page,
        "querystring": querystring,
    })
    return render(request, "reportes.html", ctx)
 
 
# ============================
# HELPERS DE ORDEN
# ============================
 
def _build_ordering(orden_param: str):
    mapping = {
        "-fecha": [F("fecha_adquisicion").desc(nulls_last=True), "pk", "clave_unica"],
        "fecha": [F("fecha_adquisicion").asc(nulls_last=True), "pk", "clave_unica"],
        "-precio": [
            F("valor_adquisicion").desc(nulls_last=True),
            F("fecha_adquisicion").desc(nulls_last=True),
            "pk",
            "clave_unica",
        ],
        "precio": [
            F("valor_adquisicion").asc(nulls_last=True),
            F("fecha_adquisicion").asc(nulls_last=True),
            "pk",
            "clave_unica",
        ],
    }
    return mapping.get(
        orden_param,
        [F("fecha_adquisicion").desc(nulls_last=True), "pk", "clave_unica"],
    )
 
 
def _build_ordering_baja(orden_param: str):
    mapping = {
        "-fecha_baja": [F("fecha_baja").desc(nulls_last=True), "pk", "clave_unica"],
        "fecha_baja": [F("fecha_baja").asc(nulls_last=True), "pk", "clave_unica"],
        "-precio": [
            F("valor_adquisicion").desc(nulls_last=True),
            F("fecha_baja").desc(nulls_last=True),
            "pk",
            "clave_unica",
        ],
        "precio": [
            F("valor_adquisicion").asc(nulls_last=True),
            F("fecha_baja").asc(nulls_last=True),
            "pk",
            "clave_unica",
        ],
    }
    return mapping.get(
        orden_param,
        [F("fecha_baja").desc(nulls_last=True), "pk", "clave_unica"],
    )
 
 
# ============================
# BIENES - LISTA GENERAL
# ============================
 
@login_required
def lista_bienes(request):
    user = request.user
    perms = permisos_context(user)
    if not perms["es_admin"] and not perms["es_supervisor"]:
        return redirect("lista_bienes_operador")
 
    q = (request.GET.get("q") or "").strip()
    f_origen = request.GET.get("f_origen") or ""
    f_estado = request.GET.get("f_estado") or ""
    f_desde = request.GET.get("f_desde") or ""
    f_hasta = request.GET.get("f_hasta") or ""
    orden = request.GET.get("orden") or "-fecha"
 
    bienes_queryset = BienPatrimonial.objects.select_related("expediente")
 
    if q:
        bienes_queryset = bienes_queryset.filter(
            Q(clave_unica__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(observaciones__icontains=q)
            | Q(numero_identificacion__icontains=q)
            | Q(servicios__icontains=q)
            | Q(cuenta_codigo__icontains=q)
            | Q(nomenclatura_bienes__icontains=q)
            | Q(numero_serie__icontains=q)
            | Q(origen__icontains=q)
            | Q(estado__icontains=q)
            | Q(expediente__numero_expediente__icontains=q)
            | Q(expediente__numero_compra__icontains=q)
            | Q(numero_compra__icontains=q)
        )
 
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
 
    bienes_queryset = bienes_queryset.order_by(*_build_ordering(orden))
 
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
 
    try:
        prev_page = page_obj.previous_page_number()
    except Exception:
        prev_page = None
 
    try:
        next_page = page_obj.next_page_number()
    except Exception:
        next_page = None
 
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
    return render(request, "bienes/lista_bienes.html", context)
 
 
@login_required
def lista_bienes_operador(request):
    q = (request.GET.get("q") or "").strip()
    f_origen = request.GET.get("f_origen") or ""
    f_estado = request.GET.get("f_estado") or ""
    f_desde = request.GET.get("f_desde") or ""
    f_hasta = request.GET.get("f_hasta") or ""
    orden = request.GET.get("orden") or "-fecha"
 
    bienes_queryset = BienPatrimonial.objects.select_related("expediente")
 
    if q:
        bienes_queryset = bienes_queryset.filter(
            Q(clave_unica__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(observaciones__icontains=q)
            | Q(numero_identificacion__icontains=q)
            | Q(servicios__icontains=q)
            | Q(cuenta_codigo__icontains=q)
            | Q(nomenclatura_bienes__icontains=q)
            | Q(numero_serie__icontains=q)
            | Q(origen__icontains=q)
            | Q(estado__icontains=q)
            | Q(expediente__numero_expediente__icontains=q)
            | Q(expediente__numero_compra__icontains=q)
            | Q(numero_compra__icontains=q)
        )
 
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
 
    bienes_queryset = bienes_queryset.order_by(*_build_ordering(orden))
 
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
 
    try:
        prev_page = page_obj.previous_page_number()
    except Exception:
        prev_page = None
 
    try:
        next_page = page_obj.next_page_number()
    except Exception:
        next_page = None
 
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
 
 
# ============================
# CRUD SIMPLE
# ============================
 
@login_required
def editar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)
 
    if request.method == "POST":
        form = BienPatrimonialForm(request.POST, instance=bien)
 
        if form.is_valid():
            obj = form.save(commit=False)
 
            fecha_alta_nueva = form.cleaned_data.get("fecha_adquisicion")
            if not fecha_alta_nueva:
                obj.fecha_adquisicion = bien.fecha_adquisicion
 
            estado_nuevo = form.cleaned_data.get("estado") or obj.estado
            if (estado_nuevo or "").upper() == "BAJA":
                if not form.cleaned_data.get("fecha_baja") and not obj.fecha_baja:
                    obj.fecha_baja = date.today()
 
            origen_nuevo = form.cleaned_data.get("origen") or obj.origen
            if (origen_nuevo or "").upper() != "COMPRA":
                obj.valor_adquisicion = None
 
            if not getattr(obj, "nombre", None):
                obj.nombre = (obj.descripcion or obj.numero_serie or "SIN NOMBRE")[:200]
 
            obj.save()
 
            nombre_bien = getattr(obj, "nombre", None) or getattr(obj, "descripcion", "Sin nombre")
            crear_notificacion_admins(
                f"Se editó el bien '{nombre_bien}' (Clave: {obj.clave_unica})."
            )
            messages.success(request, f"Bien '{nombre_bien}' editado correctamente.")
 
            perms = permisos_context(request.user)
            if perms.get("es_admin", False):
                return redirect("lista_bienes")
            return redirect("lista_bienes_operador")
 
        messages.error(request, "Revisá los datos del formulario.")
    else:
        form = BienPatrimonialForm(instance=bien)
 
    context = permisos_context(request.user)
    context.update({"form": form, "bien": bien})
    return render(request, "bienes/editar_bien.html", context)
 
 
@login_required
def eliminar_bien(request, pk):
    perms = permisos_context(request.user)
    if not perms["puede_eliminar"]:
        messages.error(request, "No tienes permisos para eliminar bienes.")
        return redirect("lista_bienes")
 
    bien = get_object_or_404(BienPatrimonial, pk=pk)
    nombre_bien = getattr(bien, "nombre", None) or getattr(bien, "descripcion", "Sin nombre")
    crear_notificacion_admins(
        f"Se dio de baja el bien '{nombre_bien}' (Clave: {bien.clave_unica})."
    )
    messages.success(request, f"Bien '{bien.nombre}' eliminado correctamente.")
    bien.delete()
    # Mensaje de éxito
    messages.success(request, f"✅ Bien '{nombre_bien}' eliminado correctamente.", extra_tags='eliminar')
    return redirect("lista_bienes")


@login_required
def carga_masiva_bienes(request):
    if request.method != "POST":
        context = permisos_context(request.user)
        context.update({"form": CargaMasivaForm()})
        return render(request, "carga_masiva.html", context)

    form = CargaMasivaForm(request.POST, request.FILES)
    if not form.is_valid():
        context = permisos_context(request.user)
        context.update({"form": form})
        return render(request, "carga_masiva.html", {"form": form})

    try:
        archivos = request.FILES.getlist("archivo_excel")
        sector_form = (form.cleaned_data.get("servicio") or "").strip()
        hashes_esta_carga = set()
        hashes_contenido_esta_carga = set()

        creados, actualizados, sin_cambios, duplicados_omitidos, errores = 0, 0, 0, 0, []
        from core.models import Expediente, BienPatrimonial, Notificacion
        import unicodedata
        import os
        from datetime import date
        from decimal import Decimal, InvalidOperation

        def normalizar(texto: str) -> str:
            """Normaliza un nombre de columna: minúsculas, sin acentos, sin caracteres especiales."""
            if not texto: return ""
            texto = str(texto).replace('\u00b0', '').replace('\u00ba', '')  # °, º
            texto = unicodedata.normalize('NFKD', texto)
            texto = ''.join(c for c in texto if not unicodedata.combining(c))
            texto = ''.join(c if c.isalnum() or c == ' ' else ' ' for c in texto)
            return ' '.join(texto.lower().split())

        def s(v: object) -> str:
            """Limpia el valor; devuelve '' si es vacío/nan."""
            if v is None: return ""
            txt = str(v).strip()
            return "" if txt.lower() in ("nan", "none") else txt

        def parse_money(v):
            txt = s(v)
            if not txt: return None
            txt = txt.replace("$", "").replace(" ", "")
            if "," in txt and txt.rfind(",") > txt.rfind("."):
                txt = txt.replace(".", "").replace(",", ".")
            else:
                txt = txt.replace(",", "")
            try:
                return Decimal(txt)
            except InvalidOperation:
                return None

        def parse_date_any(v):
            txt = s(v)
            if not txt: return None
            try:
                dt = pd.to_datetime(txt, errors="coerce", dayfirst=True)
                if pd.isna(dt): return None
                return dt.date()
            except (ValueError, TypeError):
                return None

        def map_origen(v):
            t = s(v).lower()
            if not t: return None
            if "compra" in t or "minister" in t: return "COMPRA"
            if "donac" in t: return "DONACION"
            if "omisi" in t: return "OMISION"
            if "transfer" in t or "traslad" in t: return "TRANSFERENCIA"
            return None

        def map_estado(v):
            t = s(v).lower()
            if not t: return None
            if "manten" in t: return "MANTENIMIENTO"
            if "baja" in t: return "BAJA"
            if "inac" in t: return "INACTIVO"
            if "activ" in t: return "ACTIVO"
            return None

        def hash_archivo_subido(archivo) -> str:
            hasher = hashlib.sha256()
            for chunk in archivo.chunks():
                hasher.update(chunk)
            archivo.seek(0)
            return hasher.hexdigest()

        def hash_contenido_dataframe(df: pd.DataFrame) -> str:
            df_normalizado = df.copy()
            df_normalizado.columns = [normalizar(str(c)) for c in df_normalizado.columns]

            for columna in df_normalizado.columns:
                df_normalizado[columna] = df_normalizado[columna].map(s)

            # Quita filas completamente vacías para no depender de relleno accidental del Excel.
            df_normalizado = df_normalizado.loc[
                ~(df_normalizado.apply(lambda fila: all(not valor for valor in fila), axis=1))
            ].reset_index(drop=True)

            columnas_ordenadas = sorted(df_normalizado.columns)
            registros = []
            for _, row in df_normalizado[columnas_ordenadas].iterrows():
                registros.append("||".join(row[col] for col in columnas_ordenadas))

            contenido_canonico = "\n".join(
                [f"cols:{'||'.join(columnas_ordenadas)}", *registros]
            )
            return hashlib.sha256(contenido_canonico.encode("utf-8")).hexdigest()

        def clave_fila_canonica(numero_id_val, nro_serie, descripcion, cuenta_cod, nomencl, servicios):
            if numero_id_val:
                return f"id:{normalizar(numero_id_val)}"
            if nro_serie != "NO" and descripcion:
                return f"serie_desc:{normalizar(nro_serie)}|{normalizar(descripcion)}"
            partes = [
                normalizar(descripcion or ""),
                normalizar(nro_serie if nro_serie != "NO" else ""),
                normalizar(cuenta_cod if cuenta_cod != "NO" else ""),
                normalizar(nomencl if nomencl != "NO" else ""),
                normalizar(servicios if servicios != "NO" else ""),
            ]
            return f"fila:{'|'.join(partes)}"

        def valores_distintos(valor_actual, valor_nuevo):
            if hasattr(valor_actual, "pk") or hasattr(valor_nuevo, "pk"):
                actual_pk = getattr(valor_actual, "pk", None) if valor_actual else None
                nuevo_pk = getattr(valor_nuevo, "pk", None) if valor_nuevo else None
                return actual_pk != nuevo_pk
            return valor_actual != valor_nuevo

        claves_filas_esta_carga = set()

        for archivo in archivos:
            nombre_archivo_completo = getattr(archivo, 'name', 'Archivo')
            try:
                hash_archivo = hash_archivo_subido(archivo)

                nombre_archivo_lower = nombre_archivo_completo.lower()
                
                # Nombre del servicio basado en el archivo
                servicio_archivo = os.path.splitext(nombre_archivo_completo)[0].upper()
                if sector_form:
                    servicio_archivo = f"{sector_form} - {servicio_archivo}"

                if nombre_archivo_lower.endswith('.xls') or nombre_archivo_lower.endswith('.xlt'):
                    engine = 'xlrd'
                elif nombre_archivo_lower.endswith('.xlsb'):
                    engine = 'pyxlsb'
                elif nombre_archivo_lower.endswith(('.ods', '.odf', '.odt')):
                    engine = 'odf'
                else:
                    engine = 'openpyxl'

                try:
                    df = pd.read_excel(archivo, dtype=str, engine=engine)
                except Exception:
                    df = pd.read_excel(archivo, dtype=str)

                # Detección de cabeceras
                df.columns = [normalizar(str(c)) for c in df.columns]
                keywords = ["descripcion", "cantidad", "expediente", "compra", "clave", "id", "serie", "nomenclatura"]
                cols_combined = " ".join(df.columns)
                
                if sum(1 for k in keywords if k in cols_combined) < 2:
                    header_found = False
                    for idx, row in df.head(25).iterrows():
                        row_values = [normalizar(str(v)) for v in row.values if v and str(v).lower() != 'nan']
                        row_combined = " ".join(row_values)
                        if sum(1 for k in keywords if k in row_combined) >= 2:
                            new_cols = []
                            for i, val in enumerate(row.values):
                                val_str = normalizar(str(val)) if val and str(val).lower() != 'nan' else f"columna_{i}"
                                new_cols.append(val_str)
                            df.columns = new_cols
                            df = df.iloc[idx+1:].reset_index(drop=True)
                            header_found = True
                            break
                    if not header_found:
                        errores.append(f"No se detectaron cabeceras válidas en '{nombre_archivo_completo}'")
                        continue

                hash_contenido = hash_contenido_dataframe(df)
                if (
                    hash_archivo in hashes_esta_carga
                    or hash_contenido in hashes_contenido_esta_carga
                    or ArchivoCargaMasiva.objects.filter(hash_archivo=hash_archivo).exists()
                    or ArchivoCargaMasiva.objects.filter(hash_contenido=hash_contenido).exists()
                ):
                    errores.append(f"Excel ya cargado: '{nombre_archivo_completo}'")
                    continue

                # Helpers de búsqueda de columnas (definidos por archivo porque dependen de df.columns)
                def get_first(row_data, names):
                    # 1. Match exacto
                    for n in names:
                        key = normalizar(n)
                        if key in df.columns:
                            return s(row_data.get(key))
                    # 2. Match difuso
                    for n in names:
                        key = normalizar(n)
                        if len(key) < 3: continue
                        for col in df.columns:
                            if key in col:
                                return s(row_data.get(col))
                    return ""

                def get_first_no(row_data, names):
                    val = get_first(row_data, names)
                    return val if val else "NO"

                def to_int1(v):
                    txt = s(v)
                    if not txt: return 1
                    try:
                        return max(int(float(txt)), 1)
                    except (ValueError, TypeError):
                        return 1

                # Procesamiento de filas
                errores_previos = len(errores)
                for i, row in df.iterrows():
                    try:
                        with transaction.atomic():
                            numero_id = get_first(row, ["n id", "numero identificacion", "id patrimonial", "id", "identificacion"])
                            nro_exp = get_first(row, ["n expediente", "numero expediente", "expediente", "exp", "nro exp"])
                            nro_compra = get_first(row, ["n compra", "numero compra", "compra", "nro compra", "orden de compra", "oc"])
                            nro_serie = get_first_no(row, ["n serie", "numero serie", "serie", "nro serie"])
                            descripcion = get_first(row, ["descripcion", "descripción", "detalle", "nombre", "bien"])
                            cuenta_cod = get_first_no(row, ["cuenta codigo", "cuenta", "cod cuenta"])
                            nomencl = get_first_no(row, ["nomenclatura", "nomenclatura bienes", "cod nomenclatura"])
                            observ = get_first_no(row, ["observaciones", "obs", "comentarios"])
                            origen_txt = get_first(row, ["origen"])
                            estado_txt = get_first(row, ["estado"])
                            precio_raw = get_first(row, ["precio", "valor", "importe", "costo", "valor adquisicion"])
                            cantidad = to_int1(get_first(row, ["cantidad"]))
                            
                            serv_raw = s(get_first(row, ["servicios", "servicio", "sector"]) or servicio_archivo)
                            servicios = serv_raw if serv_raw else "NO"

                            fecha_alta = parse_date_any(get_first(row, ["fecha alta", "fecha de alta"])) or date.today()
                            fecha_baja = parse_date_any(get_first(row, ["fecha de baja"]))
                            
                            origen_val = map_origen(origen_txt)
                            estado_val = map_estado(estado_txt)
                            precio = parse_money(precio_raw) if origen_val == "COMPRA" else None

                            expediente_obj = None
                            if nro_exp and nro_exp.upper() != "NO":
                                expediente_obj, _ = Expediente.objects.get_or_create(numero_expediente=nro_exp)
                                if nro_compra and nro_compra.upper() != "NO":
                                    expediente_obj.numero_compra = nro_compra
                                    expediente_obj.save(update_fields=["numero_compra"])

                            nombre_bien = descripcion[:200] if descripcion else (nro_serie if nro_serie != "NO" else "SIN NOMBRE")
                            numero_id_val = (numero_id or "").strip() or None

                            defaults = {
                                "nombre": nombre_bien,
                                "descripcion": descripcion or "NO",
                                "cantidad": cantidad,
                                "servicios": servicios,
                                "numero_serie": nro_serie,
                                "numero_identificacion": numero_id_val,
                                "cuenta_codigo": cuenta_cod,
                                "nomenclatura_bienes": nomencl,
                                "observaciones": observ,
                                "valor_adquisicion": precio,
                                "fecha_adquisicion": fecha_alta,
                                "fecha_baja": fecha_baja,
                                "expediente": expediente_obj,
                                "numero_compra": nro_compra if nro_compra and nro_compra.upper() != "NO" else "",
                            }
                            if origen_val: defaults["origen"] = origen_val
                            if estado_val: defaults["estado"] = estado_val

                            clave_fila = clave_fila_canonica(
                                numero_id_val,
                                nro_serie,
                                descripcion,
                                cuenta_cod,
                                nomencl,
                                servicios,
                            )
                            if clave_fila in claves_filas_esta_carga:
                                duplicados_omitidos += 1
                                continue

                            bien_existente = None
                            if numero_id_val:
                                bien_existente = BienPatrimonial.objects.filter(
                                    numero_identificacion=numero_id_val
                                ).first()
                            elif nro_serie != "NO" and descripcion:
                                bien_existente = BienPatrimonial.objects.filter(
                                    numero_serie=nro_serie,
                                    descripcion=descripcion,
                                ).first()

                            if bien_existente is None:
                                BienPatrimonial.objects.create(**defaults)
                                creados += 1
                            else:
                                campos_a_actualizar = []
                                for campo, valor_nuevo in defaults.items():
                                    if valores_distintos(getattr(bien_existente, campo), valor_nuevo):
                                        setattr(bien_existente, campo, valor_nuevo)
                                        campos_a_actualizar.append(campo)

                                if campos_a_actualizar:
                                    bien_existente.save(update_fields=campos_a_actualizar)
                                    actualizados += 1
                                else:
                                    sin_cambios += 1

                            claves_filas_esta_carga.add(clave_fila)
                    except Exception as e:
                        errores.append(f"Error en {nombre_archivo_completo} (fila {i+1}): {str(e)}")
                if len(errores) == errores_previos:
                    ArchivoCargaMasiva.objects.create(
                        nombre_archivo=nombre_archivo_completo,
                        hash_archivo=hash_archivo,
                        hash_contenido=hash_contenido,
                        usuario=request.user,
                    )
                    hashes_esta_carga.add(hash_archivo)
                    hashes_contenido_esta_carga.add(hash_contenido)
            except Exception as e:
                errores.append(f"Error crítico procesando '{nombre_archivo_completo}': {str(e)}")

        if creados or actualizados:
            messages.success(
                request,
                f"✅ Creados: {creados}, Actualizados: {actualizados}, Sin cambios: {sin_cambios}, Duplicados omitidos: {duplicados_omitidos}. Archivos: {len(archivos)}. Errores: {len(errores)}"
            )
        else:
            messages.warning(
                request,
                f"No se procesaron registros nuevos. Sin cambios: {sin_cambios}. Duplicados omitidos: {duplicados_omitidos}."
            )
        
        if errores:
            messages.error(request, "Resumen de errores: " + " | ".join(errores[:5]))

        Notificacion.objects.create(
            usuario=request.user,
            mensaje=f"Carga masiva finalizada: {creados} nuevos, {actualizados} actualizados, {sin_cambios} sin cambios, {duplicados_omitidos} duplicados omitidos. {len(errores)} errores.",
            leida=False
        )
        return redirect("lista_bienes")

    except Exception as e:
        messages.error(request, f"Error general en la carga: {str(e)}")
        return redirect("lista_bienes")
 
 
# ============================
# ELIMINACIONES MASIVAS
# ============================
 
@login_required
@require_POST
def eliminar_bienes_seleccionados(request):
    perms = permisos_context(request.user)
    if not perms["puede_eliminar"]:
        messages.error(request, "No tienes permisos para eliminar bienes.")
        return redirect("lista_bienes")
 
    ids = request.POST.getlist("seleccionados")
    if not ids:
        messages.warning(request, "No seleccionaste bienes para eliminar.")
        return redirect("lista_bienes")
 
    eliminados = BienPatrimonial.objects.filter(pk__in=ids).delete()[0]
    messages.success(request, f"✅ Eliminados: {eliminados} bienes correctamente.")
    return redirect("lista_bienes")
 
 
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
            Q(clave_unica__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(observaciones__icontains=q)
            | Q(descripcion_baja__icontains=q)
            | Q(numero_identificacion__icontains=q)
            | Q(servicios__icontains=q)
            | Q(cuenta_codigo__icontains=q)
            | Q(nomenclatura_bienes__icontains=q)
            | Q(numero_serie__icontains=q)
            | Q(expediente__numero_expediente__icontains=q)
            | Q(expediente__numero_compra__icontains=q)
            | Q(numero_compra__icontains=q)
            | Q(expediente_baja__icontains=q)
        )
 
    bienes_baja = bienes_baja.order_by(*_build_ordering_baja(orden))
 
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
 
    qd = request.GET.copy()
    qd.pop("page", None)
    querystring = qd.urlencode()
 
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
    bien = get_object_or_404(BienPatrimonial, pk=pk)
 
    fecha_baja = parse_date(request.POST.get("fecha_baja") or "") or date.today()
    expediente_baja = (request.POST.get("expediente_baja") or "").strip()
    descripcion_baja = (request.POST.get("descripcion_baja") or "").strip()
 
    bien.estado = "BAJA"
    update_fields = ["estado"]
 
    if hasattr(bien, "fecha_baja"):
        bien.fecha_baja = fecha_baja
        update_fields.append("fecha_baja")
    if hasattr(bien, "expediente_baja"):
        bien.expediente_baja = expediente_baja
        update_fields.append("expediente_baja")
    if hasattr(bien, "descripcion_baja"):
        bien.descripcion_baja = descripcion_baja
        update_fields.append("descripcion_baja")
 
    bien.save(update_fields=update_fields)
    nombre_bien = getattr(bien, "nombre", None) or getattr(bien, "descripcion", "Sin nombre")
    crear_notificacion_admins(
        f"Se dio de baja el bien '{nombre_bien}' (Clave: {bien.clave_unica})."
    )
    messages.success(request, f"Bien '{bien.nombre}' dado de baja correctamente.")
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
    nombre_bien = getattr(bien, "nombre", None) or getattr(bien, "descripcion", "Sin nombre")
    crear_notificacion_admins(
        f"Se restableció el bien '{nombre_bien}' (Clave: {bien.clave_unica}) a ACTIVO."
    )
    messages.success(request, f"Bien '{bien.nombre}' restablecido a ACTIVO.")
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
    nombre_bien = getattr(bien, "nombre", None) or getattr(bien, "descripcion", "Sin nombre")
    bien.delete()
    crear_notificacion_admins(
        f"Se eliminó definitivamente el bien '{nombre_bien}' (Clave: {identificador})."
    )
    messages.success(request, f"Bien '{nombre_bien}' eliminado definitivamente.")
    return redirect("lista_baja_bienes")
 
 
# ============================
# NOTIFICACIONES
# ============================
 
@login_required
def marcar_notificaciones_leidas(request):
    if request.method == "POST":
        Notificacion.objects.filter(
            usuario=request.user,
            leida=False,
            eliminada=False
        ).update(leida=True)
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False}, status=400)


@login_required
@require_POST
def borrar_todas_notificaciones(request):
    if request.method == "POST":
        Notificacion.objects.filter(
            usuario=request.user,
            eliminada=False
        ).update(eliminada=True)
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False}, status=400)


@login_required
@require_POST
def eliminar_notificacion(request, pk):
    notif = get_object_or_404(Notificacion, pk=pk)

    if notif.usuario != request.user and not request.user.is_superuser:
        return JsonResponse({"ok": False, "error": "forbidden"}, status=403)

    # 🔥 NO se elimina → se oculta
    notif.eliminada = True
    notif.save(update_fields=["eliminada"])

    return JsonResponse({"ok": True})


@login_required
@require_POST
def marcar_notificacion_leida(request, pk):
    notif = get_object_or_404(Notificacion, pk=pk)

    if notif.usuario != request.user and not request.user.is_superuser:
        return JsonResponse({"ok": False, "error": "forbidden"}, status=403)

    notif.leida = True
    notif.save(update_fields=["leida"])

    return JsonResponse({"ok": True})


def crear_notificacion(usuario, mensaje):
    Notificacion.objects.create(usuario=usuario, mensaje=mensaje)

    notificaciones = Notificacion.objects.filter(usuario=usuario).order_by("-fecha")
    if notificaciones.count() > MAX_NOTIFICACIONES:
        for n in notificaciones[MAX_NOTIFICACIONES:]:
            n.delete()

# ---------------------------
# 💡 Vista: Recuperar contraseña
# ---------------------------

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q


def recuperar_password(request):
    if request.method == "POST":
        # Acá podrías enviar el correo o guardar el pedido en la base
        messages.success(request, "✅ Solicitud enviada correctamente.")
        return redirect('recuperar_password')

    return render(request, 'recuperar_password.html')



def crear_notificacion_admins(mensaje):
    UserModel = get_user_model()
    admins = UserModel.objects.filter(
        Q(is_superuser=True) | Q(tipo_usuario="admin")
    ).distinct()

    for admin in admins:
        crear_notificacion(admin, mensaje)

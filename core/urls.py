from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # ===== Raíz del sitio =====
    
    path('', RedirectView.as_view(pattern_name='inicio', permanent=False)),

    # ===== Inicio / Auth =====
    path('inicio/', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    # Compatibilidad con /accounts/login/
    path('accounts/login/', RedirectView.as_view(pattern_name='login', permanent=False)),

    # ===== Dashboards =====
    path('home_admin/', views.home_admin, name='home_admin'),
    path('home_operador/', views.home_operador, name='home_operador'),

    # ===== Operadores =====
    path('operadores/', views.operadores, name='operadores'),
    path('alta_operadores/', views.alta_operadores, name='alta_operadores'),  # <-- nombre corregido

    # ===== Varias =====
    path('base/', views.base, name='base'),
    path('reportes/', views.reportes_view, name='reportes'),

    # ===== Bienes =====
    # Acciones específicas primero
    path('bienes/<int:pk>/editar/', views.editar_bien, name='editar_bien'),
    path('bienes/<int:pk>/eliminar/', views.eliminar_bien, name='eliminar_bien'),
    path('bienes/eliminar-seleccionados/', views.eliminar_bienes_seleccionados, name='eliminar_bienes_seleccionados'),

    # Listas
    path('lista-bienes/', views.lista_bienes, name='lista_bienes'),
    path('bienes/bajas/', views.lista_baja_bienes, name='lista_baja_bienes'),

    # Acciones sobre bajas
    path('bienes/<int:pk>/dar-baja/', views.dar_baja_bien, name='dar_baja_bien'),
    path('bienes/<int:pk>/restablecer/', views.restablecer_bien, name='restablecer_bien'),
    path('bienes/<int:pk>/eliminar-definitivo/', views.eliminar_bien_definitivo, name='eliminar_bien_definitivo'),

    # Carga masiva
    path('carga-masiva/', views.carga_masiva_bienes, name='carga_masiva'),

    # Vistas legacy / formularios simples
    path('bienes/', views.bienes, name='bienes'),
    path('bien_confirm_delete/', views.bien_confirm_delete, name='bien_confirm_delete'),
]

// notificaciones.js
document.addEventListener('DOMContentLoaded', function() {
    // Datos de ejemplo de notificaciones
    const notificaciones = [
        {
            id: 1,
            titulo: "Solicitud de Recuperación de Contraseña",
            descripcion: "El Usuario Juan Pérez ha solicitado recuperar su contraseña en el Sistema",
            fecha: "15/03/2024 14:30",
            leida: false,
            tipo: "recuperacion"
        },
        {
            id: 2,
            titulo: "Nueva Solicitud de Alta",
            descripcion: "Se ha recibido una nueva solicitud de alta de usuario para el departamento de Sistemas",
            fecha: "14/03/2024 10:15",
            leida: false,
            tipo: "alta"
        },
        {
            id: 3,
            titulo: "Actualización del Sistema",
            descripcion: "El sistema se actualizará el próximo sábado de 20:00 a 22:00 horas",
            fecha: "13/03/2024 09:00",
            leida: true,
            tipo: "sistema"
        },
        {
            id: 4,
            titulo: "Backup Completado",
            descripcion: "El proceso de backup se ha completado exitosamente",
            fecha: "12/03/2024 23:45",
            leida: true,
            tipo: "sistema"
        }
    ];

    // Elementos del DOM: seleccionar el wrapper por id si existe (no modificar alineación)
    const wrapperNotificaciones = document.getElementById('notificacionesBell') || document.querySelector('.notificaciones-wrapper');
    let badgeNotificaciones = null;

    // Inicializar sistema de notificaciones
    function inicializarNotificaciones() {
        if (!wrapperNotificaciones) return;

        // Buscar si ya existe una badge (renderizada por servidor)
        badgeNotificaciones = wrapperNotificaciones.querySelector('.notificaciones-badge');
        if (!badgeNotificaciones) {
            badgeNotificaciones = document.createElement('span');
            badgeNotificaciones.className = 'notificaciones-badge';
            // Insertar la badge después del icono para mantener el flujo
            wrapperNotificaciones.appendChild(badgeNotificaciones);
        }
        actualizarBadge();
        // Agregar event listener al wrapper (el click abre el panel/modal)
        wrapperNotificaciones.addEventListener('click', mostrarNotificaciones);

        // Si existe dropdown server-renderizado, agregar delegación para eliminar desde el dropdown
        const dropdown = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
        if (dropdown) {
            // delegación para eliminar notificaciones desde el dropdown
            dropdown.addEventListener('click', function(ev) {
                const btn = ev.target.closest('.btn-eliminar-notificacion');
                if (!btn) return;
                ev.stopPropagation();
                const id = btn.getAttribute('data-id');
                const li = btn.closest('.dropdown-notif-item');
                const badge = wrapperNotificaciones.querySelector('.notificaciones-badge');
                fetch(`/notificaciones/${id}/eliminar/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') || ''
                    },
                    body: '{}'
                }).then(function(resp) {
                    if (resp.ok) {
                        if (li && li.parentNode) li.parentNode.removeChild(li);
                        if (badge) {
                            try {
                                var cur = parseInt(badge.textContent) || 0;
                                cur = Math.max(0, cur - 1);
                                if (cur <= 0) {
                                    badge.style.display = 'none';
                                } else {
                                    badge.textContent = cur;
                                }
                            } catch (e) {
                                // noop
                            }
                        }
                    } else {
                        alert('No se pudo eliminar la notificación.');
                    }
                }).catch(function() {
                    alert('No se pudo conectar con el servidor.');
                });
            });
        }

        // Cerrar dropdown al clickear fuera
        document.addEventListener('click', function(ev) {
            const dd = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
            if (!dd) return;
            if (!wrapperNotificaciones.contains(ev.target)) {
                dd.style.display = 'none';
            }
        });
    }

    // Actualizar badge con número de notificaciones no leídas
    function actualizarBadge() {
    if (!badgeNotificaciones) return;
    // Preferir calcular desde el DOM (dropdown server-rendered) si está presente
    const dropdown = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
    let noLeidas = 0;
    if (dropdown) {
        // contar LI con data-leida="0" o con clase notificacion-no-leida
        const items = dropdown.querySelectorAll('.dropdown-notif-item');
        items.forEach(it => {
            const dl = it.getAttribute('data-leida');
            if (dl === null) {
                if (it.classList.contains('notificacion-no-leida')) noLeidas++;
            } else if (dl === '0') {
                noLeidas++;
            }
        });
    } else {
        // Fallback: usar array cliente
        noLeidas = notificaciones.filter(notif => !notif.leida).length;
    }

    badgeNotificaciones.textContent = noLeidas;
    badgeNotificaciones.style.opacity = noLeidas > 0 ? '1' : '0';
    badgeNotificaciones.style.transform = noLeidas > 0 ? 'scale(1)' : 'scale(0.6)';
    badgeNotificaciones.style.display = noLeidas > 0 ? 'flex' : 'none';
    }

    // Mostrar notificaciones: si existe dropdown (server-rendered) lo toggleamos,
    // sino creamos el modal (client-side).
    function mostrarNotificaciones(e) {
        if (e && e.stopPropagation) e.stopPropagation();
        const dropdown = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
        if (dropdown) {
            // Toggle dropdown visibility
            const isVisible = dropdown.style.display === 'block';
            dropdown.style.display = isVisible ? 'none' : 'block';

            // Si abrimos el dropdown y hay badge > 0, marcar leídas en backend y ocultar badge
            if (!isVisible) {
                const badge = wrapperNotificaciones.querySelector('.notificaciones-badge');
                if (badge && parseInt(badge.textContent) > 0) {
                    fetch('/notificaciones/leidas/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') || ''
                        },
                        body: '{}'
                    }).then(function(resp) {
                        if (resp.ok) {
                            if (badge) badge.style.display = 'none';
                        }
                    }).catch(function() {
                        // ignore network errors for read-mark
                    });
                }
            }

            return;
        }

        // Si no hay dropdown, creamos el modal (el comportamiento anterior)
        const modal = document.createElement('div');
        modal.className = 'notificaciones-modal';
        modal.style.display = 'flex';

        modal.innerHTML = `
            <div class="notificaciones-contenido">
                <div class="notificaciones-header">
                    <h2>Notificaciones</h2>
                    <button class="btn-cerrar-notificaciones">&times;</button>
                </div>
                <div class="notificaciones-body">
                    ${generarListaNotificaciones()}
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Event listeners del modal
        const btnCerrar = modal.querySelector('.btn-cerrar-notificaciones');
        btnCerrar.addEventListener('click', function() {
            cerrarModal(modal);
        });

        modal.addEventListener('click', function(ev) {
            if (ev.target === modal) {
                cerrarModal(modal);
            }
        });

        // Agregar event listeners a los botones de acción
        agregarEventListenersNotificaciones(modal);
    }

    // Generar HTML de la lista de notificaciones
    function generarListaNotificaciones() {
        if (notificaciones.length === 0) {
            return `
                <div class="sin-notificaciones">
                    <i class="fa-solid fa-bell-slash"></i>
                    <p>No hay notificaciones</p>
                </div>
            `;
        }

        return notificaciones.map(notificacion => `
            <div class="notificacion-item ${notificacion.leida ? '' : 'notificacion-no-leida'}">
                <div class="notificacion-titulo">${notificacion.titulo}</div>
                <div class="notificacion-descripcion">${notificacion.descripcion}</div>
                <div class="separador-notificacion"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; gap:10px;">
                    <div class="notificacion-fecha">Fecha: ${notificacion.fecha}</div>
                    <div class="notificacion-acciones">
                        ${!notificacion.leida ? `
                            <button class="btn-accion-notificacion btn-marcar-leido" data-id="${notificacion.id}">
                                Marcar como leído
                            </button>
                        ` : ''}
                        ${notificacion.tipo === 'recuperacion' ? `
                            <button class="btn-accion-notificacion btn-aceptar" data-id="${notificacion.id}">
                                Aceptar
                            </button>
                            <button class="btn-accion-notificacion btn-rechazar" data-id="${notificacion.id}">
                                Rechazar
                            </button>
                        ` : ''}
                        <!-- Botón eliminar (tachito) -->
                        <button class="btn-eliminar-notificacion" data-id="${notificacion.id}" title="Eliminar">
                            <i class="fa fa-trash" aria-hidden="true"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Agregar event listeners a los botones de las notificaciones
    function agregarEventListenersNotificaciones(modal) {
        // Botones marcar como leído
        modal.querySelectorAll('.btn-marcar-leido').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                marcarComoLeido(id);
                cerrarModal(modal);
            });
        });

        // Botones eliminar notificación (tachito)
        modal.querySelectorAll('.btn-eliminar-notificacion').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                const id = this.getAttribute('data-id');
                eliminarNotificacion(id, this.closest('.notificacion-item'));
            });
        });

        // Botones aceptar
        modal.querySelectorAll('.btn-aceptar').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                manejarAceptar(id);
                cerrarModal(modal);
            });
        });

        // Botones rechazar
        modal.querySelectorAll('.btn-rechazar').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                manejarRechazar(id);
                cerrarModal(modal);
            });
        });
    }

    // Eliminar notificación (frontend demo): remueve del array, del DOM y actualiza badge
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function eliminarNotificacion(id, element) {
        // Llamada al backend para persistir la eliminación
        fetch(`/notificaciones/${id}/eliminar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: '{}'
        }).then(resp => {
            if (resp.ok) {
                const idx = notificaciones.findIndex(n => n.id == id);
                if (idx !== -1) notificaciones.splice(idx, 1);
                if (element && element.parentNode) element.parentNode.removeChild(element);
                actualizarBadge();
                mostrarMensaje('Notificación eliminada', 'info');
            } else {
                mostrarMensaje('No se pudo eliminar la notificación en el servidor', 'error');
            }
        }).catch(err => {
            console.error(err);
            mostrarMensaje('Error de red al eliminar notificación', 'error');
        });
    }

    // Funciones de manejo de notificaciones
    function marcarComoLeido(id) {
        // Intentar marcar en backend primero (si existe), luego actualizar UI
        fetch(`/notificaciones/${id}/marcar-leida/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: '{}'
        }).then(resp => {
            if (resp.ok) {
                // Actualizar array cliente si aplica
                const notificacion = notificaciones.find(notif => notif.id == id);
                if (notificacion) notificacion.leida = true;

                // Si hay dropdown renderizado, actualizar atributo/data y clases
                const dropdown = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
                if (dropdown) {
                    const li = dropdown.querySelector(`.dropdown-notif-item[data-id="${id}"]`);
                    if (li) {
                        li.setAttribute('data-leida', '1');
                        li.classList.remove('notificacion-no-leida');
                    }
                }

                actualizarBadge();
                mostrarMensaje('Notificación marcada como leída', 'success');
            } else {
                mostrarMensaje('No se pudo marcar la notificación como leída', 'error');
            }
        }).catch(err => {
            console.error(err);
            mostrarMensaje('Error de red al marcar notificación', 'error');
        });
    }

    function manejarAceptar(id) {
        const notificacion = notificaciones.find(notif => notif.id == id);
        if (notificacion) {
            // Aquí iría la lógica para aceptar la solicitud
            console.log('Aceptando notificación:', notificacion);
            marcarComoLeido(id);
            mostrarMensaje('Solicitud aceptada correctamente', 'success');
        }
    }

    function manejarRechazar(id) {
        const notificacion = notificaciones.find(notif => notif.id == id);
        if (notificacion) {
            // Aquí iría la lógica para rechazar la solicitud
            console.log('Rechazando notificación:', notificacion);
            marcarComoLeido(id);
            mostrarMensaje('Solicitud rechazada', 'info');
        }
    }

    function cerrarModal(modal) {
        modal.style.display = 'none';
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        }, 300);
    }

    function mostrarMensaje(mensaje, tipo) {
        let container = document.getElementById("popup-container");

        if (!container) {
            container = document.createElement("div");
            container.id = "popup-container";
            document.body.appendChild(container);
        }

        // Evitar duplicados
        if ([...container.children].some(el => el.textContent.includes(mensaje))) {
            return;
        }

        const popup = document.createElement("div");
        popup.className = `popup ${tipo}`;

        const tipoTokens = (tipo || '').split(/\s+/).filter(Boolean);
        const tipoBase = tipoTokens.find(t => ['success', 'error', 'warning', 'info'].includes(t)) || 'info';
        let icono = 'ℹ';

        if (tipoTokens.includes('eliminar')) {
            icono = '⚠';
        } else if (tipoTokens.includes('editar')) {
            icono = '✎';
        } else if (tipoBase === 'success') {
            icono = '✔';
        } else if (tipoBase === 'error') {
            icono = '✖';
        } else if (tipoBase === 'warning') {
            icono = '⚠';
        }

        popup.innerHTML = `
            <span class="icon">${icono}</span>
            <span>${mensaje}</span>
        `;

        container.appendChild(popup);

        setTimeout(() => {
            popup.style.opacity = "0";
            popup.style.transform = "translateY(-10px)";
            setTimeout(() => popup.remove(), 300);
        }, 3500);
    }

    window.mostrarMensaje = mostrarMensaje;
    window.__processPopupMessages = function() {
        if (!window.__pendingPopupMessages || !window.__pendingPopupMessages.length) return;
        window.__pendingPopupMessages.forEach(function(item) {
            if (item && item.text) {
                mostrarMensaje(item.text, item.type || 'info');
            }
        });
        window.__pendingPopupMessages.length = 0;
    };
    window.__processPopupMessages();

    // Inicializar
    inicializarNotificaciones();
});
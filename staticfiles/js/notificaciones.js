document.addEventListener('DOMContentLoaded', function () {
 
    // ─── Configuración ───────────────────────────────────────────────
    const VISIBLE_MAX = 10;   // cuántas se muestran en el dropdown
    const BUFFER_MAX  = 50;   // cuántas se traen de la BD (ya vienen en el HTML)
 
    const wrapper = document.getElementById('notificacionesBell') || document.querySelector('.notificaciones-wrapper');
    let badge = null;
    let contadorNoLeidas = window.NOTIF_COUNT || 0;
 
    // ─── Badge ────────────────────────────────────────────────────────
    function renderBadge() {
        if (!badge) return;
        badge.textContent = contadorNoLeidas;
        if (contadorNoLeidas > 0) {
            badge.style.display    = 'flex';
            badge.style.opacity    = '1';
            badge.style.transform  = 'scale(1)';
        } else {
            badge.style.opacity   = '0';
            badge.style.transform = 'scale(0.6)';
            badge.style.display   = 'none';
        }
    }
 
    function descontarBadge() {
        if (contadorNoLeidas > 0) contadorNoLeidas--;
        renderBadge();
    }
 
    // ─── Helpers DOM ──────────────────────────────────────────────────
    function todosLosItems() {
        var dd = document.getElementById('notificacionesDropdown');
        if (!dd) return [];
        // Todos los ítems, incluyendo los ocultos en cola
        return Array.from(dd.querySelectorAll('.dropdown-notif-item'));
    }
 
    // ─── Cola / buffer ────────────────────────────────────────────────
    // Al arrancar: los primeros VISIBLE_MAX se muestran; el resto queda
    // en cola (display:none, data-en-cola="1"). Cuando se elimina uno
    // visible, el primero de la cola hace slide-in y ocupa su lugar.
    function actualizarCola() {
        var items = todosLosItems();
 
        items.forEach(function (li, idx) {
            if (idx < VISIBLE_MAX) {
                // Debe ser visible
                if (li.dataset.enCola === '1') {
                    // Viene de la cola → animar entrada
                    li.dataset.enCola = '0';
                    li.style.display     = '';
                    li.style.opacity     = '0';
                    li.style.transform   = 'translateY(-8px)';
                    li.style.transition  = 'opacity 300ms ease, transform 300ms ease';
                    // Forzar reflow para que la transición arranque
                    li.getBoundingClientRect();
                    li.style.opacity   = li.dataset.leida === '1' ? '0.55' : '1';
                    li.style.transform = 'translateY(0)';
                } else {
                    li.style.display = '';
                }
            } else {
                // Debe estar en cola (oculto)
                li.style.display   = 'none';
                li.dataset.enCola  = '1';
            }
        });
 
        // Placeholder "sin notificaciones"
        var dd    = document.getElementById('notificacionesDropdown');
        if (!dd) return;
        var lista       = dd.querySelector('.dropdown-list');
        var placeholder = dd.querySelector('.sin-notif-placeholder');
 
        if (items.length === 0) {
            if (!placeholder && lista) {
                lista.innerHTML = '<li class="sin-notif-placeholder" style="text-align:center; padding:20px; color:#999; list-style:none;"><i class="fa-solid fa-bell-slash" style="font-size:24px; display:block; margin-bottom:8px;"></i><p style="margin:0; font-size:13px;">Sin notificaciones</p></li>';
            }
        } else {
            if (placeholder) placeholder.remove();
        }
<<<<<<< HEAD
        actualizarBadge();
        // Agregar event listener al wrapper (el click abre el panel/modal)
        wrapperNotificaciones.addEventListener('click', mostrarNotificaciones);

        // Si existe dropdown server-renderizado, agregar delegación para eliminar desde el dropdown
        const dropdown = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
        if (dropdown) {
            // delegación para acciones dentro del dropdown
            dropdown.addEventListener('click', function(ev) {
                const btnMarcarTodas = ev.target.closest('.btn-marcar-todas');
                if (btnMarcarTodas) {
                    ev.stopPropagation();
                    marcarTodasComoLeidas();
                    return;
                }

                const btnMarcar = ev.target.closest('.btn-marcar-leido');
                if (btnMarcar) {
                    ev.stopPropagation();
                    const id = btnMarcar.getAttribute('data-id');
                    if (id) marcarComoLeido(id);
                    return;
                }

                const btnEliminar = ev.target.closest('.btn-eliminar-notificacion');
                if (!btnEliminar) return;
                ev.stopPropagation();
                const id = btnEliminar.getAttribute('data-id');
                const li = btnEliminar.closest('.dropdown-notif-item');
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
=======
    }
 
    // ─── Marcar leída ─────────────────────────────────────────────────
    function marcarComoLeido(id, li) {
        fetch('/notificaciones/' + id + '/marcar-leida/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: '{}'
        })
        .then(function (resp) {
            if (resp.ok) {
                li.setAttribute('data-leida', '1');
                li.classList.remove('notificacion-no-leida');
                li.style.opacity = '0.55';
                var btnLeida = li.querySelector('.btn-marcar-leida');
                if (btnLeida) btnLeida.remove();
                descontarBadge();
            }
        })
        .catch(function (err) { console.error(err); });
    }
 
    // ─── Eliminar ─────────────────────────────────────────────────────
    function eliminarNotificacion(id, li) {
        var eraNoLeida = li.getAttribute('data-leida') === '0' ||
                         li.classList.contains('notificacion-no-leida');
 
        fetch('/notificaciones/' + id + '/eliminar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: '{}'
        })
        .then(function (resp) {
            if (!resp.ok) return;
 
            // Animación de salida
            li.style.transition    = 'opacity 200ms ease, transform 200ms ease, max-height 250ms ease';
            li.style.overflow      = 'hidden';
            li.style.maxHeight     = li.offsetHeight + 'px';
            li.getBoundingClientRect();
            li.style.opacity       = '0';
            li.style.transform     = 'translateX(20px)';
            li.style.maxHeight     = '0';
            li.style.padding       = '0';
            li.style.marginBottom  = '0';
 
            setTimeout(function () {
                if (li.parentNode) li.parentNode.removeChild(li);
                if (eraNoLeida) descontarBadge();
                // Después de sacar el ítem del DOM, reordenar la cola:
                // el primero en cola (idx === VISIBLE_MAX ahora es idx === VISIBLE_MAX-1)
                // pasará a ser visible gracias a actualizarCola().
                actualizarCola();
            }, 260);
        })
        .catch(function () {});
    }
 
    // ─── Cookie helper ────────────────────────────────────────────────
    function getCookie(name) {
        var value = '; ' + document.cookie;
        var parts = value.split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
 
    // ─── Toggle dropdown ──────────────────────────────────────────────
    function mostrarNotificaciones(e) {
        var dd = document.getElementById('notificacionesDropdown');
        if (dd && dd.contains(e.target)) return;
        e.stopPropagation();
        if (dd) {
            dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
>>>>>>> blackboxai/fix-back-log
        }
    }
 
    // ─── Init ─────────────────────────────────────────────────────────
    function init() {
        if (!wrapper) return;
 
        badge = document.querySelector('.notificaciones-badge');
        if (!badge) {
            badge = document.createElement('span');
            badge.className = 'notificaciones-badge';
            wrapper.appendChild(badge);
        }
 
        renderBadge();
 
        // Marcar visualmente las ya leídas y poner en cola las que
        // superan VISIBLE_MAX desde el arranque.
        todosLosItems().forEach(function (li, idx) {
            if (li.getAttribute('data-leida') === '1') {
                li.style.opacity = '0.55';
            }
            if (idx >= VISIBLE_MAX) {
                li.style.display  = 'none';
                li.dataset.enCola = '1';
            }
        });
 
        wrapper.addEventListener('click', mostrarNotificaciones);
 
        document.addEventListener('click', function (ev) {
            var dd = document.getElementById('notificacionesDropdown');
            if (!dd) return;
 
            // Botón eliminar
            var btnEliminar = ev.target.closest('.btn-eliminar-notificacion');
            if (btnEliminar) {
                var id = btnEliminar.getAttribute('data-id');
                var li = btnEliminar.closest('.dropdown-notif-item');
                eliminarNotificacion(id, li);
                return;
            }
 
            // Botón marcar leída
            var btnLeida = ev.target.closest('.btn-marcar-leida');
            if (btnLeida) {
                var id = btnLeida.getAttribute('data-id');
                var li = btnLeida.closest('.dropdown-notif-item');
                marcarComoLeido(id, li);
                return;
            }
 
            // Click fuera → cerrar
            if (!wrapper.contains(ev.target) && dd.style.display === 'block') {
                dd.style.display = 'none';
            }
        });
    }
<<<<<<< HEAD

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
            return;
        }

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

    function marcarTodasComoLeidas() {
        fetch('/notificaciones/leidas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: '{}'
        }).then(resp => {
            if (resp.ok) {
                const dropdown = document.getElementById('notificacionesDropdown') || wrapperNotificaciones.querySelector('.notificaciones-dropdown');
                if (dropdown) {
                    dropdown.querySelectorAll('.dropdown-notif-item[data-leida="0"]').forEach(li => {
                        li.setAttribute('data-leida', '1');
                        li.classList.remove('notificacion-no-leida');
                        const actionBtn = li.querySelector('.btn-marcar-leido');
                        if (actionBtn) actionBtn.remove();
                    });
                }
                actualizarBadge();
                mostrarMensaje('Todas las notificaciones quedaron como leídas', 'success');
            } else {
                mostrarMensaje('No se pudo marcar todas las notificaciones como leídas', 'error');
            }
        }).catch(err => {
            console.error(err);
            mostrarMensaje('Error de red al marcar todas las notificaciones', 'error');
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
                        const actionBtn = li.querySelector('.btn-marcar-leido');
                        if (actionBtn) actionBtn.remove();
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
=======
 
    init();
>>>>>>> blackboxai/fix-back-log
});
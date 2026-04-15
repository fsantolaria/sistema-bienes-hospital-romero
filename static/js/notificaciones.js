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
 
    init();
});
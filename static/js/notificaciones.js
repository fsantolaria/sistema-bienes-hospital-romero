document.addEventListener('DOMContentLoaded', function () {

    const VISIBLE_MAX = 10;

    const wrapper = document.getElementById('notificacionesBell') || document.querySelector('.notificaciones-wrapper');
    let badge = null;
    let contadorNoLeidas = window.NOTIF_COUNT || 0;

    function renderBadge() {
        if (!badge) return;
        badge.textContent = contadorNoLeidas;
        if (contadorNoLeidas > 0) {
            badge.style.display = 'flex';
            badge.style.opacity = '1';
            badge.style.transform = 'scale(1)';
        } else {
            badge.style.opacity = '0';
            badge.style.transform = 'scale(0.6)';
            badge.style.display = 'none';
        }
    }

    function descontarBadge() {
        if (contadorNoLeidas > 0) contadorNoLeidas--;
        renderBadge();
    }

    function todosLosItems() {
        var dd = document.getElementById('notificacionesDropdown');
        if (!dd) return [];
        return Array.from(dd.querySelectorAll('.dropdown-notif-item'));
    }

    function actualizarCola() {
        var items = todosLosItems();
        items.forEach(function (li, idx) {
            if (idx < VISIBLE_MAX) {
                if (li.dataset.enCola === '1') {
                    li.dataset.enCola = '0';
                    li.style.transition = 'opacity 300ms ease, transform 300ms ease';
                    li.style.opacity = '0';
                    li.style.transform = 'translateY(-8px)';
                    li.style.display = '';
                    li.getBoundingClientRect();
                    li.style.opacity = li.dataset.leida === '1' ? '0.55' : '1';
                    li.style.transform = 'translateY(0)';
                } else {
                    li.style.display = '';
                }
            } else {
                li.style.display = 'none';
                li.dataset.enCola = '1';
            }
        });

        var dd = document.getElementById('notificacionesDropdown');
        if (!dd) return;
        var lista = dd.querySelector('.dropdown-list');
        var placeholder = dd.querySelector('.sin-notif-placeholder');
        if (items.length === 0) {
            if (!placeholder && lista) {
                lista.innerHTML = '<li class="sin-notif-placeholder" style="text-align:center; padding:20px; color:#999; list-style:none;"><i class="fa-solid fa-bell-slash" style="font-size:24px; display:block; margin-bottom:8px;"></i><p style="margin:0; font-size:13px;">Sin notificaciones</p></li>';
            }
        } else {
            if (placeholder) placeholder.remove();
        }
    }

    function marcarComoLeido(id, li) {
        fetch('/notificaciones/' + id + '/marcar-leida/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
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

    function eliminarNotificacion(id, li) {
        var eraNoLeida = li.getAttribute('data-leida') === '0' || li.classList.contains('notificacion-no-leida');

        fetch('/notificaciones/' + id + '/eliminar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') || '' },
            body: '{}'
        })
        .then(function (resp) {
            if (!resp.ok) return;

            li.style.transition = 'opacity 200ms ease, transform 200ms ease, max-height 250ms ease';
            li.style.overflow = 'hidden';
            li.style.maxHeight = li.offsetHeight + 'px';
            li.getBoundingClientRect();
            li.style.opacity = '0';
            li.style.transform = 'translateX(20px)';
            li.style.maxHeight = '0';
            li.style.padding = '0';
            li.style.marginBottom = '0';

            setTimeout(function () {
                if (li.parentNode) li.parentNode.removeChild(li);
                if (eraNoLeida) descontarBadge();
                actualizarCola();
            }, 260);
        })
        .catch(function () {});
    }

    function getCookie(name) {
        var value = '; ' + document.cookie;
        var parts = value.split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function mostrarNotificaciones(e) {
        var dd = document.getElementById('notificacionesDropdown');
        if (dd && dd.contains(e.target)) return;
        e.stopPropagation();
        if (dd) {
            dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
        }
    }

    function init() {
        if (!wrapper) return;

        badge = document.querySelector('.notificaciones-badge');
        if (!badge) {
            badge = document.createElement('span');
            badge.className = 'notificaciones-badge';
            wrapper.appendChild(badge);
        }

        renderBadge();
        actualizarCola();

        todosLosItems().forEach(function (li) {
            if (li.getAttribute('data-leida') === '1') {
                li.style.opacity = '0.55';
            }
        });

        wrapper.addEventListener('click', mostrarNotificaciones);

        document.addEventListener('click', function (ev) {
            var dd = document.getElementById('notificacionesDropdown');
            if (!dd) return;

            var btnEliminar = ev.target.closest('.btn-eliminar-notificacion');
            if (btnEliminar) {
                var id = btnEliminar.getAttribute('data-id');
                var li = btnEliminar.closest('.dropdown-notif-item');
                eliminarNotificacion(id, li);
                return;
            }

            var btnLeida = ev.target.closest('.btn-marcar-leida');
            if (btnLeida) {
                var id = btnLeida.getAttribute('data-id');
                var li = btnLeida.closest('.dropdown-notif-item');
                marcarComoLeido(id, li);
                return;
            }

            if (!wrapper.contains(ev.target) && dd.style.display === 'block') {
                dd.style.display = 'none';
            }
        });
    }

    init();
});
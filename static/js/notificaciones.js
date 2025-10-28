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

    // Elementos del DOM
    const btnNotificaciones = document.querySelector('.header-icon[title="Notificaciones"]');
    let badgeNotificaciones = null;

    // Inicializar sistema de notificaciones
    function inicializarNotificaciones() {
        if (!btnNotificaciones) return;

        // Crear badge de notificaciones no leídas
        badgeNotificaciones = document.createElement('span');
        badgeNotificaciones.className = 'notificaciones-badge';
        actualizarBadge();

        // Agregar badge al botón de notificaciones
        btnNotificaciones.parentNode.classList.add('notificaciones-container');
        btnNotificaciones.parentNode.appendChild(badgeNotificaciones);

        // Agregar event listener
        btnNotificaciones.addEventListener('click', mostrarNotificaciones);
    }

    // Actualizar badge con número de notificaciones no leídas
    function actualizarBadge() {
        if (!badgeNotificaciones) return;

        const noLeidas = notificaciones.filter(notif => !notif.leida).length;
        badgeNotificaciones.textContent = noLeidas;
        badgeNotificaciones.style.display = noLeidas > 0 ? 'flex' : 'none';
    }

    // Mostrar modal de notificaciones
    function mostrarNotificaciones() {
        // Crear modal
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

        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
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
                <div style="display: flex; justify-content: space-between; align-items: center;">
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

    // Funciones de manejo de notificaciones
    function marcarComoLeido(id) {
        const notificacion = notificaciones.find(notif => notif.id == id);
        if (notificacion) {
            notificacion.leida = true;
            actualizarBadge();
            mostrarMensaje('Notificación marcada como leída', 'success');
        }
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
        // Puedes usar la misma función de mensajes que en operadores.js
        console.log(mensaje, tipo);
        // Temporal - puedes reemplazar con tu sistema de mensajes
        alert(mensaje);
    }

    // Inicializar
    inicializarNotificaciones();
});
// operadores.js
document.addEventListener('DOMContentLoaded', function() {
    // Elementos principales
    const tablaOperadores = document.querySelector('.tabla-operadores tbody');
    const btnAgregar = document.querySelector('.btn-icono-agregar');
    
    // Datos de ejemplo más completos
    const operadores = [
        { 
            id: 1, 
            usuario: 'PABLO', 
            nombreCompleto: 'Pablo Larralde',
            email: 'pablo.larralde@empresa.com',
            telefono: '+54 11 1234-5678',
            departamento: 'Sistemas',
            fechaAlta: '2023-01-15',
            estado: 'Activo',
            permisos: 'Administrador'
        },
        { 
            id: 2, 
            usuario: 'LEONEL', 
            nombreCompleto: 'Leonel Martinez',
            email: 'leonel.martinez@empresa.com',
            telefono: '+54 11 2345-6789',
            departamento: 'Recursos Humanos',
            fechaAlta: '2023-03-20',
            estado: 'Activo',
            permisos: 'Usuario'
        },
        { 
            id: 3, 
            usuario: 'EMILIA', 
            nombreCompleto: 'Emilia Gonzales',
            email: 'emilia.gonzales@empresa.com',
            telefono: '+54 11 3456-7890',
            departamento: 'Contabilidad',
            fechaAlta: '2023-02-10',
            estado: 'Activo',
            permisos: 'Supervisor'
        },
        { 
            id: 4, 
            usuario: 'ROBERTO', 
            nombreCompleto: 'Roberto Pettinato Diaz',
            email: 'roberto.pettinato@empresa.com',
            telefono: '+54 11 4567-8901',
            departamento: 'Operaciones',
            fechaAlta: '2023-04-05',
            estado: 'Activo',
            permisos: 'Usuario'
        }
    ];

    // Inicializar la tabla
    function inicializarTabla() {
        renderizarTabla();
        agregarEventListeners();
    }

    // Renderizar la tabla con los operadores
    function renderizarTabla() {
        tablaOperadores.innerHTML = '';
        
        operadores.forEach(operador => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${operador.usuario}</td>
                <td>${operador.nombreCompleto}</td>
                <td><span class="icono-ver-mas" data-id="${operador.id}" title="Ver más información">✅</span></td>
                <td><span class="icono-baja" data-id="${operador.id}" title="Dar de baja">💬</span></td>
            `;
            tablaOperadores.appendChild(fila);
        });

        // Agregar fila vacía al final
        const filaVacia = document.createElement('tr');
        filaVacia.innerHTML = `
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        `;
        tablaOperadores.appendChild(filaVacia);
    }

    // Agregar event listeners a los iconos
    function agregarEventListeners() {
        // Botón agregar operador
        btnAgregar.addEventListener('click', function() {
            abrirModalAgregar();
        });

        // Iconos ver más
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('icono-ver-mas')) {
                const id = e.target.getAttribute('data-id');
                verDetallesOperador(id);
            }
        });

        // Iconos baja
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('icono-baja')) {
                const id = e.target.getAttribute('data-id');
                confirmarBaja(id);
            }
        });
    }

    // Función para ver detalles completos del operador
    function verDetallesOperador(id) {
        const operador = operadores.find(op => op.id == id);
        if (operador) {
            mostrarModalDetalles(operador);
        }
    }

    // Modal para ver detalles completos del operador
    function mostrarModalDetalles(operador) {
        const modal = document.createElement('div');
        modal.className = 'modal-operadores';
        modal.innerHTML = `
            <div class="modal-contenido modal-detalles">
                <div class="modal-header">
                    <h3>Detalles del Operador</h3>
                    <button class="btn-cerrar-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="detalles-operador">
                        <div class="info-principal">
                            <div class="avatar-operador">
                                <i class="fa-solid fa-user"></i>
                            </div>
                            <div class="datos-principales">
                                <h4>${operador.nombreCompleto}</h4>
                                <p class="usuario">@${operador.usuario.toLowerCase()}</p>
                            </div>
                        </div>
                        
                        <div class="seccion-detalles">
                            <h5>Información Personal</h5>
                            <div class="detalle-item">
                                <span class="etiqueta">Email:</span>
                                <span class="valor">${operador.email}</span>
                            </div>
                            <div class="detalle-item">
                                <span class="etiqueta">Teléfono:</span>
                                <span class="valor">${operador.telefono}</span>
                            </div>
                            <div class="detalle-item">
                                <span class="etiqueta">Departamento:</span>
                                <span class="valor">${operador.departamento}</span>
                            </div>
                        </div>
                        
                        <div class="seccion-detalles">
                            <h5>Información Laboral</h5>
                            <div class="detalle-item">
                                <span class="etiqueta">Fecha de Alta:</span>
                                <span class="valor">${formatearFecha(operador.fechaAlta)}</span>
                            </div>
                            <div class="detalle-item">
                                <span class="etiqueta">Estado:</span>
                                <span class="valor estado-${operador.estado.toLowerCase()}">${operador.estado}</span>
                            </div>
                            <div class="detalle-item">
                                <span class="etiqueta">Nivel de Permisos:</span>
                                <span class="valor permisos-${operador.permisos.toLowerCase()}">${operador.permisos}</span>
                            </div>
                        </div>
                        
                        <div class="seccion-detalles">
                            <h5>Actividad Reciente</h5>
                            <div class="actividad-item">
                                <span class="actividad-icono">📋</span>
                                <span class="actividad-texto">Último acceso: Hoy 14:30</span>
                            </div>
                            <div class="actividad-item">
                                <span class="actividad-icono">🔐</span>
                                <span class="actividad-texto">Contraseña actualizada hace 15 días</span>
                            </div>
                        </div>
                    </div>
                    <div class="modal-actions">
                        <button class="btn-editar" data-id="${operador.id}">
                            <i class="fa-solid fa-pen"></i> Editar
                        </button>
                        <button class="btn-cerrar">Cerrar</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Event listeners del modal
        const btnCerrar = modal.querySelector('.btn-cerrar-modal');
        const btnCerrar2 = modal.querySelector('.btn-cerrar');
        const btnEditar = modal.querySelector('.btn-editar');

        btnCerrar.addEventListener('click', cerrarModal);
        btnCerrar2.addEventListener('click', cerrarModal);
        btnEditar.addEventListener('click', function() {
            editarOperador(operador.id);
            cerrarModal();
        });

        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                cerrarModal();
            }
        });

        function cerrarModal() {
            document.body.removeChild(modal);
        }
    }

    // Función para formatear fecha
    function formatearFecha(fecha) {
        const opciones = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(fecha).toLocaleDateString('es-ES', opciones);
    }

    // Función para editar operador (placeholder)
    function editarOperador(id) {
        console.log('Editar operador:', id);
        // Aquí puedes implementar la lógica para editar
        alert(`Funcionalidad de edición para el operador ${id} - En desarrollo`);
    }

    // Función para confirmar baja de operador
    function confirmarBaja(id) {
        const operador = operadores.find(op => op.id == id);
        if (operador) {
            const confirmar = confirm(`¿Está seguro que desea dar de baja al operador ${operador.nombreCompleto}?`);
            
            if (confirmar) {
                // En un caso real, aquí harías una petición DELETE a la API
                console.log('Dar de baja operador:', operador);
                
                // Simular eliminación
                const index = operadores.findIndex(op => op.id == id);
                if (index !== -1) {
                    operadores.splice(index, 1);
                    renderizarTabla();
                    mostrarMensaje('Operador dado de baja correctamente', 'success');
                }
            }
        }
    }

    // Resto de funciones (modal agregar, mensajes, etc.)...
    function abrirModalAgregar() {
        // Tu código existente para agregar operadores
        console.log('Abrir modal agregar');
    }

    function mostrarMensaje(mensaje, tipo) {
        // Tu código existente para mostrar mensajes
        console.log(mensaje, tipo);
    }

    // CSS adicional para los modales de detalles
    const estiloModal = document.createElement('style');
    estiloModal.textContent = `
        .modal-operadores {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .modal-contenido {
            background: white;
            border-radius: 8px;
            width: 90%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }

        .modal-detalles {
            max-width: 600px;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid #ddd;
        }

        .modal-header h3 {
            margin: 0;
            color: #333;
        }

        .btn-cerrar-modal {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #666;
        }

        .modal-body {
            padding: 20px;
        }

        .info-principal {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }

        .avatar-operador {
            width: 60px;
            height: 60px;
            background-color: #4CAF50;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: white;
            font-size: 24px;
        }

        .datos-principales h4 {
            margin: 0 0 5px 0;
            color: #333;
        }

        .usuario {
            margin: 0;
            color: #666;
            font-style: italic;
        }

        .seccion-detalles {
            margin-bottom: 25px;
        }

        .seccion-detalles h5 {
            margin: 0 0 15px 0;
            color: #333;
            font-size: 16px;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
        }

        .detalle-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #f5f5f5;
        }

        .etiqueta {
            font-weight: bold;
            color: #555;
            min-width: 150px;
        }

        .valor {
            color: #333;
            text-align: right;
        }

        .estado-activo {
            color: #4CAF50;
            font-weight: bold;
        }

        .permisos-administrador {
            color: #f44336;
            font-weight: bold;
        }

        .permisos-supervisor {
            color: #ff9800;
            font-weight: bold;
        }

        .permisos-usuario {
            color: #2196F3;
            font-weight: bold;
        }

        .actividad-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
        }

        .actividad-icono {
            margin-right: 10px;
            font-size: 16px;
        }

        .actividad-texto {
            color: #666;
            font-size: 14px;
        }

        .modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }

        .btn-editar {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .btn-cerrar {
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }

        .btn-editar:hover {
            background-color: #0b7dda;
        }

        .btn-cerrar:hover {
            background-color: #5a6268;
        }
    `;

    document.head.appendChild(estiloModal);

    // Inicializar la aplicación
    inicializarTabla();
});
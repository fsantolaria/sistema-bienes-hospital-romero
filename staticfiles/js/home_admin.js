document.addEventListener('DOMContentLoaded', () => {
    console.log("Dashboard de administración cargado correctamente");

    // Botón BIENES
    document.getElementById('btn-bienes').addEventListener('click', () => {
        console.log("Navegando a gestión de bienes");
    });

    // Botón OPERADORES
    document.getElementById('btn-operadores').addEventListener('click', () => {
        console.log("Navegando a gestión de operadores");
    });

    // Botón PERFIL
    document.getElementById('btn-perfil').addEventListener('click', () => {
        console.log("Botón PERFIL presionado");
        // Aquí puedes agregar la funcionalidad del perfil
        alert('Funcionalidad de perfil en desarrollo');
    });

    // Notificaciones
    document.querySelector('.material-symbols-outlined[title="Notificaciones"]').addEventListener('click', () => {
        console.log("Notificaciones clickeadas");
        alert('No hay notificaciones nuevas');
    });
});
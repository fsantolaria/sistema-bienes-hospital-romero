document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const adminBtn = document.getElementById('admin-btn');
    const userBtn = document.getElementById('user-btn');

    // Función para simular la redirección al login
    function redirectToLogin(userType) {
        const button = userType === 'admin' ? adminBtn : userBtn;
        const originalText = button.innerHTML;

        button.classList.add('loading');
        button.disabled = true;

        setTimeout(() => {
            alert(`Redirigiendo al login de ${userType === 'admin' ? 'Administrador' : 'Usuario'}`);
            button.classList.remove('loading');
            button.innerHTML = originalText;
            button.disabled = false;
        }, 1500);
    }

    // Eventos para los botones
    adminBtn.addEventListener('click', function() {
        this.innerHTML = 'Cargando...';
        redirectToLogin('admin');
    });

    userBtn.addEventListener('click', function() {
        this.innerHTML = 'Cargando...';
        redirectToLogin('user');
    });

    // Efectos de hover mejorados
    const buttons = document.querySelectorAll('.login-button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '2px 3px 4px rgba(0, 0, 0, 0.2)';
        });
    });
});

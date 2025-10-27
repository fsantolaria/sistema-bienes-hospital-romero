document.addEventListener('DOMContentLoaded', function() {
    // ---------------------------
    // BOTONES DE LOGIN
    // ---------------------------
    document.addEventListener('click', function(e) {
        if (e.target.id === 'admin-btn' || e.target.closest('#admin-btn')) {
            handleButtonClick('admin', e.target);
        } else if (e.target.id === 'user-btn' || e.target.closest('#user-btn')) {
            handleButtonClick('user', e.target);
        }
    });

    function handleButtonClick(userType, button) {
        const originalText = button.innerHTML;
        
        button.classList.add('loading');
        button.disabled = true;
        button.innerHTML = 'Cargando...';

        setTimeout(() => {
            alert(`Redirigiendo al login de ${userType === 'admin' ? 'Administrador' : 'Usuario'}`);
            button.classList.remove('loading');
            button.innerHTML = originalText;
            button.disabled = false;
        }, 1500);
    }

    // ---------------------------
    // EFECTOS DE HOVER LOGIN
    // ---------------------------
    document.addEventListener('mouseover', function(e) {
        if (e.target.classList.contains('login-button')) {
            e.target.style.transform = 'translateY(-3px)';
            e.target.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
        }
    });

    document.addEventListener('mouseout', function(e) {
        if (e.target.classList.contains('login-button')) {
            e.target.style.transform = 'translateY(0)';
            e.target.style.boxShadow = '2px 3px 4px rgba(0, 0, 0, 0.2)';
        }
    });
});
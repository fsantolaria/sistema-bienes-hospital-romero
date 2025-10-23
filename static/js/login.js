document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginBox = document.getElementById('loginBox');
    const usernameField = document.getElementById('usernameField');
    const passwordField = document.getElementById('passwordField');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const loginError = document.getElementById('loginError');
    const loginButton = document.getElementById('loginButton');
    const spinner = document.querySelector('.spinner');
    const buttonText = document.querySelector('.button-text');

    // Si hay errores de Django, mostramos el mensaje
    {% if form.errors %}
    loginError.style.display = 'block';
    {% endif %}

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Resetear errores
        resetErrors();
        
        const username = document.getElementById('usuario').value.trim();
        const password = document.getElementById('contrasena').value.trim();
        
        let isValid = true;
        
        // Validar usuario
        if (!username) {
            showError(usernameField, usernameError, 'Por favor ingrese su usuario');
            isValid = false;
        }
        
        // Validar contraseña
        if (!password) {
            showError(passwordField, passwordError, 'Por favor ingrese su contraseña');
            isValid = false;
        } else if (password.length < 5) {
            showError(passwordField, passwordError, 'La contraseña debe tener al menos 5 caracteres');
            isValid = false;
        }
        
        if (!isValid) {
            loginBox.classList.add('shake');
            setTimeout(() => loginBox.classList.remove('shake'), 500);
            return;
        }
        
        // Si pasa validación frontend, enviar el formulario normalmente
        loginForm.submit();
    });

    function showError(field, errorElement, message) {
        field.classList.add('error');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    function resetErrors() {
        usernameField.classList.remove('error');
        passwordField.classList.remove('error');
        usernameError.style.display = 'none';
        passwordError.style.display = 'none';
        loginError.style.display = 'none';
    }

    // Limpiar errores cuando el usuario comience a escribir
    document.getElementById('usuario').addEventListener('input', function() {
        usernameField.classList.remove('error');
        usernameError.style.display = 'none';
        loginError.style.display = 'none';
    });

    document.getElementById('contrasena').addEventListener('input', function() {
        passwordField.classList.remove('error');
        passwordError.style.display = 'none';
        loginError.style.display = 'none';
    });
});
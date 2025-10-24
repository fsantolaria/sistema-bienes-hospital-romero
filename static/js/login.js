document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;
    const loginBox = document.getElementById('loginBox');
    const usernameField = document.getElementById('usernameField');
    const passwordField = document.getElementById('passwordField');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const loginError = document.getElementById('loginError');
    const loginButton = document.getElementById('loginButton');
    const spinner = loginButton ? loginButton.querySelector('.spinner') : null;
    const buttonText = loginButton ? loginButton.querySelector('.button-text') : null;

    // Si el template ya renderizó un error con estilo inline, respetarlo.
    // Evitar mostrarlo solo porque el elemento contiene el texto por defecto.
    if (loginError && loginError.style.display === 'block') {
        loginError.style.display = 'block';
    }

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Resetear errores
        resetErrors();

        const username = (document.getElementById('usuario') || {}).value || '';
        const password = (document.getElementById('contrasena') || {}).value || '';

        let isValid = true;

        // Validar usuario
        if (!username.trim()) {
            showError(usernameField, usernameError, 'Por favor ingrese su usuario');
            isValid = false;
        }

        // Validar contraseña
        if (!password.trim()) {
            showError(passwordField, passwordError, 'Por favor ingrese su contraseña');
            isValid = false;
        } else if (password.length < 5) {
            showError(passwordField, passwordError, 'La contraseña debe tener al menos 5 caracteres');
            isValid = false;
        }

        if (!isValid) {
            if (loginBox) {
                loginBox.classList.add('shake');
                setTimeout(() => loginBox.classList.remove('shake'), 500);
            }
            // If client-side validation blocked submission but user did type
            // a username and some password text, show the same global inline
            // login error so feedback is consistent (avoids needing a second try
            // to see the red 'incorrect credentials' message).
            const uname = (document.getElementById('usuario') || {}).value || '';
            const pwd = (document.getElementById('contrasena') || {}).value || '';
            // Mostrar el mensaje global de credenciales incorrectas tan pronto
            // como el usuario haya tecleado alguna contraseña (evita esperar a
            // que cumpla la longitud mínima). Esto da feedback inmediato.
            if (loginError && pwd.trim().length > 0) {
                loginError.textContent = 'El Usuario y/o Contraseña es incorrecto';
                loginError.style.display = 'block';
            }
            return;
        }

        // UX: mostrar spinner y deshabilitar botón para evitar envíos dobles
        if (loginButton) {
            loginButton.classList.add('loading');
            loginButton.disabled = true;
        }

        // Enviar formulario
        loginForm.submit();
    });

    function showError(field, errorElement, message) {
        if (field) field.classList.add('error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    function resetErrors() {
        if (usernameField) usernameField.classList.remove('error');
        if (passwordField) passwordField.classList.remove('error');
        if (usernameError) usernameError.style.display = 'none';
        if (passwordError) passwordError.style.display = 'none';
        if (loginError) loginError.style.display = 'none';
    }

    // Limpiar errores cuando el usuario comience a escribir
    const usuarioInput = document.getElementById('usuario');
    if (usuarioInput) {
        usuarioInput.addEventListener('input', function() {
            if (usernameField) usernameField.classList.remove('error');
            if (usernameError) usernameError.style.display = 'none';
            if (loginError) loginError.style.display = 'none';
        });
    }

    const contrasenaInput = document.getElementById('contrasena');
    if (contrasenaInput) {
        contrasenaInput.addEventListener('input', function() {
            if (passwordField) passwordField.classList.remove('error');
            if (passwordError) passwordError.style.display = 'none';
            if (loginError) loginError.style.display = 'none';
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginBox = document.getElementById('loginBox');
    const usernameField = document.getElementById('usernameField');
    const passwordField = document.getElementById('passwordField');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const loginError = document.getElementById('loginError');

    loginForm.addEventListener('submit', function(e) {
        // Validación frontend antes de enviar
        let isValid = true;
        const username = document.getElementById('usuario').value.trim();
        const password = document.getElementById('contrasena').value.trim();

        resetErrors();

        if (!username) {
            showError(usernameField, usernameError, 'Por favor ingrese su usuario');
            isValid = false;
        }

        if (!password) {
            showError(passwordField, passwordError, 'Por favor ingrese su contraseña');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            loginBox.classList.add('shake');
            setTimeout(() => loginBox.classList.remove('shake'), 500);
            return;
        }
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
        if (loginError) loginError.style.display = 'none';
    }

    document.getElementById('usuario').addEventListener('input', function() {
        usernameField.classList.remove('error');
        usernameError.style.display = 'none';
        if (loginError) loginError.style.display = 'none';
    });

    document.getElementById('contrasena').addEventListener('input', function() {
        passwordField.classList.remove('error');
        passwordError.style.display = 'none';
        if (loginError) loginError.style.display = 'none';
    });
});
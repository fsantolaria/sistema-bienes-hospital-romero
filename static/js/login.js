document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;
    const loginBox = document.getElementById('loginBox');
    
    // Inputs directos
    const usernameInput = document.getElementById('usuario');
    const passwordInput = document.getElementById('contrasena');
    
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const loginError = document.getElementById('loginError');
    const loginButton = document.getElementById('loginButton');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            resetErrors();

            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();
            let isValid = true;

            if (!username) {
                showError(usernameInput, usernameError, 'Por favor ingrese su usuario');
                isValid = false;
            }

            if (!password) {
                showError(passwordInput, passwordError, 'Por favor ingrese su contraseña');
                isValid = false;
            }

            if (!isValid) {
                if (loginBox) {
                    loginBox.classList.add('shake');
                    setTimeout(() => loginBox.classList.remove('shake'), 500);
                }
                return;
            }

            if (loginButton) {
                loginButton.classList.add('loading');
                loginButton.disabled = true;
            }
            loginForm.submit();
        });
    }

    function showError(input, errorElement, message) {
        if (input) input.classList.add('error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    function resetErrors() {
        if (usernameInput) usernameInput.classList.remove('error');
        if (passwordInput) passwordInput.classList.remove('error');
        if (usernameError) usernameError.style.display = 'none';
        if (passwordError) passwordError.style.display = 'none';
        if (loginError) loginError.style.display = 'none';
    }

    if (usernameInput) {
        usernameInput.addEventListener('input', () => {
            usernameInput.classList.remove('error');
            usernameError.style.display = 'none';
            if (loginError) loginError.style.display = 'none';
        });
    }

    if (passwordInput) {
        passwordInput.addEventListener('input', () => {
            passwordInput.classList.remove('error');
            passwordError.style.display = 'none';
            if (loginError) loginError.style.display = 'none';
        });
    }
});
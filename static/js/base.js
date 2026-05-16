document.addEventListener('DOMContentLoaded', function() {
    // ---------------------------
    // BOTONES DE LOGIN
    // ---------------------------
    document.addEventListener('click', function(e) {
        const dismissibleMessage = e.target.closest('.mensaje-success-distintivo');
        if (dismissibleMessage) {
            dismissibleMessage.remove();
            return;
        }

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

    // ---------------------------
    // NO REMOVER MENSAJES AUTOMÁTICAMENTE
    // ---------------------------
    // Los mensajes de éxito se muestran de forma estática y no se eliminan ni animan.
    
    // ---------------------------
    // MODO OSCURO (DARK MODE)
    // ---------------------------
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (themeToggle) {
        const updateIcon = (theme) => {
            if (!themeIcon) return;
            if (theme === 'dark') {
                themeIcon.textContent = 'light_mode';
            } else {
                themeIcon.textContent = 'dark_mode';
            }
        };

        // El tema inicial ya lo pone Django en el <html> via data-theme
        // Solo actualizamos el icono
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        updateIcon(currentTheme);

        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            const isDark = newTheme === 'dark';

            // Cambio visual inmediato
            document.documentElement.setAttribute('data-theme', newTheme);
            updateIcon(newTheme);
            
            // Sincronización con el servidor (si está autenticado)
            fetch('/actualizar-tema/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ tema_oscuro: isDark })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'ok') {
                    console.error('Error al guardar preferencia de tema:', data.message);
                }
            })
            .catch(error => {
                console.error('Error en la petición de tema:', error);
            });
        });
    }

    // ---------------------------
    // FLOATING SCROLLBAR (STICKY)
    // ---------------------------
    function initFloatingScrollbar() {
        // Buscamos contenedores de tablas responsivas
        const containers = document.querySelectorAll('.table-responsive');
        
        containers.forEach(container => {
            if (container.dataset.floatingScrollInit) return;
            container.dataset.floatingScrollInit = 'true';

            const table = container.querySelector('table');
            if (!table) return;

            // Creamos un div para la barra "fantasma"
            const ghostScroll = document.createElement('div');
            ghostScroll.className = 'floating-scrollbar-ghost';
            ghostScroll.style.cssText = `
                position: fixed;
                bottom: 0;
                overflow-x: auto;
                overflow-y: hidden;
                z-index: 1050;
                display: none;
                height: 20px;
                background: rgba(255,255,255,0.1);
            `;

            const ghostContent = document.createElement('div');
            ghostContent.style.height = '1px';
            ghostScroll.appendChild(ghostContent);
            document.body.appendChild(ghostScroll);

            const updatePosition = () => {
                const rect = container.getBoundingClientRect();
                const viewportHeight = window.innerHeight;

                // Solo mostrar si el contenedor está en el viewport pero su parte inferior está fuera
                const isVisible = rect.top < viewportHeight && rect.bottom > 0;
                const bottomIsOffscreen = rect.bottom > viewportHeight;

                if (isVisible && bottomIsOffscreen) {
                    ghostScroll.style.display = 'block';
                    ghostScroll.style.left = rect.left + 'px';
                    ghostScroll.style.width = rect.width + 'px';
                    ghostContent.style.width = table.offsetWidth + 'px';
                    ghostScroll.scrollLeft = container.scrollLeft;
                } else {
                    ghostScroll.style.display = 'none';
                }
            };

            // Sincronizar scrolls
            ghostScroll.onscroll = () => {
                container.scrollLeft = ghostScroll.scrollLeft;
            };
            container.onscroll = () => {
                ghostScroll.scrollLeft = container.scrollLeft;
            };

            window.addEventListener('scroll', updatePosition);
            window.addEventListener('resize', updatePosition);
            new ResizeObserver(updatePosition).observe(table);
            new ResizeObserver(updatePosition).observe(container);
            
            updatePosition();
        });
    }

    initFloatingScrollbar();
});
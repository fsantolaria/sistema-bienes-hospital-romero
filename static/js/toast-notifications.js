// Toast Notification System
(function() {
    function getToastContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    window.showToast = function(message, type = 'success', duration = 4000) {
        // Si hay un contenedor inline, usarlo en lugar de toast flotante
        const inlineContainer = document.getElementById('inline-message');
        if (inlineContainer) {
            inlineContainer.textContent = message;
            inlineContainer.style.display = 'block';
            setTimeout(() => {
                inlineContainer.style.display = 'none';
            }, duration);
            return inlineContainer;
        }

        // Toast flotante original
        const container = getToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        
        let icon = '';
        switch(type) {
            case 'success':
                icon = '<i class="fas fa-check-circle"></i>';
                break;
            case 'error':
                icon = '<i class="fas fa-exclamation-circle"></i>';
                break;
            case 'warning':
                icon = '<i class="fas fa-exclamation-triangle"></i>';
                break;
            case 'info':
                icon = '<i class="fas fa-info-circle"></i>';
                break;
            default:
                icon = '<i class="fas fa-bell"></i>';
        }
        
        toast.innerHTML = `
            ${icon}
            <div class="toast-content">
                <p class="toast-message">${escapeHtml(message)}</p>
            </div>
            <button class="toast-close" onclick="this.closest('.toast-notification').remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(toast);
        
        let timeoutId = setTimeout(() => {
            removeToast(toast);
        }, duration);
        
        toast.addEventListener('mouseenter', () => {
            clearTimeout(timeoutId);
        });
        
        toast.addEventListener('mouseleave', () => {
            timeoutId = setTimeout(() => {
                removeToast(toast);
            }, 1500);
        });
        
        return toast;
    };
    
    function removeToast(toast) {
        toast.classList.add('hiding');
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 300);
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Convertir mensajes de Django existentes a toasts
    function convertDjangoMessagesToToasts() {
        const messagesContainer = document.querySelector('.contenedor-mensajes');
        if (messagesContainer) {
            const messages = messagesContainer.querySelectorAll('.mensaje');
            messages.forEach(msg => {
                let type = 'info';
                if (msg.classList.contains('mensaje-success')) type = 'success';
                else if (msg.classList.contains('mensaje-error')) type = 'error';
                else if (msg.classList.contains('mensaje-warning')) type = 'warning';
                
                const text = msg.textContent.trim();
                if (text) {
                    showToast(text, type);
                }
            });
            messagesContainer.style.display = 'none';
        }
        
        // También buscar mensajes de Bootstrap alerts
        const alertContainer = document.querySelector('.messages-container');
        if (alertContainer) {
            const alerts = alertContainer.querySelectorAll('.alert');
            alerts.forEach(alert => {
                let type = 'info';
                if (alert.classList.contains('alert-success')) type = 'success';
                else if (alert.classList.contains('alert-danger')) type = 'error';
                else if (alert.classList.contains('alert-warning')) type = 'warning';
                
                const text = alert.textContent.trim();
                if (text) {
                    showToast(text, type);
                }
            });
            alertContainer.style.display = 'none';
        }
    }
    
    document.addEventListener('DOMContentLoaded', convertDjangoMessagesToToasts);
    
    if (typeof Turbolinks !== 'undefined') {
        document.addEventListener('turbolinks:load', convertDjangoMessagesToToasts);
    }
})();
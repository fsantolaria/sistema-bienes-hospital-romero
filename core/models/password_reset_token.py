from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import secrets

User = get_user_model()

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'core_password_reset_token'
    
    def __str__(self):
        return f"Reset token para {self.user.username}"
    
    @staticmethod
    def generate_token():
        """Genera un token seguro único."""
        return secrets.token_urlsafe(32)
    
    def is_valid(self):
        """Verifica si el token es válido (no expirado ni usado)."""
        expiry_time = self.created_at + timedelta(hours=24)
        return not self.is_used and timezone.now() < expiry_time

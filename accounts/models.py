import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_code():
    """Generate a random 6-digit numeric verification code."""
    return ''.join(random.choices(string.digits, k=6))


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    code = models.CharField(max_length=6, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} — {"✓" if self.is_verified else "✗"}'

    def regenerate_code(self):
        self.code = generate_code()
        self.save()


class GameScore(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    score      = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', 'achieved_at']

    def __str__(self):
        return f'{self.user.username} — {self.score} pts'


from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Account(models.Model):
    PLAN_CHOICES = (
        ('free', 'Gratis'),
        ('starter', 'Inicio'),
        ('professional', 'Profesional'),
        ('enterprise', 'Empresarial'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owned_account')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    active = models.BooleanField(default=True)
    domain = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cuenta')
        verbose_name_plural = _('Cuentas')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class AccountUser(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('agent', 'Agente'),
        ('manager', 'Gerente'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['account', 'user']
        verbose_name = _('Usuario de Cuenta')
        verbose_name_plural = _('Usuarios de Cuenta')

    def __str__(self):
        return f'{self.user.email} - {self.account.name} ({self.role})'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    availability = models.CharField(
        max_length=20,
        choices=(
            ('online', 'En línea'),
            ('busy', 'Ocupado'),
            ('away', 'Ausente'),
            ('offline', 'Desconectado'),
        ),
        default='offline'
    )
    last_seen = models.DateTimeField(auto_now=True)
    auto_response_enabled = models.BooleanField(default=False)
    auto_response_text = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfiles')

    def __str__(self):
        return f'Perfil de {self.user.email}'

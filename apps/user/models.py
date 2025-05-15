import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from .choices import UserRole
from helpers.generate_short_id import generate_short_id


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)

        # Generate username if not provided
        if not extra_fields.get("username"):
            first_name = extra_fields.get("first_name", "")
            last_name = extra_fields.get("last_name", "")

            # Try to create username from first and last name
            if first_name and last_name:
                base_username = f"{first_name.lower()}{last_name.lower()}"
            # If no first and last name, use email prefix
            else:
                base_username = email.split("@")[0]

            # Remove special characters and spaces
            base_username = "".join(e for e in base_username if e.isalnum())

            # Make sure username is unique by adding random numbers if needed
            username = base_username
            while self.model.objects.filter(username=username).exists():
                # Generate at least 5 random digits
                random_suffix = "".join(random.choices(string.digits, k=5))
                username = f"{base_username}{random_suffix}"

            extra_fields["username"] = username

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # User Details
    email = models.EmailField(unique=True, max_length=50)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    username = models.CharField(max_length=50, unique=True, blank=True)
    role = models.CharField(
        max_length=15,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    # Email Verification
    email_verification_token = models.CharField(max_length=255, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Flags
    last_login = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_sign_in = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        db_table = "users"

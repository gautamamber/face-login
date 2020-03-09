from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


class BaseModel(models.Model):
    """
    Base model which contains UUID, created_at, updated_at
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    Base user for creating user and super user
    """
    user_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields):
        """
        Create and save user with given email and password
        :param email:
        :param password:
        :param is_staff:
        :param is_superuser:
        :param extra_fields:
        :return:
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser
                          , **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        """
        Create normal user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Create super user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """
    Create custom user
    """
    HEAD = 1
    EMPLOYEE = 2
    ROLE_CHOICES = (
        (HEAD, 'Head'),
        (EMPLOYEE, 'Employee')
    )
    email = models.EmailField(unique=True, db_index=True)
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin site.')

    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as '
                                                            'active. Unselect this instead of deleting accounts.')
    dob = models.CharField(max_length=100, blank=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=HEAD)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    def __str__(self):
        """
        return user
        :return:
        """
        return str(self.email)

    def get_full_name(self):
        """
        return full name
        :return:
        """
        return "{}-{}".format(self.first_name, self.last_name)

    @property
    def is_head(self):
        """
        check user is head
        :return:
        """
        return self.role == self.HEAD

    @property
    def is_employee(self):
        """
        check user is employee
        :return:
        """

        return self.role == self.EMPLOYEE


class ReferralEmployee(BaseModel):
    """
    refer employee for signup
    """
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Referral"
        verbose_name_plural = "Referral"

    def __str__(self):
        """
        return user
        :return:
        """
        return str(self.email)

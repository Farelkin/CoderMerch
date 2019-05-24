from django.db import models
from django.conf import settings
import datetime, calendar
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


def image_path(instance, filename):
    return f'users_avatars/{instance.username.lower()}/{filename}'


def reduce_years():
    _date = datetime.date.today()
    month = _date.month - 1
    year = _date.year + month // 12 - 18
    month = month % 12 + 1
    day = min(_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, date_of_birth, password=None):
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            first_name=first_name,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            first_name=first_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    username = None
    email = models.EmailField(verbose_name='e-mail', unique=True)

    date_of_birth = models.DateField(verbose_name='birth date',
                                     default=reduce_years())
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'date_of_birth']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class CustomUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True,
                                null=False,
                                db_index=True, on_delete=models.CASCADE,
                                related_name='profile')

    patronymic = models.CharField(verbose_name='patronymic', max_length=150,
                                  blank=True)

    gender = models.CharField(verbose_name='gender', max_length=1,
                              choices=GENDER_CHOICES, blank=True)

    avatar = models.ImageField(upload_to=image_path,
                               blank=True,
                               default='',
                               )

    phone = PhoneNumberField(verbose_name='phone', blank=True)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CustomUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class ShippingAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True,
                                null=False,
                                db_index=True, on_delete=models.CASCADE,
                                related_name='address')

    name = models.CharField('Full name', max_length=128, )

    intercom = models.CharField('Intercom code', max_length=12, blank=True, )

    floor = models.IntegerField('Floor number', blank=True, )

    entrance = models.IntegerField('Entrance number', blank=True, )

    premise = models.CharField('Premise number', max_length=12, )

    street = models.CharField('Street name', max_length=512, )

    postal_code = models.CharField('Postal code', max_length=12, )

    city = models.CharField('City', max_length=64, )

    country = models.CharField('Country', max_length=128, )

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

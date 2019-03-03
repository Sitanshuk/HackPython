from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

class Loan(models.Model):
    l_id = models.BigIntegerField(primary_key=True)
    t = models.ForeignKey('Transaction', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan'

class Transaction(models.Model):
    t_id = models.BigIntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=10, blank=True, null=True)
    amount = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'transaction'

class Deposit(models.Model):
    d_id = models.BigIntegerField(primary_key=True)
    t = models.ForeignKey('Transaction', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deposit'
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    credit_score = models.BigIntegerField(blank=True, null=True)
    account_bal = models.BigIntegerField(blank=True, null=True)
    base_limit = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

class Userd(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    credit_score = models.BigIntegerField(blank=True, null=True)
    base_limit = models.BigIntegerField(blank=True, null=True)
    balance = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userd'

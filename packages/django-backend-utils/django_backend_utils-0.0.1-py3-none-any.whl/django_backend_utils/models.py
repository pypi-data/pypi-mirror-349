from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    organisation = models.ForeignKey('Organisation', on_delete=models.SET_NULL, related_name='role_organisation', null=True)

    def __str__(self):
        return self.name

class Organisation(models.Model):
    name = models.CharField(max_length=128, unique=True)
    primaryPhoneNumber = models.CharField(max_length=128, unique=True)
    admin = models.OneToOneField('CustomUser', on_delete=models.SET_NULL, related_name='admin_organisation', null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, related_name="user_organisation", null=True, blank=True)
    firebase_uid = models.CharField(max_length=128, unique=True)
    roles = models.ManyToManyField(Role, related_name='roles_users')

    def __str__(self):
        return self.username

    def get_roles_array(self):
        return [{role.name: True} for role in self.roles.all()]

    def has_superadmin_role(self):
        return any(r.get("superadmin") or r.get("super_admin") for r in self.get_roles_array())

    def belongs_to_an_organisation(self):
        return self.organisation is not None

    def saveUser(self, user, *args, **kwargs):
        self.organisation = user.organisation
        super().save(*args, **kwargs)

    @staticmethod
    def filter_by_user_role(queryset, user):
        if user.has_superadmin_role():
            return queryset
        return queryset.filter(organisation=user.organisation)

class RbacTasks(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="rbac_organisation", null=True, blank=True)
    urlPath = models.CharField(max_length=128, null=True, blank=True)
    task = models.CharField(max_length=128, unique=True, null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name='rbac_users', blank=True)

    def __str__(self):
        return self.task + " for path - " + self.urlPath

    def validateOrganisation(self, user):
        # Ensure the admin user belongs to this organisation
        if user.organisation is not self.organisation and not user.has_superadmin_role():
            raise ValidationError("Admin user must belong to this organisation.")

    def saveTask(self, *args, **kwargs):
        self.validateOrganisation(user)
        self.organisation = user.organisation
        super().save(*args, **kwargs)

    @staticmethod
    def filter_by_user_role(queryset, user):
        if user.has_superadmin_role():
            return queryset
        return queryset.filter(organisation=user.organisation)

    def get_roles_array(self):
        return [{role.name: True} for role in self.roles.all()]
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

#-------------------------------------------------------------------------------
#   A Custom usermanager to make it so that usernames are case insensitive.
#   Useful especially since usernames are emails.
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

#-------------------------------------------------------------------------------
#   Model for all users.
#   adminUser:      whether or not this is an admin account

class UserInfo(AbstractUser):
    objects = CustomUserManager()
    adminUser = models.BooleanField(default=False)
from django.forms import ModelForm
from apps.users.models import User

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        exclude = ('date_joined', "password", "is_active", "is_staff")

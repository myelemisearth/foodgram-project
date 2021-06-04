from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django import forms


User = get_user_model()

class CreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')

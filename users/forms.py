from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label="Фото (необязательно)")
    phone_number = forms.CharField(required=False, label="Телефон (необязательно)")
    country = forms.CharField(required=False, label="Страна (необязательно)")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'phone_number', 'country')

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя или Email",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_username(self):
        username_or_email = self.cleaned_data.get('username')
        if '@' in username_or_email:
            try:
                user = CustomUser.objects.get(email=username_or_email)
                return user.username
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")
        return username_or_email
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    """Extended sign-up form that requires email."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@example.com',
        }),
        help_text='Required. A verification code will be sent here.',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a strong password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Repeat your password',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # Stays inactive until email is verified
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Login form with styled inputs."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your password',
        }),
    )


class VerifyEmailForm(forms.Form):
    """Form for entering the 6-digit email verification code."""
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input code-input',
            'placeholder': '000000',
            'maxlength': '6',
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
            'autocomplete': 'one-time-code',
            'autofocus': True,
        }),
        label='Verification Code',
    )

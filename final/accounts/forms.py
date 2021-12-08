from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)


class CustomUserCreationForm(UserCreationForm):
    zipcode = forms.CharField(
        label='우편번호',
        required=True,
    )
    phone = forms.CharField(
        label='전화번호',
        required=True,
    )
    address = forms.CharField(
        label='주소',
        required=True,
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email','phone', 'address', 'zipcode')
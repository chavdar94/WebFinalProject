from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from .models import UserProfile

UserModel = get_user_model()


class RegisterForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__clear_fields_helper_text()

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = UserProfile(
            user=user,
        )
        if commit:
            profile.save()
        return user

    def __clear_fields_helper_text(self):
        for field in self.fields.values():
            # field.help_text = ''
            field.widget.attrs['class'] = 'bg-slate-200 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'


class ProfileUpdateForm(forms.ModelForm):
    # password = None

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'age', 'city', 'profile_picture',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_field_classes()
        self.fields['profile_picture'].widget.attrs.update(
            {'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})

    def __set_field_classes(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'bg-slate-200 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'


class SignInForm(auth_forms.AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_field_classes()

    def __set_field_classes(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'bg-slate-200 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'


class PasswordChangeForm(auth_forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_field_classes()

    def __set_field_classes(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'bg-slate-200 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'

    class Meta:
        model = UserModel

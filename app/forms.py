from django import forms
from django.forms.widgets import Input
from .models import Activity


class MultipleFileInput(Input):
    """
    Bypasses Django's FileInput restriction on multiple files
    by subclassing Input directly instead of FileInput.
    """
    input_type = 'file'
    needs_multipart_form = True
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        final_attrs = {'multiple': True}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    def value_from_datadict(self, data, files, name):
        return files.getlist(name)

    def value_omitted_from_data(self, data, files, name):
        return name not in files

    def format_value(self, value):
        return None  # file inputs never show existing value


class MultipleFileField(forms.FileField):
    """FileField that accepts and validates a list of uploaded files."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # data is a list from value_from_datadict
        if not data:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return []
        result = []
        for f in data:
            result.append(super().clean(f, initial))
        return result


class ActivityForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        label='Photos & Documents',
        widget=MultipleFileInput(attrs={'accept': 'image/*,application/pdf,.doc,.docx,.xls,.xlsx,.txt'})
    )

    class Meta:
        model = Activity
        fields = ['team_name', 'members', 'description', 'date']
        widgets = {
            'team_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Beta Team 4',
            }),
            'members': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Boomitha, Ashis, Ashok, Ethirajan',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'What did your team work on today?',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
        }


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create password',
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter password',
        })
    )

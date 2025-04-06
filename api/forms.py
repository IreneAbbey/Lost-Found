from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password', 'phone_number', 'location', 'role']

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match.')
            

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'email', 'phone_number', 'location', 'vehicle_type', 'vehicle_number']
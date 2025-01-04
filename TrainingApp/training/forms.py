from django import forms
from .models import User, Workout, Achievement

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'created_by', 'steps', 'difficulty', 'duration']

class SpecialWorkoutForm(forms.ModelForm):
    achievement = forms.ModelChoiceField(queryset=Achievement.objects.all(), required=True)

    class Meta:
        model = Workout
        fields = ['title', 'difficulty', 'duration', 'steps', 'achievement']



from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Announcement title'}),
            'body': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your announcement...'}),
        }

from django import forms
from .models import WarParticipation

class TagForm(forms.ModelForm):

    class Meta:
        model = WarParticipation
        fields = ('player_tag',)

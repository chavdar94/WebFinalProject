from django import forms

from .models import Topic


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)

from django import forms

from ..models import Topic


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_fields_classes()

    def __set_fields_classes(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'rounded-xl w-3/4 bg-slate-300 text-lg font-["Poppins"]'

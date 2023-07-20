from django import forms

from ..models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_fields_classes()

    def __set_fields_classes(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'rounded-xl bg-slate-300 text-lg font-["Poppins"]'


class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_disabled_fields()

    def __set_disabled_fields(self):
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.required = False


class CommentCreateForm(forms.ModelForm):
    class Meta:
        fields = ('body',)
        model = Comment
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_fields_classes()

    def __set_fields_classes(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'rounded-xl bg-slate-300 text-lg font-["Poppins"]'

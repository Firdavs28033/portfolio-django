from django.forms import ModelForm, CheckboxSelectMultiple

from base.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        widgets = {
                'tags': CheckboxSelectMultiple(),
            }
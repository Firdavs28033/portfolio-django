import django_filters
from django_filters import CharFilter

from django import forms

from .models import Tags, Post

class PostFilter(django_filters.FilterSet):
	headline = CharFilter(field_name='headline', lookup_expr="icontains", label='Headline')
	tags = django_filters.ModelMultipleChoiceFilter(queryset=Tags.objects.all(),
		widget=forms.CheckboxSelectMultiple
		)
	class Meta:
		model = Post
		fields = ['headline', 'tags']
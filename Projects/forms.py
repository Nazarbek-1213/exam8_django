# Projects/forms.py

from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'category',
            'budget_type',
            'budget_min',
            'budget_max',
            'level',
            'skills',
            'deadline',
        ]
        # 'client' va 'status' YO'Q — view da qo'shiladi

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'masalan: Django REST API + React frontend',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 6,
                'placeholder': 'Loyiha haqida batafsil yozing…',
            }),
            'category': forms.RadioSelect(attrs={
                'class': 'cat-option',
            }),
            'budget_type': forms.RadioSelect(attrs={
                'class': 'budget-option',
            }),
            'budget_min': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '100',
                'min': 0,
            }),
            'budget_max': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '500',
                'min': 0,
            }),
            'level': forms.RadioSelect(attrs={
                'class': 'level-option',
            }),
            'skills': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Python, Django, React…',
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
        }
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'tags', 'users', 'has_frequency', 'frequency', 'frequency_detail']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['due_date'].widget.attrs['class'] = 'datepicker'
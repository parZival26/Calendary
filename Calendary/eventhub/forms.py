from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions
from .models import Task, Tag

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'tags', 'state']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # Filtrar las etiquetas que pertenecen al usuario
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(users=user)
        
        # Establecer el atributo 'class' para el widget de fecha
        self.fields['due_date'].widget.attrs['class'] = 'datepicker'
        
        # Crear un objeto FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            'due_date',
            'tags',
            'state',
            FormActions(
                Submit('submit', 'Guardar', css_class='btn btn-primary')
            )
        )
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['color'].widget.attrs['class'] = 'colorpicker'
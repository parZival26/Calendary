from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions
from .models import Task, Tag

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'tags', 'state']

        widgets = {
                'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # Filtrar las etiquetas que pertenecen al usuario
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(users=user)
            

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form_inputs" 
        
        # Establecer el atributo 'class' para el widget de fecha
        self.fields['due_date'].widget = forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'})
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
        self.fields['color'].widget = forms.TextInput(attrs={'type':'color', 'id':'id_color'})
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import TeacherProfile, StudentProfile, Location, Classes, Availability


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña', required=True)
    
    ROLE_CHOICES = [
        ('', 'Seleccione un rol'),
        ('teacher', 'Profesor'),
        ('student', 'Estudiante'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol', required=True)
    # EL CAMPO DE ROLE NO ES UN ATRIBUTO(COLUMNA) DE LA TABLA USER, SOLO SE USA PARA ASIGNACIÓN DE GRUPO
    # EN LA FUNCIÓN create_profile DE signals.py

    class Meta:
        model   = User
        fields  = ['first_name', 'last_name', 'email', 'username', ]
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'username': forms.TextInput(),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'username': 'Usuario',
        }
        help_texts = {
            'username': ''
        }

    def clean(self):
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        first_name  = cleaned_data.get('first_name')
        last_name  = cleaned_data.get('last_name')
        if first_name:
            cleaned_data['first_name'] = first_name.upper()
        if last_name:
            cleaned_data['last_name'] = last_name.upper()

        email = cleaned_data.get('email')
        if email:
            cleaned_data['email'] = email.lower()

            

        if password1 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')

        return cleaned_data
        

        # Group inclusion must be done after user is saved            
    def save(self, commit=False):
        new_user =  super().save(commit=False)
        new_user.set_password(self.cleaned_data['password1'])
        new_user.save()

        role = self.cleaned_data.get('role')
        if role == "teacher":
            group = Group.objects.get(name="Teachers")
            new_user.groups.add(group)
            TeacherProfile.objects.create(user=new_user)
        elif role == "student":
            group = Group.objects.get(name="Students")
            new_user.groups.add(group)
            StudentProfile.objects.create(user=new_user)
        


        return new_user


class TeacherForm(forms.ModelForm):
    
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label="Seleccione una ubicación",
        label="Ubicación"
    )

    class Meta:
        model = TeacherProfile
        fields = ['years_of_experience', 'educational_level', 'bio', 'location']

        labels = {
            'years_of_experience': 'Años de experiencia',
            'educational_level': 'Nivel educativo',
            'bio': 'Bio',
            'location': 'Ubicación'
        }


class StudentForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['interests']
        labels = {
            'interests': 'Intereses',
        }

    
class ClassForm(forms.ModelForm):

    class Meta:
        model = Classes
        # location debe vincularse con el dato del maestro
        fields = ['name', 'description', 'category', 'price']
        labels = {
            'name' : 'Nombre', 
            'description' : 'Descripción', 
            'category' : 'Category', 
            'price' : 'Precio'
        }

    


class AvailabilityForm(forms.ModelForm):
    
    class Meta:
        model = Availability
        fields = ['days', 'start_time', 'end_time']
        labels = {
            'days': "Día",
            'start_time': 'Hora de inicio',
            'end_time': 'Hora de fin'
        }
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


AvailabilityFormSet = modelformset_factory(
    Availability,
    form=AvailabilityForm,
    extra=1
)



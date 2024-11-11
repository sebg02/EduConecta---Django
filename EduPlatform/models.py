from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    city = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f"{self.city}"


class TeacherProfile(models.Model):
    LEVELS_OF_EDUCATION = [
        ('basic', 'Bachillerato'),
        ('technical', 'Técnica'),
        ('technological', 'Tecnológico'),
        ('BD', 'Profesional'),
        ('PD', 'Posgrado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    years_of_experience = models.IntegerField(null=False, default=0)
    educational_level = models.CharField(
        max_length=13, choices=LEVELS_OF_EDUCATION)
    bio = models.TextField()
    location = models.OneToOneField(
        Location, on_delete=models.SET_NULL, null=True)
    list_of_classes = models.ManyToManyField('Classes')

    def __str__(self):
        return f"{self.user}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    list_of_classes = models.ManyToManyField('Classes')
    interests = models.TextField()

    def __str__(self):
        return f"{self.user}"


class Availability(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Lunes'),
        ('Tue', 'Martes'),
        ('Wed', 'Miércoles'),
        ('Thu', 'Jueves'),
        ('Fri', 'Viernes'),
        ('Sat', 'Sábado'),
        ('Sun', 'Domingo'),
    ]
    days = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_obj = models.ForeignKey('Classes', on_delete=models.CASCADE, related_name='availabilities')

    def __str__(self):
        return f"{self.get_days_display()} desde {self.start_time} hasta {self.end_time}"


class Classes(models.Model):
    CLASS_CATEGORIES = [
        ('tech', 'Tecnología'),
        ('lang', 'Idiomas'),
        ('scho', 'Materias escolares'),
        ('art', 'Arte'),
        ('cook', 'Cocina'),
        ('DIY', 'Manualidades'),
        ('bsns', 'Negocios'),
        ('oth', 'Otros'),
    ]

    name = models.CharField(max_length=50, null=False)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=4, choices=CLASS_CATEGORIES)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.name}"
    



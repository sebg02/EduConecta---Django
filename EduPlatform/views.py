from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm, StudentForm, TeacherForm, ClassForm, AvailabilityForm
from .models import TeacherProfile, StudentProfile, Classes
from .decorators import unauthenticated_user, redirecter_based_on_group


# LANGING PAGE
def index(request):
    if request.method == "GET":
        return render(request, 'index.html')


# ----------------------------- USERS MANAGEMENT -----------------------------
# SIGN IN (should have decorator for authenticated user to not access this)
@unauthenticated_user
def sign_in(request):
    if request.method == "GET":
        return render(request, 'signin.html', {'form': UserForm})
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save()
                login(request, new_user)
                return redirect_complementary_forms(request, new_user)
            except Exception as e:
                print(e)
                return render(request, 'signin.html',
                              {'error': 'Ha ocurrido un error'})
        return render(request, 'signin.html', {'form': form})


# LOG IN
@unauthenticated_user
def log_in(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'login.html',
                          {'error': "Usuario o contraseña incorrecta"})
        else:
            login(request, user)
            if user.groups.filter(name="Teachers").exists():
                teacher = TeacherProfile.objects.get(user=user)
                if not teacher.years_of_experience:
                    return redirect_complementary_forms(request, user)
                else:
                    return redirect('home')
            elif user.groups.filter(name="Students").exists():
                student = StudentProfile.objects.get(user=user)
                if not student.interests:
                    return redirect_complementary_forms(request, user)
                else:
                    return redirect('home')


# REDIRECTION TO COMPLEMENTARY FORMS AFTER CREATION OF USER
@login_required
def redirect_complementary_forms(request, user):
    if user.groups.filter(name="Teachers").exists():
        return redirect('edit-teacher')
    elif user.groups.filter(name="Students").exists():
        return redirect('edit-student')


# LOG OUT
@login_required
def log_out(request):
    logout(request)
    return redirect('index')


# HOME PAGE FOR AUTHENTICATED USERS
@login_required
def home(request):
    user_role = [group.name for group in request.user.groups.all()]
    if "Teachers" in user_role:
        teacher = TeacherProfile.objects.get(user=request.user)
        classes = teacher.list_of_classes.all()
        context = {'role': user_role, 'classes': classes}

        return render(request, 'home.html', context)

    classes = Classes.objects.all()
    context = {'role': user_role, 'classes': classes}    
    return render(request, 'home.html', context)


# EDIT TEACHER PROFILE VIEW
@login_required
@redirecter_based_on_group(allowed_roles=["Teachers"])
def edit_profile_teacher(request):
    if request.method == "GET":
        return render(request, 'edit/edit-teacher-profile.html',
                    {'form': TeacherForm})
    elif request.method == "POST":
        form = TeacherForm(request.POST, instance=request.user.teacherprofile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TeacherForm(request.POST, instance=request.user.teacherprofile)
    return render(request, 'edit/edit-teacher-profile.html',
                    {'form': form})


# EDIT STUDENT PROFILE VIEW
@login_required
@redirecter_based_on_group(allowed_roles=["Students"])
def edit_profile_student(request):
    if request.method == "GET":
        return render(request, 'edit/edit-student-profile.html',
                    {'form': StudentForm})
    elif request.method == "POST":
        form = StudentForm(request.POST, instance=request.user.studentprofile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = StudentForm(instance=request.user.studentprofile)
    return render(request, 'edit/edit-student-profile.html', {'form': form})




# DELETE USER, PROFILE AND DATA WITHIN THEM (Add some type of confimation both from front and backend)
# considering this shouldn't be accessible with just the url, don't just put in the nav, this should be in a configuration page
# or maybe even in edit profile, confirmation using password or checkbox
@login_required
def delete_user(request):
    if request.method == "POST":
        try:
            user_to_delete = User.objects.get(username=request.user)
            logout(request)
            user_to_delete.delete()
            return redirect('index')
        except Exception as e:
            print(e)
            return render(request, 'edit/delete-user.html',
                          {'error': "Ha ocurrido un error, inténtelo más tarde"})
    return render(request, 'edit/delete-user.html')


# ---------------------------- CLASSES MANAGEMENT ----------------------------


# CREAR CLASE
@login_required
@redirecter_based_on_group(allowed_roles=["Teachers"])
def create_class(request):
    if request.method == "GET":
        return render(request, 'EduClasses/create-class.html', {
            'form': ClassForm(),
            'formset': AvailabilityForm()
        })
    elif request.method == "POST":
        class_form = ClassForm(request.POST)
        av_form = AvailabilityForm(request.POST)

        if class_form.is_valid() and av_form.is_valid():
            new_class = class_form.save(commit=False)

            teacher = TeacherProfile.objects.get(user=request.user)         
            new_class.location = teacher.location
            new_class.teacher = teacher
            new_class = class_form.save()

            teacher.list_of_classes.add(new_class)
            availability_instance = av_form.save(commit=False)
            availability_instance.class_obj = new_class
            availability_instance.save()


            return redirect("home")

        return render(request, 'EduClasses/create-class.html', {
            'form': ClassForm(),
            'av_form': AvailabilityForm()
        })


# EDITAR CLASE
@login_required
@redirecter_based_on_group(allowed_roles=["Teachers"])
def edit_class(request, class_id):
    pass


# ELIMINAR CLASE
@login_required
@redirecter_based_on_group(allowed_roles=["Teachers"])
def delete_class(request, class_id):
    if request.method == "POST":
        class_to_delete = Classes.objects.get(id=class_id)
        class_to_delete.delete()
        return redirect("home")


# FILTRAR CLASES
@login_required
def filter_classes(request):
    response = request.GET
    class_name = response.get('className')
    city_name = response.get('cityName')
    educational_level = response.get('educationalLevel')
    
    classes = Classes.objects.all()

    if class_name:
        classes = classes.filter(name__icontains=class_name)
    if educational_level:
        classes = classes.filter(teacher__educational_level=educational_level)
    if city_name:
        classes = classes.filter(location__city__icontains=city_name)
    

    return render(request, "home.html", {'role': "Students",'classes': classes})


        




# ADMINISTRAR REGISTRO EN CLASES
@login_required
@redirecter_based_on_group(allowed_roles=["Teachers"])
def handle_enrollment_request(request):
    pass

        
# ENVIAR SOLICITUD DE REGISTRO A CLASE
@login_required
@redirecter_based_on_group(allowed_roles=["Students"])
def send_enrollment_request(request):
    pass



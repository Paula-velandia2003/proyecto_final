from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import MascotaForm
from .models import Mascota
from django.http import HttpResponseForbidden  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:   
            try:
                user = User.objects.create_user(username = request.POST['username'],
                password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('lista_mascotas')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'El usuario ya existe'})
        return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Las contraseñas no coinciden'})


@login_required    
def lista_mascotas(request):
    busqueda = request.GET.get("buscar")
    mascotas = Mascota.objects.filter(user=request.user)

    if request.user.is_authenticated:
        if busqueda:
            mascotas = Mascota.objects.filter(
                Q(nombre__icontains = busqueda)|
                Q(especie__icontains = busqueda)|
                Q(edad__icontains = busqueda)
            ).distinct()
                                              
    
    return render(request, 'mascotas.html', {'mascotas': mascotas})
    


@login_required
def create_mascotas(request):

    if request.method == 'GET':
        return render(request, 'create.html', {
            'form':MascotaForm
        })
    else:
        try:
            form = MascotaForm(request.POST)
            new_mascota = form.save(commit = False)
            new_mascota.user = request.user
            new_mascota.save()
            return redirect('lista_mascotas')
        except ValueError:
            return render(request, 'create.html', {
                'form':MascotaForm,
                'error':'Por favor valide los datos'
            })

@login_required
def mascota_detail(request, mascota_id):
    if request.method == 'GET':
        mascota = get_object_or_404(Mascota, pk=mascota_id, user=request.user)
        form = MascotaForm(instance=mascota)
        return render(request,'mascota_detail.html',{'mascota': mascota, 'form' : form})
    else:
        try:
            mascota = get_object_or_404(Mascota, pk=mascota_id, user=request.user)
            form = MascotaForm(request.POST, instance=mascota)
            form.save()
            return redirect('lista_mascotas')
        except ValueError:
            return render(request,'mascota_detail.html',{'mascota': mascota, 'form' : form, 'error' : "error al actualizar mascota"})

@login_required
def delete_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id, user=request.user)
    if request.method == 'POST':
        mascota.delete()
        return redirect('lista_mascotas')


@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'El usuario o la contraseña son incorrectos'})
        else:
            login(request, user)
            return redirect('lista_mascotas')



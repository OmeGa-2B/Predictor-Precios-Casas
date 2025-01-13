from django.shortcuts import redirect, render
#template de predicciones
from .forms import PredictForm
import joblib  # Para cargar el modelo guardado
import warnings
import os
from django.conf import settings
#registro de usuaraios
from .forms import RegisterForm
from .models import Casas
#login de usuario
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
from django.shortcuts import get_object_or_404
from .forms import EditProfileForm
#comentarios
from .models import Comentario
from .forms import ComentarioForm

# Cargar el modelo predictivo
MODEL_PATH = os.path.join(settings.BASE_DIR, 'analisis_casas_app', 'static', 'models_p', 'modelo_entrenado_analisis_casas.joblib')

# Cargar el modelo predictivo
model = joblib.load(MODEL_PATH)

@login_required
def predict_price(request):
    prediction = None  # Para almacenar el precio predicho
    if request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            features = [
                data['bedrooms'],
                data['bathrooms'],
                data['sqft_living'],
                data['sqft_lot'],
                data['floors'],
                data['waterfront'],
                data['view'],
                data['condition'],
                data['grade'],
                data['sqft_above'],
                data['sqft_basement'],
                data['yr_built'],
                data['yr_renovated'] or 0,  # Si no está renovado, usar 0
                data['zipcode'],
            ]
            prediction = model.predict([features])[0]

            # Si el usuario decide guardar la predicción
            if 'save_prediction' in request.POST:
                # Guardar la predicción en el modelo `Casas`
                Casas.objects.create(
                    usuario_fk=request.user,
                    bedrooms=data['bedrooms'],
                    bathrooms=data['bathrooms'],
                    sqft_living=data['sqft_living'],
                    sqft_lot=data['sqft_lot'],
                    floors=data['floors'],
                    waterfront=data['waterfront'],
                    view=data['view'],
                    condition=data['condition'],
                    grade=data['grade'],
                    sqft_above=data['sqft_above'],
                    sqft_basement=data['sqft_basement'],
                    yr_built=data['yr_built'],
                    yr_renovated=data['yr_renovated'] or 0,
                    zipcode=data['zipcode'],
                    predicted_price=prediction
                )
                return redirect('profile')  # Redirige al perfil del usuario
    else:
        form = PredictForm()

    return render(request, 'predict.html', {'form': form, 'prediction': prediction})

def home(request):
    # Lógica para comentarios
    comentarios = Comentario.objects.all().order_by('-fecha_creacion')  # Cargar comentarios ordenados por fecha
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user  # Asociar comentario al usuario actual
            comentario.save()
            return redirect('index')  # Redirige al mismo index después de guardar
    else:
        form = ComentarioForm()

    # Contexto para la página principal
    context = {
        'average_price': 540088.14,  # Precio promedio
        'total_properties': 21613,  # Total de propiedades
        'total_regions': 20,  # Total de regiones analizadas
        'comentarios': comentarios,  # Pasar comentarios al contexto
        'form': form,  # Pasar formulario al contexto
    }
    return render(request, 'index.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'

@login_required
def profile_view(request):
    # Obtiene las casas asociadas al usuario
    casas = Casas.objects.filter(usuario_fk=request.user)

    if request.method == 'POST':
        # Manejo de la eliminación de una casa
        casa_id = request.POST.get('casa_id')
        casa = get_object_or_404(Casas, id=casa_id, usuario_fk=request.user)
        casa.delete()

    return render(request, 'profile.html', {'user': request.user, 'casas': casas})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirige al perfil del usuario después de editar
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
    
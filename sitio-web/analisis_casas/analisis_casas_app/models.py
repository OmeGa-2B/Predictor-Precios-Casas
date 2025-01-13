from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Casas(models.Model):
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='casas')
    bedrooms = models.PositiveIntegerField(verbose_name='bedrooms')
    bathrooms = models.PositiveIntegerField(verbose_name='bathrooms')
    sqft_living = models.PositiveIntegerField(verbose_name='sqft_living')
    sqft_lot = models.PositiveIntegerField(verbose_name='sqft_lot')
    floors = models.PositiveIntegerField(verbose_name='floors')
    waterfront = models.CharField(
        max_length=1,
        choices=[('0', 'No'), ('1', 'Sí')],
        verbose_name='waterfront'
    )
    view = models.PositiveIntegerField(default=0, verbose_name='view')
    condition = models.PositiveIntegerField(default=3, verbose_name='condition')
    grade = models.PositiveIntegerField(default=7, verbose_name='grade')
    sqft_above = models.PositiveIntegerField(verbose_name='sqft_above')
    sqft_basement = models.PositiveIntegerField(verbose_name='sqft_basement')
    yr_built = models.PositiveIntegerField(verbose_name='yr_built')
    yr_renovated = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='yr_renovated'
    )
    zipcode = models.CharField(max_length=10, verbose_name='zipcode')
    predicted_price = models.FloatField(null=True, blank=True, verbose_name='Predicted Price')

    def __str__(self):
        return f"Casa de {self.usuario_fk.username} - {self.zipcode}"


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(verbose_name='Comentario')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
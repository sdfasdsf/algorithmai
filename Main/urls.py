from django.urls import path
from . import views



urlpatterns = [
    path('config.js', views.config_js, name='config_js'),
    path('', views.Main.as_view(), name="Main"),
    path('movie/<int:movie_id>/', views.Movie.as_view(), name="movie"),


]
from django.urls import path
from .views import mark_list, model_list


urlpatterns = [
    path('mark/', mark_list, name='mark_list'),
    path('model/', model_list, name='model_list'),
]

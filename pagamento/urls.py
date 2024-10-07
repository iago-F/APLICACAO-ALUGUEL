from django.urls import path
from . import views

urlpatterns = [

    path('realizar_pagamento/<int:reserva_id>/', views.realizar_pagamento, name='realizar_pagamento'),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('', getRoutes, name="routes"),
    path('health/', health_check, name="health"),   # NEW — health check endpoint
    path('notes/', getNotes, name="notes"),
    path('notes/<str:pk>/update/', updateNote, name="update-note"),
    path('notes/<str:pk>/delete/', deleteNote, name="delete-note"),
    path('notes/create/', createNote, name="create-note"),
    path('notes/<str:pk>/', getNote, name="note"),
]

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RenderReadView

app_name = 'render'

render_router = DefaultRouter()
render_router.register(r'render', RenderReadView)

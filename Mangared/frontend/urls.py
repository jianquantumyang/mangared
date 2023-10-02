from django.urls import path
from . import views
urlpatterns = [
    path("",views.index),
    path('about/',views.index),
    path('login/',views.index),
    path('manga/<uuid:mangauuid>/',views.index),
    path('chapter/<uuid:uuid>/',views.index),
    path('popular/',views.index),
    path('discussion/',views.index),
    path('discussion/<uuid:uuid>/',views.index),

    path('folder/reading/',views.index),
    path('folder/plans/',views.index),
    path('folder/watched/',views.index),
    path('folder/abandoned/',views.index),
    path('folder/postponed/',views.index),
    path('search/',views.index),
    path('register/',views.index),
    path('catalog/',views.index)
]
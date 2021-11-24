from django.urls import path

from . import views

urlpatterns = [
    path("api_auth", views.api_auth, name="api_auth"),
    path("cars", views.cars, name="cars"),
    path("check_user", views.check_user, name="check_user"),
    path("", views.chat, name="chat"),
    path("discuss", views.discuss, name="discuss"),
    path("upload_file", views.upload_file, name="upload_file"),
    path("icon_recognition", views.icon_recognition, name="icon_recognition"),
    path("air_filter_analysis",views.air_filter_analysis,name="air_filter_analysis",),
    path("speech_to_text", views.speech_to_text, name="speech_to_text"),
    path("remove", views.remove, name="remove"),
]

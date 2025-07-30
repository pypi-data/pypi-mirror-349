from django.urls import path
from app import views

urlpatterns = [
    path("my_view/", views.my_view, name="my_view"),
    path("createNewUser/", views.createNewUser, name="createNewUser"),
    path("createOrganisation/", views.createOrganisation, name="createOrganisation"),
    path("getUserDetails/", views.getUserDetails, name="getUserDetails"),
    path("getOrganisationDetails/", views.getOrganisationDetails, name="getOrganisationDetails"),
]

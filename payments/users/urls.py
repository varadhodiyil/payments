from django.urls import path
from payments.users import views
urlpatterns = [
    path('', views.UserAPI.as_view() , name="users")
]
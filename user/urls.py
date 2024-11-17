from django.urls import path
from .views import CreateUserView
from .views import VerifyApi

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyApi.as_view(), name='verify')

]
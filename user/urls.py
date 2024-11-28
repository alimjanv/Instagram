from django.urls import path
from .views import CreateUserView, VerifyApi, GetNewVerification
urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyApi.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view(), name='verify_new')


]


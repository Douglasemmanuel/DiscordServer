from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class MyuserCreationForm(UserCreationForm):  #to enable a user create the user account
    class Meta:
        model = User
        fields =['name','username','email','password1','password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = {'host','participants'}  #to allow any user that is log-in to create a group not only the host 



class UserForm(ModelForm): #to enable a user update his profile details
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']

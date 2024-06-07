from rest_framework import serializers
import re
from .models import *


class LoginSerializer(serializers.Serializer):
    email_id=serializers.EmailField()
    password=serializers.CharField()




class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email_id','password']

    def validate_password(self,value):
        pw_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:"<>?])[A-Za-z\d!@#$%^&*()_+{}|:"<>?]{8,}$')
        if not pw_pattern.match(value) or len(value)>30:
            print(value)
            raise serializers.ValidationError('Password should contain atleast one uppercase, lowercase, number and special character.')
        return value
    
    def create(self,data):
        password=data.pop('password')
        user=User.objects.create(**data)
        user.set_password(password)
        user.save()
        return user
    
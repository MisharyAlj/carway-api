from rest_framework.authentication import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'nationality_id', 'phone', 'occupation', 'salary', 'password')

    def create(self, validated_data):
        user = CustomUser(first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                          email=validated_data['email'], nationality_id=validated_data[
                              'nationality_id'], phone=validated_data['phone'],
                          occupation=validated_data['occupation'], salary=validated_data['salary'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'nationality_id',
                  'phone', 'email', 'occupation', 'salary', 'is_active', 'last_login', 'date_joined')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name',
                  'occupation', 'phone', 'email')


class AuthTokenSerializer(serializers.Serializer):
    nationality_id = serializers.CharField(label=_("National ID"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        nationality_id = data.get('nationality_id')
        password = data.get('password')

        if nationality_id and password:
            user = authenticate(
                nationality_id=nationality_id, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is deactivated.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "national Id" and "password".')
            raise serializers.ValidationError(msg)

        data['user'] = user
        return data

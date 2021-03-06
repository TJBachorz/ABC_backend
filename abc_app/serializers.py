from .models import Account, Case, CaseLink, Incident
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
import pdb

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'antecedent', 'behavior', 'consequence', 'date', 'time', 'case']

class CaseObjectForAccountSerializer(serializers.ModelSerializer):
    incidents = IncidentSerializer(many=True)
    class Meta:
        model = Case
        fields = ['id', 'name', 'dob', 'incidents']

class AccountSerializer(serializers.ModelSerializer):
    cases = CaseObjectForAccountSerializer(many=True, required=False)
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'cases']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        account = Account.objects.create(**validated_data)
        return account

class CaseSerializer(serializers.ModelSerializer):
    incidents = IncidentSerializer(many=True, required=False)
    class Meta:
        model = Case
        fields = ['id', 'name', 'dob', 'incidents']  

class CaseLinkSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField(many=False, read_only=True)
    case = serializers.StringRelatedField(many=False, read_only=True)
    account_id = serializers.IntegerField(write_only=True)
    case_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = CaseLink
        fields = ['id', 'account', 'case', 'account_id', 'case_id']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only = True)
    token = serializers.CharField(max_length=255, read_only = True)
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email = email, password = password)
        if user is None:
            raise serializers.ValidationError('Incorrect username or password')
        try:
            # payload = api_settings.JWT_PAYLOAD_HANDLER('user_id': user['id'])
            payload = api_settings.JWT_PAYLOAD_HANDLER(user)
            token = api_settings.JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')
        return {
            'token': token,
            'email': user.email,
        }
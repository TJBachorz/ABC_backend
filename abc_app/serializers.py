from rest_framework import serializers
from .models import Account, Case, CaseLink

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email']

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'name', 'dob']
    
class CaseLinkSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField(many=True)
    case = serializers.StringRelatedField(many=True)
    class Meta:
        model = CaseLink
        fields = ['id', 'account', 'case']
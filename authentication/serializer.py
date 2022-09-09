from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from yaml import serialize
import logging

from authentication.models import User

logger = logging.getLogger(__name__)

class TokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        # token['username'] = user.name

        return token


class UserAccountSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'email', 'created_by', 'created_date', 'modified_by', 'modified_date')

    def create(self, validated_data):
        logger.info("Create was triggered.")
        user = User(
            phone_number=validated_data.get("phone_number"),
            email=validated_data.get("email"),
            name=validated_data.get("name"),
            created_by=validated_data.get("name"),
            modified_by=validated_data.get("name"),
        )
        user.save()
        return user
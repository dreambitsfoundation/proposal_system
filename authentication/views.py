from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework import status
from django.db import IntegrityError
from rest_framework.decorators import permission_classes
from authentication.custom_auth import UserViewPermission
from authentication.serializer import TokenObtainPairSerializer, UserAccountSerializer

from authentication.models import User

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

class UserView(APIView):
    """
    This view handles all the CRUD operation related to user
    """

    serializer = UserAccountSerializer
    permission_classes = (UserViewPermission,)

    def get(self, request):
        user_serialized = UserAccountSerializer(request.user)
        return Response(data=user_serialized.data)
    
    def post(self, request):
        user_serializer = UserAccountSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        try:
            user_serializer.save()

            # Set the user password
            password = request.data.get("password")
            user_serializer.instance.set_password(password)
            user_serializer.instance.save()
            return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise APIException(
                "Another user with same phone number already exists.")
        except Exception as e:
            raise APIException(e)

    def put(self, request):
        """
        We are not following the concept of ID in this case since
        only the authorized used can update itself.
        """
        serialized_user = UserAccountSerializer(request.user, data=request.data)
        serialized_user.is_valid(raise_exception=True)
        serialized_user.save()
        if "password" in request.data:
            password = request.data.get("password")
            serialized_user.instance.set_password(password)
            serialized_user.instance.save()
        return Response(data=serialized_user.data)

    def delete(self, request, pk=None):
        """
        One user can delete any user
        """
        # Fetch user account
        user = User.objects.filter(pk=pk)
        user = user.last()
        if not user:
            raise APIException("No User with the provided ID was found.")
        
        user_is_deleting_itself = user == request.user
        
        # Delete User
        user.delete()

        message = "User was successfully deleted."
        if user_is_deleting_itself:
            message = "You have deleted your account successful."

        return Response(data={
            "message": message
        }, status=status.HTTP_204_NO_CONTENT)
        


    



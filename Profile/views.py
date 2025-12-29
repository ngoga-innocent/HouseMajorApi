# Profile/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer,ProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.shortcuts import render
url='https://44550e797e53.ngrok-free.app/'
User = get_user_model()
token_generator = PasswordResetTokenGenerator()
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
    
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    serializer = ProfileSerializer(request.user)  # reuse or create a ProfileSerializer
    return Response(serializer.data)
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email', '').strip().lower()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "If that email exists, a reset link will be sent."}, status=200)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    reset_link = f"{url}/reset-password/{uid}/{token}/"

    # Render HTML email
    subject = "Password Reset Request"
    from_email = None
    html_content = render_to_string("emails/reset_password.html", {
        "full_name": user.full_name,
        "reset_link": reset_link
    })
    msg = EmailMultiAlternatives(subject, "", from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return Response({"message": "If that email exists, a reset link will be sent."}, status=200)

@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Invalid link"}, status=400)

    if not token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    new_password = request.data.get('password')
    if not new_password:
        return Response({"error": "Password is required"}, status=400)

    user.set_password(new_password)
    user.save()

    return render(request,'reset_success.html')
def reset_password_form(request, uidb64, token):
    """Show the reset password form"""
    context = {
        "uidb64": uidb64,
        "token": token
    }
    return render(request, "reset_password_form.html", context)

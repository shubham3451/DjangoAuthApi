from rest_framework import serializers
from api.models import MyUser
from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from api.utils import Util


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model  = MyUser
        fields = ['id', 'email', 'name', 'tc', 'password', 'password2']
        extra_kwargs={
        'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('passsword do not match')
        return attrs

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class  Meta:
        model = MyUser
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'name', 'email']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style = {'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style = {'input_type':'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('passsword do not match')
        user.set_password(password)
        user.save()
        return attrs
    
class UserSendpasswordResetMailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['email',]

    def validate(self, attrs):
        email = attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user =MyUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
          ' subject':'Reset Your Password',
          ' body':body,
          ' to_email':user.email
               }
            #Util.send_email(data)
            return attrs   
        else:
           raise serializers.ValidationError("you are not a registered user")


class UserPasswordResetSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    model = MyUser
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = MyUser.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')

    

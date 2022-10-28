from unittest.util import _MAX_LENGTH
from rest_framework import serializers

###############################################################################

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

###############################################################################

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    user_name = serializers.CharField(max_length = 100)
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length=100)

###############################################################################

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length=100)
    
###############################################################################

class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length=100)

###############################################################################

class AuthenticateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100, allow_blank=True)
    college = serializers.CharField(max_length=100)
    year = serializers.CharField(max_length=100)
    branch = serializers.CharField(max_length=100)
    profile_url = serializers.URLField(max_length=100)
    skills = serializers.CharField(max_length=5000)

###############################################################################

class UserSerializer(serializers.Serializer):
	name = serializers.CharField(max_length = 100)
	email = serializers.EmailField()
	college = serializers.CharField(max_length = 100)
	key = serializers.CharField(max_length=100)
	mobile = serializers.IntegerField()

###############################################################################

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	college = serializers.CharField(max_length = 100)
	key = serializers.CharField(max_length=100)

###############################################################################

class AddQuestionSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password= serializers.CharField(max_length=1000)
    anonymous= serializers.BooleanField()
    question= serializers.CharField(max_length=1000)
    tags= serializers.CharField(max_length=1000)
    
###############################################################################

class AddAnswerSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password= serializers.CharField(max_length=100)
    question= serializers.CharField(max_length=100000000)
    answer= serializers.CharField(max_length=10000000000)

###############################################################################

class ViewSpecificQuestionSerializer(serializers.Serializer):
    question= serializers.CharField(max_length=100000000)
    
###############################################################################

class UpvoteQuestionSerializer(serializers.Serializer):
    question= serializers.CharField(max_length=100000000)

###############################################################################

class UpvoteAnswerSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=100000000)
    answer = serializers.CharField(max_length=10000000000)

###############################################################################

class SpecificTagSerializer(serializers.Serializer):
    tag = serializers.CharField(max_length=10000)

###############################################################################



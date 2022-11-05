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

class ContributorSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    gender = serializers.CharField(max_length=10)
    college = serializers.CharField(max_length=100)
    semester = serializers.CharField(max_length=100)
    branch = serializers.CharField(max_length=100)
    linkedin_url = serializers.URLField(max_length=1000)
    github_url = serializers.URLField(max_length=1000)
    codechef_url = serializers.URLField(max_length=1000,allow_blank=True)
    codeforces_url = serializers.URLField(max_length=1000,allow_blank=True)
    leetcode_url = serializers.URLField(max_length=1000,allow_blank=True)
    other_url = serializers.URLField(max_length=1000,allow_blank=True)
    skills = serializers.CharField(max_length=5000)
    company = serializers.CharField(max_length=5000,allow_blank=True)
    position = serializers.CharField(max_length=5000,allow_blank=True)

###############################################################################

class EditProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    name = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length=100)
    gender = serializers.CharField(max_length=10)
    college = serializers.CharField(max_length=100)
    semester = serializers.CharField(max_length=100)
    branch = serializers.CharField(max_length=100)
    linkedin_url = serializers.URLField(max_length=1000)
    github_url = serializers.URLField(max_length=1000)
    codechef_url = serializers.URLField(max_length=1000,allow_blank=True)
    codeforces_url = serializers.URLField(max_length=1000,allow_blank=True)
    leetcode_url = serializers.URLField(max_length=1000,allow_blank=True)
    other_url = serializers.URLField(max_length=1000,allow_blank=True)
    skills = serializers.CharField(max_length=5000)
    company = serializers.CharField(max_length=5000,allow_blank=True)
    position = serializers.CharField(max_length=5000,allow_blank=True)
    projectName1 = serializers.CharField(max_length=5000,allow_blank=True)
    projectDesc1 = serializers.CharField(max_length=5000,allow_blank=True)
    projectLink1 = serializers.CharField(max_length=5000,allow_blank=True)
    projectName2 = serializers.CharField(max_length=5000,allow_blank=True)
    projectDesc2 = serializers.CharField(max_length=5000,allow_blank=True)
    projectLink2 = serializers.CharField(max_length=5000,allow_blank=True)

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
    tags= serializers.CharField(max_length=1000,allow_blank=True)
    
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

class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10000)

###############################################################################



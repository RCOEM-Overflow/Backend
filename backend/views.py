from os import stat
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import *
from .serializers import *

###############################################################################


@api_view(['POST'])
def register(request):
    """
    {
        "name": "Demo User 1",
        "user_name": "noob1",
        "email": "demouser1@gmail.com",
        "password": "pass"
    }
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        data = serializer.data

        user_data = {
            'name': data['name'],
            'user_name': data['user_name'],
            'email': data['email'],
            'password': data['password'],
            'contributor': False,
            'college': "",
            'semester': "",
            'branch': "",
            'skills': "",
            'points': 0,
            'linkedin_url': "",
            'github_url': "",
            'codechef_url': "",
            'codeforces_url': "",
            'leetcode_url': "",
            'other_url': "",
            'company': "",
            'position': "",
            "projectName1" : "",
            "projectDesc1" : "",
            "projectLink1" : "",
            "projectName2" : "",
            "projectDesc2" : "",
            "projectLink2" : ""
        }

        email = data['email']
        user_name = data['user_name']


        if (check_email_exist(email) != 0):
            print("EMAIL ALREADY EXIST")
            return Response("EMAIL ALREADY EXIST", status=status.HTTP_406_NOT_ACCEPTABLE)

        elif(check_username_exist(user_name) != 0):
            print("EMAIL USER NAME EXIST")
            return Response("USER NAME ALREADY EXIST", status=status.HTTP_406_NOT_ACCEPTABLE)

        elif((check_email_exist(email) == 0) and (check_username_exist(user_name) == 0)):
            print("NEW USER FOUND")
            if(create_user(email, user_data)==1):
                return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)
            else:
                print("ERROR IN CREATING USER, TRY AGAIN")
                return Response("ERROR IN CREATING USER, TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        else:
            print("ERROR IN REGISTERING, TRY AGAIN")
            return Response("ERROR IN REGISTERING, TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

    else:
        return Response("Invalid Email", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def login(request):
    
    """
    {
        "email": "demouser1@gmail.com",
        "password": "pass"
    }
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        
        email = data['email']
        password = data['password']

        # print(email)
        # print(password)
        
        doexist = check_email_exist(email)

        if(doexist == 1):

            if(verify_login_by_email(email, password) == 1):
                print("LOGGED IN SUCCESFULLY")
                isContributor = is_contributor(email)
                username =  get_username(email)
                data = {
                    'contributor':isContributor,
                    'username':username
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                print("INVALID PASSWORD")
                return Response("Invalid Password !! Please Try Again", status=status.HTTP_401_UNAUTHORIZED)

        elif(doexist == -1):
            print("Cant verify email (-1)")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        else:
            print("EMAIL DOES NOT EXIST")
            return Response("PLEASE REGISTER", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("Invalid Email", status=status.HTTP_400_BAD_REQUEST)


###############################################################################


@api_view(['POST'])
def register_contributor(request):
    """
    {
        "email": "demouser1@gmail.com",
        "gender": "male",
        "college": "RCOEM",
        "semester": "2nd",
        "branch" : "CSE A",
        "skills": "C++,C,Java,Python",
        "linkedin_url" : "https://www.demouser1.com",
        "github_url" : "https://www.github.demouser1.com",
        "codechef_url" : "https://www.codechef.demouser1.com",
        "codeforces_url" : "https://www.codeforces.demouser1.com",
        "leetcode_url" : "https://www.leetcode.demouser1.com",
        "other_url" : "https://www.demouser1.com",
        "company" : "",
        "position" : ""
    }
    """
    serializer = ContributorSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data

        email = data['email']
        gender = data['gender']
        college = data['college']
        semester = data['semester']
        branch = data['branch']
        skills_str = data['skills']
        linkedin_url = data['linkedin_url']
        github_url = data['github_url']
        codechef_url = data['codechef_url']
        codeforces_url = data['codeforces_url']
        leetcode_url = data['leetcode_url']
        other_url = data['other_url']
        company = data['company']
        position = data['position']

        skills = covert_string_to_skills_list(skills_str)
        
        gender = gender.upper()

        user_data = {
            'contributor': True,
            'gender': gender,
            'college': college,
            'semester': semester,
            'branch': branch,
            'skills': skills,
            'points': 0,
            'linkedin_url': linkedin_url,
            'github_url': github_url,
            'codechef_url': codechef_url,
            'codeforces_url': codeforces_url,
            'leetcode_url': leetcode_url,
            'other_url': other_url,
            'company': company,
            'position': position
        }
        
        doexist = check_email_exist(email)

        if (doexist == 0):
            print("NO USER FOUND")
            return Response("NO USER FOUND", status=status.HTTP_404_NOT_FOUND)

        elif (doexist == -1):
            print("ERROR")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        elif (doexist == 1):
            print("USER FOUND")

            if(add_authentication_user_data(email, user_data) == 1):
                return Response("PROFILE UPDATED", status=status.HTTP_200_OK)
            else:
                print("ERROR IN UPDATING DATA")
                return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

    return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################
    
@api_view(['POST'])
def update_password(request):
    """
    {
        "email": "demouser2@gmail.com",
        "password": "updated_password"
    }
    """
    serializer = UpdatePasswordSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        
        email = data['email']
        password = data['password']

        # print(email)
        # print(password)
        
        doexist = check_email_exist(email)

        if(doexist == 1):

            if(updatePassword(email, password) == 1):
                print("Password Updated Successfully")
                return Response("Password Updated Successfully", status=status.HTTP_200_OK)
            else:
                print("Cant update Password")
                return Response("FAILED TO UPDATE PASSWORD, PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        elif(doexist == -1):
            print("Cant verify email (-1)")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        else:
            print("EMAIL DOES NOT EXIST")
            return Response("EMAIL DOES NOT EXIST", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)


###############################################################################

@api_view(['POST'])
def edit_profile(request):
    """
    {
        "email": "rajbhojpr@rknec.edu",
        "name": "Prathamesh Rajbhoj",
        "password": "1234",
        "gender": "male",
        "college": "RCOEM",
        "semester": "5th",
        "branch" : "CSE A",
        "skills": "C++, C, Java, Python, CP, Django",
        "linkedin_url": "https://www.linkedin.com/in/prathamesh-rajbhoj-2bb157200/",
        "github_url" : "https://github.com/Pratham2301",
        "codechef_url" : "https://www.codechef.com/users/noob_pratham",
        "codeforces_url": "https://codeforces.com/profile/noob_pratham23",
        "leetcode_url": "https://leetcode.com/noob_pratham23/",
        "other_url" : "",
        "company" : "",
        "position" : "",
        "projectName1" : "",
        "projectDesc1" : "",
        "projectLink1" : "",
        "projectName2" : "",
        "projectDesc2" : "",
        "projectLink2" : ""
    }
    """

    serializer = EditProfileSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data

        email = data['email']
        name = data['name']
        password = data['password']
        gender = data['gender']
        college = data['college']
        semester = data['semester']
        branch = data['branch']
        skills_str = data['skills']
        linkedin_url = data['linkedin_url']
        github_url = data['github_url']
        codechef_url = data['codechef_url']
        codeforces_url = data['codeforces_url']
        leetcode_url = data['leetcode_url']
        other_url = data['other_url']
        company = data['company']
        position = data['position']
        projectName1 = data['projectName1']
        projectDesc1 = data['projectDesc1']
        projectLink1 = data['projectLink1']
        projectName2 = data['projectName2']
        projectDesc2 = data['projectDesc2']
        projectLink2 = data['projectLink2']

        skills = covert_string_to_skills_list(skills_str)
        
        gender = gender.upper()

        user_data = {
            'name': name,
            'password': password,
            'contributor': True,
            'gender': gender,
            'college': college,
            'semester': semester,
            'branch': branch,
            'skills': skills,
            'linkedin_url': linkedin_url,
            'github_url': github_url,
            'codechef_url': codechef_url,
            'codeforces_url': codeforces_url,
            'leetcode_url': leetcode_url,
            'other_url': other_url,
            'company': company,
            'position': position,
            'projectName1' : projectName1,
            'projectDesc1' : projectDesc1,
            'projectLink1' : projectLink1,
            'projectName2' : projectName2,
            'projectDesc2' : projectDesc2,
            'projectLink2' : projectLink2
        }

        doexist = check_email_exist(email)

        if (doexist == 0):
            print("NO USER FOUND")
            return Response("NO USER FOUND", status=status.HTTP_404_NOT_FOUND)

        elif (doexist == -1):
            print("ERROR")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        elif (doexist == 1):
            print("USER FOUND")

            if(edit_user_data(email, user_data) == 1):
                return Response("PROFILE UPDATED", status=status.HTTP_200_OK)
            else:
                print("ERROR IN UPDATING DATA")
                return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

    return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['GET'])
def view_all_questions(request):
    try:
        data = get_all_questions()
        return Response(data, status=status.HTTP_200_OK)
    except:
        return Response("PLEASE TRY AGAIN", status=status.HTTP_400_BAD_REQUEST)

###############################################################################

@api_view(['GET'])
def view_search_questions(request):
    try:
        data = get_search_questions()
        return Response(data, status=status.HTTP_200_OK)
    except:
        return Response("PLEASE TRY AGAIN", status=status.HTTP_400_BAD_REQUEST)
    

###############################################################################


@api_view(['GET'])
def view_trending_questions(request):
    try:
        data = get_trending_questions()
        return Response(data, status=status.HTTP_200_OK)
    except:
        return Response("PLEASE TRY AGAIN", status=status.HTTP_400_BAD_REQUEST)


###############################################################################


@api_view(['GET'])
def view_unanswered_questions(request):
    try:
        data = get_unanswered_questions()
        return Response(data, status=status.HTTP_200_OK)
    except:
        return Response("PLEASE TRY AGAIN", status=status.HTTP_400_BAD_REQUEST)


###############################################################################


@api_view(['POST'])
def add_question(request):
    """
    {
            "email": "demouser1@gmail.com",
            "password":"pass",
            "anonymous": "False",
            "question":"How to become 7 star on codechef",
            "tags":"competitive-programming,cp,dsa"
    }
    """
    
    try:
        serializer = AddQuestionSerializer(data=request.data)

        if serializer.is_valid():
            
            data = serializer.data
            
            email = data['email']
            password = data['password']
            question = data['question']
            tags = data['tags']
            anonymous = data['anonymous']
            
            if(len(tags)==0):
                return Response("No Tags Found", status=status.HTTP_400_BAD_REQUEST)
            
            check = checkUserForAddQuestion(email, password,question,tags,anonymous)
            
            updated = updatePoints(email,2)
            
            if(updated==False):
                return Response("Failed to Update Points", status=status.HTTP_403_FORBIDDEN)
            
            if(check == True):
                return Response("Question added successfully", status=status.HTTP_200_OK)
            else:
                return Response("INVALID USER DATA", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("PLEASE TRY AGAIN", status=status.HTTP_400_BAD_REQUEST)
    
###############################################################################


@api_view(['POST'])
def add_answer(request):
    """
    {
            "email": "demouser1@gmail.com",
            "password":"pass",
            "question":"How to become 6 star on codechef?",
            "answer":"Youtube"
    }
    """
    serializer = AddAnswerSerializer(data=request.data)

    if serializer.is_valid():
        
        data = serializer.data
        
        email = data['email']
        password = data['password']
        question = data['question']
        answer = data['answer']
        
        check = checkUser2(email, password, question, answer)
        
        updated = updatePoints(email,5)
            
        if(updated==False):
            return Response("Failed to Update Points", status=status.HTTP_403_FORBIDDEN)
        
        if(check == True):
            return Response("Answer added successfully")
        else:
            return Response("INVALID USER DATA")
    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def view_specific_question(request):
    """
        {
            "question":"How to become 6 star on codechef?"
        }
    """
    serializer = ViewSpecificQuestionSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.data
        
        question = data['question']
        data = get_specific_question(question)
        
        return Response(data, status=status.HTTP_200_OK) 
    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


###############################################################################

@api_view(['POST'])
def user_info(request):
    """
    {
        "username":"noob_pratham23"
    }
    """
    try:
        serializer = UserInfoSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.data
            
            username = data['username']
            data = get_user_info(username)
            
            return Response(data, status=status.HTTP_200_OK) 
        else:
            return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("PLEASE TRY AGAIN", status=status.HTTP_400_BAD_REQUEST)


###############################################################################

@api_view(['GET'])
def all_contributors(request):
    try:
        data=get_all_contributors()
        return Response(data, status=status.HTTP_200_OK)   
    except:
        return Response("Failed to Fetch Contributors", status=status.HTTP_400_BAD_REQUEST)

###############################################################################

@api_view(['GET'])
def all_users(request):
    try:
        data=get_all_users()
        return Response(data, status=status.HTTP_200_OK)      
    except:
        return Response("Failed to Users", status=status.HTTP_400_BAD_REQUEST)
    

###############################################################################

@api_view(['GET'])
def top5_contributors(request):
    try:
        data = get_top_5_contributors()
        return Response(data, status=status.HTTP_200_OK)      
    except:
        return Response("Failed to Fetch Contributors", status=status.HTTP_400_BAD_REQUEST)   

###############################################################################

@api_view(['GET'])
def total_users_count(request):
    try:
        count = get_total_users_count()
        return Response(count, status=status.HTTP_200_OK)        
    except:
        return Response(93, status=status.HTTP_400_BAD_REQUEST) 
    
###############################################################################

@api_view(['GET'])
def total_questions_count(request):
    try:
        count=get_total_questions_count()
        return Response(count, status=status.HTTP_200_OK)       
    except:
        return Response(54, status=status.HTTP_400_BAD_REQUEST) 
    

###############################################################################

@api_view(['GET'])
def total_views_count(request):
    try:
        increase_views()
        count=get_total_views_count()
        return Response(count, status=status.HTTP_200_OK)      
    except:
        return Response(322, status=status.HTTP_400_BAD_REQUEST) 
    

###############################################################################

@api_view(['GET'])
def front_page_analytics(request):
    try:
        increase_views()
        qcount=get_total_questions_count()
        vcount=get_total_views_count()
        ucount = get_total_users_count()
        data = {
            'que_count': qcount,
            'views_count': vcount,
            'users_count': ucount
        }
        return Response(data, status=status.HTTP_200_OK)      
    except:
        return Response(322, status=status.HTTP_400_BAD_REQUEST) 
    
###############################################################################

@api_view(['POST'])
def upvote_question(request):
    """
    {
            "question":"How to become 6 star on codechef?"
    }
    """
    try:
        serializer = UpvoteQuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            
            data = serializer.data
            question = data['question']
            
            upvote_que(question)
            
            return Response(status=status.HTTP_200_OK)
        else:   
            return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("Failed to Upvote", status=status.HTTP_400_BAD_REQUEST)

###############################################################################

@api_view(['POST'])
def upvote_answer(request):
    """
    {
        "question":"How to become 6 star on codechef?",
        "answer":"Youtube"
    }
    """
    try:
        serializer = UpvoteAnswerSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.data
            question = data['question']
            answer = data['answer']
            # print(question)
            # print(answer)
            upvote_ans(question, answer)  
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("Failed to Upvote", status=status.HTTP_400_BAD_REQUEST)
        
###############################################################################

@api_view(['GET'])
def all_tags(request):
    try:
        data=get_all_tags()
        return Response(data, status=status.HTTP_200_OK)       
    except:
        return Response({},status=status.HTTP_400_BAD_REQUEST) 


###############################################################################

@api_view(['POST'])
def tagwise_question(request):
    """
    {
        "tag":"html"
    }
    """
    try:
        serializer = SpecificTagSerializer(data=request.data)
        
        if serializer.is_valid():
            
            data = serializer.data
            tag = data['tag']
            
            data = questionsByTag(tag) 

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("FAILED TO FETCH QUESTIONS BY TAG", status=status.HTTP_400_BAD_REQUEST) 

###############################################################################

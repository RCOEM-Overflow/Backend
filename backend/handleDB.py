import json
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
import firebase_admin
from firebase_admin import credentials, firestore
from grpc import Status
cred = credentials.Certificate('credentials.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

###############################################################################

def check():
      print("checking heroku push")
      
###############################################################################

def get_all_questions():
      index = get_total_questions_count()
      index = index + 5
      returndata = []
      # print(index)

      for i in range(index):
            returnmap = {}
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            if(data.exists):
                  data = data.to_dict()
                  answerlen = len(data['answers'])
                  # print(data['answers'])
                  print(i)
                  if(answerlen > 0):
                        returnmap['author'] = data['author']
                        returnmap['no_of_answers'] = answerlen
                        returnmap['views'] = data['views']
                        returnmap['upvotes'] = data['upvotes']
                        returnmap['question'] = data['question']
                        returnmap['tags'] = data['tags']
                        returnmap['anonymous'] = data['anonymous']
                        
                        if(data['anonymous']==True):
                              returnmap['author'] = "Anonymous"
                              
                        returndata.append(returnmap)

      returndata.reverse()
      return returndata

###############################################################################

def get_search_questions():
      index = get_total_questions_count()
      index = index + 5
      returndata = []

      for i in range(index):
            returnmap = {}
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            if(data.exists):
                  data = data.to_dict()
                  answerlen = len(data['answers'])
                  if(answerlen > 0):
                        returnmap['question'] = data['question']
                        question=data['question']
                        # linkstr="http://localhost:3000/answers/"
                        linkstr="https://collegewit.netlify.app/answers/"
                        for element in question:
                              if(element==' '):
                                    linkstr+="%20"
                              else:
                                    linkstr+=element
                        returnmap['link']=linkstr
                        returndata.append(returnmap)

      return returndata

###############################################################################

def get_unanswered_questions():
      index = get_total_questions_count()
      index = index + 5
      returndata = []

      for i in range(index):
            returnmap = {}
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            if(data.exists):
                  data = data.to_dict()
                  answerlen = len(data['answers'])
                  if(answerlen == 0):
                        returnmap['author'] = data['author']
                        returnmap['question'] = data['question']
                        returnmap['tags'] = data['tags']
                        returnmap['anonymous'] = data['anonymous']
                        
                        if(data['anonymous']==True):
                              returnmap['author'] = "Anonymous"
                              
                        returndata.append(returnmap)

      return returndata

###############################################################################

def checkUserForAddQuestion(email, password,question,tags,anonymous):
      try:
            user = db.collection('users').document(email).get()
            user = user.to_dict()
            pas = user['password']
            
            question1 = ""

            for i in question:
                  if i=='?':
                        question1 = question1 + "."
                  else:
                        question1 = question1 + i

            if(pas == password):
                  author = user['user_name']
                  add_question_db(question1,author,tags,anonymous)
                  return True
            else :
                  return False
      except:
            print("Error in checkUser")
            return False

###############################################################################

def checkUser2(email, password, question, answer):
      try:
            user = db.collection('users').document(email).get()
            getuser = user.to_dict()
            
            pas = getuser['password']
            
            if(pas==password):
                  author = getuser['user_name']
                  add_answer_db(question, author, answer)
                  return True
            else :
                  return False
      except:
            print("Error in checkUser2")
            return False
###############################################################################

def add_question_db(question, author, tags, anonymous):
      
      try:
            tags = tags.upper()
            tags = tags.split(",");
            
            if(question.endswith('?')==False):
                  # print("not")
                  question = question + "?"
                  
            data = {
                  'question': question,
                  'answers': [],
                  'upvotes': 0,
                  'views': 0,
                  'author': author,
                  'tags': tags,
                  'anonymous': anonymous
            }
            
            index = get_total_questions_count()
            index = index+1
            question_no = 'question'+str(index)
            db.collection('questions').document(question_no).set(data)
            increase_questions_views()
            
      except:
            print("Error in add_question_db")
            return False

###############################################################################

def add_answer_db(question, author, answer):
      qdata = db.collection('questions').where("question", "==", question).get()
      key = qdata[0].id

      qdata = qdata[0].to_dict()
      
      answer_array = qdata['answers']

      data = {
            'answer': answer,
            'author': author,
            'upvotes': 0,
            'comments': [],
      }
      
      answer_array.append(data)
      db.collection('questions').document(key).update({"answers": answer_array})

###############################################################################

def get_specific_question(question):
      qdata = db.collection('questions').where("question", "==", question).get()
      if(len(qdata) != 0):
            quenum = qdata[0].id
            
            data = db.collection('questions').document(quenum)
            data.update({'views': firestore.Increment(1)})
            
            data = data.get()
            data = data.to_dict()
            
            if(data['anonymous']==True):
                  data['author'] = "Anonymous"
            
            answerlist = data['answers']
            
            answerlist = sorted(answerlist, key=lambda k: k['upvotes'], reverse=True)
            
            data['answers'] =  answerlist
            
            return data
      else:
            return "Question Not Found"

###############################################################################

def get_trending_questions():
      index = get_total_questions_count() + 5
      returndata = []
      dic = {}
      for i in range(index):
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            if(data.exists):
                  data = data.to_dict()
                  answerlen = len(data['answers'])
                  if(answerlen > 0):
                        dic[(i+1)] = data['upvotes']

      sorted_dict = {}
      sorted_keys = sorted(dic, key=dic.get)
      sorted_keys.reverse()

      for w in sorted_keys:
            sorted_dict[w] = dic[w]
            returnmap = {}
            question_no = 'question'+str(w)
            data = db.collection('questions').document(question_no).get()
            data = data.to_dict()
            returnmap['author'] = data['author']
            returnmap['no_of_answers'] = answerlen
            returnmap['views'] = data['views']
            returnmap['upvotes'] = data['upvotes']
            returnmap['question'] = data['question']
            
            if(data['anonymous']==True):
                  returnmap['author'] = "Anonymous"
                  
            returndata.append(returnmap)
      
      returndata = sorted(returndata, key=lambda k: k['upvotes'], reverse=True)

      return returndata

###############################################################################

def check_email_exist(email):
      
      try:
            user = db.collection('users').document(email).get()
            if(user.exists):
                  return 1
            else:
                  return 0
            
      except:
            print("ERROR IN CHECK_EMAIL_EXIST")
            return -1
      
###############################################################################

def check_username_exist(user_name):
	try:
		user = db.collection("users").where('user_name', '==', user_name).get()
		if(len(user)>0):
			return 1
		else:
			return 0
	except:
		print("ERROR IN CHECK_USERNAME_EXIST")
		return -1

###############################################################################

def create_user(email,data):
      
      try:
            db.collection('users').document(email).set(data)
            
            return 1
      except:
            print("ERROR IN CREATE_USER")
            return -1

###############################################################################

def get_user_data(email):
      try:
            users = db.collection('users').document(email).get()

            if len(users) > 0:
                  userdata = users[0].to_dict()
                  return userdata
            else:
                  userdata = {}
                  return userdata
      except:
            print("ERROR IN GET_USER_DATA")
            return -1

###############################################################################

def verify_login_by_username(user_name,password):
      try:
            user = db.collection("users").where('user_name', u'==', user_name).get()
            userdata=user[0].to_dict()
            
            if(password==userdata['password']):
                  return 1
            else:
                  return 0
      except:
            print("ERROR IN VERIFY_LOGIN_BY_USERNAME")
            return -1

###############################################################################

def verify_login_by_email(email,password):
      try:
            user = db.collection('users').document(email).get()
            userdata=user.to_dict()   
            
            if(password == userdata['password']):
                  return 1
            else:
                  return 0
      except:
            print("ERROR IN VERIFY_LOGIN_BY_EMAIL")
            return -1
      

###############################################################################

def is_contributor(email):
      try:
            user = db.collection('users').document(email).get()
            userdata=user.to_dict() 
            
            isContributor = userdata['contributor']       
            return isContributor
      except:
            print("ERROR IN VERIFY_LOGIN_BY_EMAIL")
            return -1
      
###############################################################################

def get_username(email):
      try:
            user = db.collection('users').document(email).get()
            userdata=user.to_dict() 
            
            username = userdata['user_name'];       
            return username
      except:
            print("ERROR IN VERIFY_LOGIN_BY_EMAIL")
            return -1
      
###############################################################################

def add_authentication_user_data(email,user_data):
      try:
            user = db.collection('users').document(email)
            user.update(user_data)
            return 1
      except:
            return 0
###############################################################################

def edit_user_data(email,user_data):
      try:
            user = db.collection('users').document(email)
            user.update(user_data)
            return 1
      except:
            return 0
###############################################################################

def covert_string_to_skills_list(skills_str):
      
      skills=[]
      var=""
      
      for c in skills_str:
            if(c==','):
                  skills.append(var)
                  var=""
            else:
                  var+=c                  
      skills.append(var)
      
      print(skills)
      return skills

###############################################################################

def get_all_tags():
      
      my_list=[]
      tags = db.collection('tags').get()
      tags = tags[0].to_dict()
      
      for tag in tags.keys():
            dict={
                  'tag':tag,
                  'number_of_questions':tags[tag]
            }
            my_list.append(dict)
            
      my_list = sorted(my_list, key=lambda k: k['number_of_questions'], reverse=True)
      return my_list
      
# print(get_all_tags())

###############################################################################

def get_all_users():
      
      my_list=[]
      users = db.collection("users").get()

      for user in users:
            user_data = user.to_dict()
            user_data['password']="*****"
            my_list.append(user_data)     

      my_list = sorted(my_list, key=lambda k: k['points'], reverse=True)
      
      return my_list
###############################################################################

def get_user_info(username):
      
      users = db.collection("users").where('user_name', u'==', username).get()
      
      if(len(users)>0):
      
            userdata = users[0].to_dict()
            
            # changes in skills (array to string)
            skills = userdata['skills']
            cskills = ""
            skill_len = len(skills)
            
            for i in range(skill_len):
                  cskills = cskills + skills[i]
                  if(i!=skill_len-1):
                        cskills = cskills + ", "
                  
            userdata['skills'] = cskills

            
            if(userdata['github_url'] != ""):
                  val = userdata['github_url'].split('/')
                  if(len(val)>=4):
                        val = val[3]
                        userdata['github_username'] = val
                  else:
                        userdata['github_username'] = ""
                        
            
            if(userdata['linkedin_url'] != ""):
                  val = userdata['linkedin_url'].split('/')
                  if(len(val)>=5):
                        val = val[4]
                        userdata['linkedin_username'] = val
                  else:
                        userdata['linkedin_username'] = ""

            if(userdata['codechef_url'] != ""):
                  val = userdata['codechef_url'].split('/')
                  if(len(val)>=5):
                        val = val[4]
                        userdata['codechef_username'] = val
                  else:
                        userdata['codechef_username'] = ""

            if(userdata['codeforces_url'] != ""):
                  val = userdata['codeforces_url'].split('/')
                  if(len(val)>=5):
                        val = val[4]
                        userdata['codeforces_username'] = val
                  else:
                        userdata['codeforces_username'] = ""

            if(userdata['leetcode_url'] != ""):
                  val = userdata['leetcode_url'].split('/')
                  if(len(val)>=4):
                        val = val[3]
                        userdata['leetcode_username'] = val
                  else:
                        userdata['leetcode_username'] = ""

            userdata['password']="*****"
            
            return userdata
      
      return {}

###############################################################################

def get_all_contributors():
      
      my_list=[]
      users = db.collection('users').where('contributor', u'==', True).get()

      for user in users:
            user_data = user.to_dict()
            
            l_username = ""
            g_username = ""
            
            if(user_data['github_url'] != ""):
                  val = user_data['github_url']
                  val = val.split('/')
                  if(len(val)>=4):
                        val = val[3]
                        g_username = val

            if(user_data['linkedin_url'] != ""):
                  val = user_data['linkedin_url']
                  val = val.split('/')
                  if(len(val)>=5):
                        val = val[4]
                        l_username = val
                        
            
            dict={
                  'name': user_data['name'],
                  'rank': 0,
                  'user_name': user_data['user_name'],
                  'points': user_data['points'],
                  'linkedin_url': user_data['linkedin_url'],
                  'github_url': user_data['github_url'],
                  'linkedin_username': l_username,
                  'github_username': g_username
            }
            
            
            my_list.append(dict)    
            
            # name username score github linkedin 
      
      my_list = sorted(my_list, key=lambda k: k['points'], reverse=True)
      
      for i in range(len(my_list)):
            my_list[i]['rank']=i+1

      
      arr1i = slice(0,3)
      arr2i = slice(3,len(my_list))
      
      arr1 = my_list[arr1i]
      arr2 = my_list[arr2i]

      
      data = {
            'top3': arr1,
            'next':arr2
      }

      return data

###############################################################################

def get_top_5_contributors():
      my_list=[]
      
      users = db.collection("users").where('contributor', u'==', True).get()

      for user in users:
            user_data=user.to_dict()

            dict={
                  'name':user_data['name'],
                  'user_name':user_data['user_name'],
                  'college':user_data['college'],
                  'points':user_data['points']
            }
            my_list.append(dict)   
      
      my_list = sorted(my_list, key=lambda k: k['points'], reverse=True)
      my_list = my_list[0:5]
      return my_list

###############################################################################

def get_total_users_count():
      data = db.collection('users').get()
      return len(data)
      
###############################################################################

def increase_questions_views():
      index=db.collection('index').document('index')
      index.update({"questions": firestore.Increment(1)})
      
###############################################################################

def increase_views():
      index=db.collection('index').document('index')
      index.update({"views": firestore.Increment(1)})
      
###############################################################################

def get_total_views_count():
      data = db.collection("index").document('index').get()
      data=data.to_dict()
      count=data['views']
      return count

###############################################################################

def check_valid_email(email):
      if(re.fullmatch(regex, email)):
            print("Valid Email")
            return 1
      else:
            print("Invalid Email")
            return 0
      
###############################################################################

def upvote_que(question):
      # print(question)
      qdata = db.collection('questions').where("question", "==", question).get()
      quenum = qdata[0].id
      data = db.collection("questions").document(quenum)
      data.update({"upvotes": firestore.Increment(1)})
      
      data = db.collection('questions').document(quenum)
      data.update({'views': firestore.Increment(1)})
            

###############################################################################

def upvote_ans(question, answer):
      qdata = db.collection('questions').where("question", "==", question).get()
      quenum = qdata[0].id
      data = qdata[0].to_dict()

      dict={
            "answers": data['answers'],
            "author": data['author'],
            "question": data['question'],
            "upvotes": data['upvotes'],
            "views": data['views'],
            "tags": data['tags'],
            "anonymous": data['anonymous']
      }

      index=0

      for ans in dict["answers"]:
            if(ans["answer"]==answer):
                  # print("found")
                  # print(ans)
                  dict["answers"][index]["upvotes"] = dict["answers"][index]["upvotes"] + 1
                  # print(ans)
                  break
            index=index+1     

      # print(quenum)
      # print(dict)
      db.collection("questions").document(quenum).set(dict)
      
###############################################################################

def get_total_questions_count():
      data = db.collection('index').document('index').get()
      data = data.to_dict()
      count = data['questions']
      return count

###############################################################################

def updatePassword(email,newpassword):
      try:
            user = db.collection('users').document(email)
            user.update({
                  'password': newpassword
            })
            return 1
      except:
            return -1
      
###############################################################################

# def update_questions_data_manually():
#       index = get_total_questions_count()
#       index = 10
      
#       for i in range(index):
#             question_no = 'question'+str(i+1)
#             data = db.collection('questions').document(question_no)
#             data.update({
#                   'anonymous': False,
#                   'views':100,
#                   'upvotes':20,
#                   'tags':['HTML','CSS','JAVASCRIPT']
#             })
            
#       return "Questions data updated manually"

# ###############################################################################

# def update_users_data_manually():
#       datas = db.collection('users').get()
#       for data in datas:
#             userid = data.id
#             userdata = datas = db.collection('users').document(userid)
#             userdata.update({
#                   "projectName1" : "",
#                   "projectDesc1" : "",
#                   "projectLink1" : "",
#                   "projectName2" : "",
#                   "projectDesc2" : "",
#                   "projectLink2" : ""
#             })
            
#       return "Questions data updated manually"

# update_users_data_manually()

# ###############################################################################

# def questionsByTag(tag):
#       tag = tag.upper()
#       data=[]
#       index = get_total_questions_count()
      
#       for i in range(index):
#             question_no = 'question'+str(i+1)
#             qdata = db.collection('questions').document(question_no).get()
#             qdata = qdata.to_dict()
#             qtags = qdata['tags']
#             # print(qtags)
#             count = qtags.count(tag)
#             if(count>0):
#                   data.append(qdata)      
      
#       return data
###############################################################################

def questionsByTag(tag):
      tag = tag.upper()
      que_list=[]
      
      data = db.collection('questions').get()
      for que in data:
            qdata = que.to_dict()
            qtags = qdata['tags']
            # print(qtags)
            count = qtags.count(tag)
            if(count>0):
                  returnmap = {}
                  returnmap['author'] = qdata['author']
                  returnmap['views'] = qdata['views']
                  returnmap['upvotes'] = qdata['upvotes']
                  returnmap['question'] = qdata['question']
                  
                  if(qdata['anonymous']==True):
                        returnmap['author'] = "Anonymous"
                        
                  que_list.append(returnmap)
            
      que_list = sorted(que_list, key=lambda k: k['views'], reverse=True)
      return que_list

###############################################################################

def updatePoints(email,increase):
      try:
            user = db.collection('users').document(email)
            userdata = user.get()
            userdata = userdata.to_dict()
            points = userdata['points']
            points = points + increase
            
            user.update({
                  'points':points
            })
            return True
      except:
            return False

###############################################################################
###############################################################################

            
      















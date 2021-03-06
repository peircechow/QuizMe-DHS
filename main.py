
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
import cgi
import random
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Question(ndb.Model):
	questiontext = ndb.StringProperty(indexed = False)
	answer = ndb.StringProperty(indexed = False)
	option_1=ndb.StringProperty(indexed = False)
	option_2=ndb.StringProperty(indexed = False)
	option_3=ndb.StringProperty(indexed = False)
	option_4=ndb.StringProperty(indexed = False)
	user_name=ndb.StringProperty(indexed = False)


def get_key():
	return ndb.Key("Question", 1)

class Dunmanian(ndb.Model):
	name= ndb.StringProperty(indexed=True)
	score=ndb.IntegerProperty()
	
class TempAns(ndb.Model):
	tempans= ndb.StringProperty(indexed= False)
	datetime = ndb.DateTimeProperty(auto_now_add=True) #gets the current date and time
	
def TempAns_key():
	return ndb.Key("TempAns", 3)
	
def Dunmanian_key():
	return ndb.Key("Dunmanian", 2)
	
class UserAns(ndb.Model):
	userans= ndb.StringProperty(indexed= False)
	datetime = ndb.DateTimeProperty(auto_now_add=True) #gets the current date and time
	
def UserAns_key():
	return ndb.Key("UserAns", 4)

class QuestionStore(webapp2.RequestHandler):
	def post(self):
		user=users.get_current_user()
		if user:
			user_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
			user_data=user_query.fetch(1)
			user_list=user_data[0]
			#obtain user_key IMPORTANT
			user_key=user_list.key
			score=int(user_data[0].score) 
			#+7
			q = Question(parent=get_key())
			q.answer=self.request.get("option")
			q.option_1=self.request.get("optA")
			q.option_2=self.request.get("optB")
			q.option_3=self.request.get("optC")
			q.option_4=self.request.get("optD")
			q.questiontext=self.request.get("qntext")
			q.blank=self.request.get("optE")
			q.user_name=user.nickname()
			if q.answer==q.blank or q.option_1==q.blank or q.option_2==q.blank or q.option_3==q.blank or q.option_4==q.blank or q.questiontext==q.blank: #checking for empty responses
				new_score=score-5
				user_entity=user_key.get()
				#store user score(need to get key of user's nickname first, find out in GAE book.)
				user_entity.score=new_score
				#update user entity
				user_entity.put()
				self.redirect('/')
			else:
				q.put()
			
			
			#get user score from database

				new_score=score+25
				user_entity=user_key.get()
				#store user score(need to get key of user's nickname first, find out in GAE book.)
				user_entity.score=new_score
				#update user entity
				user_entity.put()
				self.redirect('/question')
		else:
			self.redirect(users.create_login_url(self.request.uri))
			if user:
				self.redirect('/question')
				
	def get(self):
		if users.get_current_user():
			self.redirect('/')
class CheckStore(webapp2.RequestHandler):
	def post(self):
		if users.get_current_user():
			user=users.get_current_user()
			resp=self.request.get("choice")
			blank=self.request.get("no_option_selected")
			# u=UserAns(parent=UserAns_key())
			# u.userans=resp
			# u.put()
			# userans_query=UserAns.query().order(UserAns.datetime)
			# userans_list=userans_query.fetch(1)
			# choice=userans_list[0].userans
			tempans_query=TempAns.query().order(-TempAns.datetime)
			answer_list=tempans_query.fetch(1)
			answer=answer_list[0].tempans
			user_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
			user_data=user_query.fetch(1)
			user_list=user_data[0]
			#obtain user_key IMPORTANT
			user_key=user_list.key
			
			if resp==answer:
				
				score=int(user_data[0].score) 
				#+7
				new_score=score+4
				user_entity=user_key.get()
				#store user score(need to get key of user's nickname first, find out in GAE book.)
				user_entity.score=new_score
				#update user entity
				user_entity.put()

			elif resp==blank:
				score=int(user_data[0].score) 
				#+7
				new_score=score-5
				user_entity=user_key.get()
				#store user score(need to get key of user's nickname first, find out in GAE book.)
				user_entity.score=new_score
				#update user entity
				user_entity.put()
			else:
				score=int(user_data[0].score) 
				#+7
				new_score=score+1
				user_entity=user_key.get()
				#store user score(need to get key of user's nickname first, find out in GAE book.)
				user_entity.score=new_score
				#update user entity
				user_entity.put()
			self.redirect('/')
		else:
			self.redirect(users.create_login_url(self.request.uri))
			if users.get_current_user():
				self.redirect('/')
	def get(self):
		if users.get_current_user():
			self.redirect('/')
class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
			
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
			#useremail = user.email()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'	
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
			#'useremail': useremail
		}
	user = users.get_current_user()
	dunmanian=Dunmanian(parent=Dunmanian_key())
	if users.get_current_user():#checking if Dunmanian exists, if not redirect them to about page
		d_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
		result=d_query.fetch(1)
		d_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
		result=d_query.fetch(1)
		if result:
			user_score=result[0].score #gets score of current user
			user_text="Your Current Score:"

		
		if not result:
			dunmanian.name=user.nickname()
			dunmanian.score=0
			dunman_key=dunmanian.put()
			self.redirect("/about")
			
			user_text="Welcome to QuizMe@DHS!"
			user_score=''
	else:
		user_score=''
		user_text="Please login to view your score"
	
	question_query = Question.query(ancestor=get_key())
	n=random.randint(1,10)
	questions=question_query.fetch()
	u=len(questions)
	q_index=random.randint(0,len(questions)-1)
	i=questions[q_index]
	qntext=i.questiontext
	option_a=i.option_1
	option_b=i.option_2
	option_c=i.option_3
	option_d=i.option_4
	answer=i.answer
	a=TempAns(parent=TempAns_key())
	a.tempans=answer
	a.put()	
	template_values={
	'user': user,
	'url': url,
	'url_linktext': url_linktext,
	"qntext":qntext,
	"user_text":user_text,
	"user_score":user_score,
	"option_a":option_a,
	"option_b":option_b,
	"option_c":option_c,
	"option_d":option_d,}
	template = JINJA_ENVIRONMENT.get_template('home.html')
	self.response.write(template.render(template_values))

class Leaderboard(webapp2.RequestHandler):
	
		def get(self):
			user = users.get_current_user()
			if user:
				url = users.create_logout_url(self.request.uri)
				url_linktext = 'Logout'
				#useremail = user.email()
			else:
				url = users.create_login_url(self.request.uri)
				url_linktext = 'Login'
			user = users.get_current_user()
			dunmanian=Dunmanian(parent=Dunmanian_key())
			users.get_current_user()
			if users.get_current_user():
				d_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
				result=d_query.fetch(1)
				
				if not result:
					dunmanian.name=user.nickname()
					dunmanian.score=0
					dunman_key=dunmanian.put()
					self.response.write(dunman_key)
					self.redirect("/about")
				
			
			a=[] #put all the scores here 
			score_query=Dunmanian.query().order(-Dunmanian.score)
			scores=score_query.fetch()
			for i in scores:
				a.append(i.score)
			b=sorted(a)
			b.reverse()#now the scores are in accending order in array of b
			try:
				score_1=scores[0].score
				name_1=scores[0].name
			except:
				score_1="-"
				name_1="-"
			
			try:
				score_2=scores[1].score
				name_2=scores[1].name
			except:
				score_2="-"
				name_2="-"
			
			try:
				score_3=scores[2].score
				name_3=scores[2].name
			except:
				score_3="-"
				name_3="-"
			try:
				score_4=scores[3].score
				name_4=scores[3].name
			except:
				score_4="-"
				name_4="-"
				
			try:
				score_5=scores[4].score
				name_5=scores[4].name
			except:
				score_5="-"
				name_5="-"
				
			try:
				score_6=scores[5].score
				name_6=scores[5].name
			except:
				score_6="-"
				name_6="-"
				
			try:
				score_7=scores[6].score
				name_7=scores[6].name
			except:
				score_7="-"
				name_7="-"
				
			try:
				score_8=scores[7].score
				name_8=scores[7].name
			except:
				score_8="-"
				name_8="-"
			
			try:
				score_9=scores[8].score
				name_9=scores[8].name
			except:
				score_9="-"
				name_9="-"
				
			try:
				score_10=scores[9].score
				name_10=scores[9].name
			except:
				score_10="-"
				name_10="-"
			#score_2=b[1]
			#score_3=b[2]
			# score_4=b[3]
			# score_5=b[4]
			# score_6=b[5]
			# score_7=b[6]
			# score_8=b[7]
			# score_9=b[8]
			# score_10=b[9]
			user = users.get_current_user()
			if user:
				try:
					user_nick=user.nickname()+"(You)"
					d_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
					result=d_query.fetch(1)
					user_score=result[0].score #gets score of current user
					user_position=(b.index(user_score))+1
				except:
					self.redirect('/leaderboard')
			else:
				user_nick="-"
				user_score="-"
				user_position="-"
			
			template_values = {
				'score_1':score_1,
				'score_2':score_2,
				'score_3':score_3,
				'score_4':score_4,
				'score_5':score_5,
				'score_6':score_6,
				'score_7':score_7,
				'score_8':score_8,
				'score_9':score_9,
				'score_10':score_10,
				'name_1':name_1,
				'name_2':name_2,
				'name_3':name_3,
				'name_4':name_4,
				'name_5':name_5,
				'name_6':name_6,
				'name_7':name_7,
				'name_8':name_8,
				'name_9':name_9,
				'name_10':name_10,
				'user': user,
				'user_nick':user_nick,
				'user_score':user_score,
				'user_position':user_position,
				'url': url,
				'url_linktext': url_linktext,
				#'useremail': useremail
			}			
			template = JINJA_ENVIRONMENT.get_template('leaderboard.html') #change the file to the relevant html file
			self.response.write(template.render(template_values))
				
class About(webapp2.RequestHandler):
		def get(self):
			user = users.get_current_user()
			if user:
				url = users.create_logout_url(self.request.uri)
				url_linktext = 'Logout'
				#useremail = user.email()
			else:
				url = users.create_login_url(self.request.uri)
				url_linktext = 'Login'	
			template_values = {
				'user': user,
				'url': url,
				'url_linktext': url_linktext,
				#'useremail': useremail
			}
			user = users.get_current_user()
			dunmanian=Dunmanian(parent=Dunmanian_key())
			users.get_current_user()
			if users.get_current_user():
				d_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
				result=d_query.fetch(1)
				
				if not result:
					dunmanian.name=user.nickname()
					dunmanian.score=0
					dunman_key=dunmanian.put()
					self.response.write(dunman_key)
					self.redirect("/about")
		
			template = JINJA_ENVIRONMENT.get_template('about.html') #change the file to the relevant html file
			self.response.write(template.render(template_values))
				
class QuestionPage(webapp2.RequestHandler):
		def get(self):
			user = users.get_current_user()
			if user:
				url = users.create_logout_url(self.request.uri)
				url_linktext = 'Logout'
				#useremail = user.email()
			else:
				url = users.create_login_url(self.request.uri)
				url_linktext = 'Login'	
			template_values = {
				'user': user,
				'url': url,
				'url_linktext': url_linktext,
				#'useremail': useremail
			}
			user = users.get_current_user()
			dunmanian=Dunmanian(parent=Dunmanian_key())
			users.get_current_user()
			if users.get_current_user():
				d_query=Dunmanian.query().filter(Dunmanian.name==user.nickname())
				result=d_query.fetch(1)
				
				if not result:
					dunmanian.name=user.nickname()
					dunmanian.score=0
					dunman_key=dunmanian.put()
					self.redirect("/about")
			
				
			template = JINJA_ENVIRONMENT.get_template('question.html') #change the file to the relevant html file
			self.response.write(template.render(template_values))
			
class TrollPage(webapp2.RequestHandler):
		def get(self):
			user = users.get_current_user()
			if user:
				url = users.create_logout_url(self.request.uri)
				url_linktext = 'Logout'
				#useremail = user.email()
			else:
				url = users.create_login_url(self.request.uri)
				url_linktext = 'Login'	
			template_values = {
				'user': user,
				'url': url,
				'url_linktext': url_linktext,
				#'useremail': useremail
			}
			
			template = JINJA_ENVIRONMENT.get_template('trollpage.html') #change the file to the relevant html file
			self.response.write(template.render(template_values))
# class QuizPage(webapp2.RequestHandler):
    # def get(self):
        # user = users.get_current_user()
        # if user:
            # url = users.create_logout_url(self.request.uri)
            # url_linktext = 'Logout'
			# #useremail = user.email()
        # else:
            # url = users.create_login_url(self.request.uri)
            # url_linktext = 'Login'	
        # template_values = {
            # 'user': user,
            # 'url': url,
            # 'url_linktext': url_linktext,
			# #'useremail': useremail
		# }

	# question_query = Question.query(ancestor=get_key())
	# n=random.randint(1,10)
	# questions=question_query.fetch(n)
	# for a in range(1,16):
		# for i in questions:
			# qntext=i.questiontext
			# option_a=i.option_1
			# option_b=i.option_2
			# option_c=i.option_3
			# option_d=i.option_4
			# answer=i.answer
			# template_values={
			# 'user': user,
			# 'url': url,
			# 'url_linktext': url_linktext,
			# "qntext":qntext,
			# "option_a":option_a,
			# "option_b":option_b,
			# "option_c":option_c,
			# "option_d":option_d,
			# "a":a}
        # template = JINJA_ENVIRONMENT.get_template('quizpage.html')
        # self.response.write(template.render(template_values))

			
#class Guestbook(webapp2.RequestHandler):
#	def post(self):
#		self.response.write('<html><body>You wrote:<pre>')
#		answer = (cgi.escape(self.request.get('content')))
#		self.response.write('</pre></body></html>')
#		q = Question(qntext,answer)
#		q.put()
							
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/leaderboard', Leaderboard),
	('/about', About),			#add the name of the class and the link that you want to assign it
	('/question', QuestionPage),
	('/store', QuestionStore),
	('/checkstore', CheckStore),
	('/trollpage', TrollPage)
	#('/quizpage',QuizPage)
], debug=True)

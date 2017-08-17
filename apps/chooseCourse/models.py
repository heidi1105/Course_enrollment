from __future__ import unicode_literals

from django.db import models
from django.contrib import sessions
import re
import bcrypt

EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9+._-]+@[a-zA-Z0-9+._-]+\.[a-zA-Z]+$')
# Create your models here.


class userManager(models.Manager):
	def reg_validator(self, postData):
		errors={}

		if len(postData['name'])<2:
			errors['name']="First name should be more than 2 characters"
		if len(postData['password'])<8:
			errors['password']="Password should not less than 8 characters"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] ="Invalid email"
		if postData['password'] != postData['cfmpwd']:
			errors['password']="Passwords are not the same"	
		try:
			User.objects.get(email=postData['email'])
			errors['email'] ="You have registered already"
		except:
			pass

		if not len(errors):
		 	hashed=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			user=User.objects.create(name=postData['name'], email=postData['email'], password=hashed)
			return user.id

		return errors

	def login_validator(self, postData):
		errors={}
		if not EMAIL_REGEX.match(postData['email']):
			errors['email']='Invalid email'
		try:
			user=User.objects.get(email=postData['email'])
			hashed= User.objects.get(email=postData['email']).password
			pwcheck= postData['password']
			if not bcrypt.checkpw(pwcheck.encode(), hashed.encode()):
				errors['password'] ='Invalid password'
		except:
			errors['email'] ="You have to register"

		if not len(errors):
			return user.id
		return errors

	def course_validator(self, postData, user_id):
		errors={}
		if len(postData['name'])<2:
			errors['course']='The name should be at least 2 characters'
		try:
			Course.objects.get(name=postData['name'])
			errors['course'] ="The course exists already. Try another course."
		except:
			pass
		if len(errors):
			return errors
		user=User.objects.get(id=user_id)
		course=Course.objects.create(name=postData['name'], instructor=user)
		return course.id		

	def drop_validator(self, cid, user_id):
		errors={}
		try:
			Course.objects.get(id=cid, students__id=user_id)
		except:
			errors['course']="You did not register this course"
		try: 
			Course.objects.get(id=cid, instructor__id=user_id)
			errors['course']="You teach this course, you cannot take it"
		except:
			pass	
		if len(errors):
			return errors
		else:
			Course.objects.get(id=cid).students.remove(User.objects.get(id=user_id))
			print ("Dropped the course")

	def delete_validator(self, cid, user_id):
		errors={}
		try:
			Course.objects.get(id=cid, instructor__id=user_id)
			Course.objects.filter(id=cid).delete()
			print("You deleted the course")
		except:
			errors['course']="You are not the instructor"
			return errors





class User(models.Model):
	name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	user_level=models.IntegerField(default=1)
	objects=userManager()

class Course(models.Model):
	name=models.CharField(max_length=255)
	instructor=models.ForeignKey(User, related_name="teaching_courses")
	students=models.ManyToManyField(User, related_name="enrolled_courses")










from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
	if 'id' in request.session:
		return redirect("/dashboard")
	return render(request, "chooseCourse/index.html")

def dashboard(request):
	if 'id' not in request.session:
		return redirect ("/")

	return render(request, "chooseCourse/dashboard.html", {'user': User.objects.get(id=request.session['id'])})

def createCourse(request):
	if 'id' not in request.session:
		return redirect ("/")


	return render(request, "chooseCourse/create.html")

def enrollCourse(request):
	if 'id' not in request.session:
		return redirect ("/")





	return render(request, "chooseCourse/enrollCourse.html", {'courses':Course.objects.all().exclude(instructor__id=request.session['id']).exclude(students__id=request.session['id'])})

def login(request):
	check=User.objects.login_validator(request.POST)
	if type(check)== dict:  # it is an error
		if len(check):
			for tag, error in check.iteritems():
				messages.error(request, error, extra_tags='login')		
			return redirect("/")
	elif type(check)==int:	
		request.session['id']=check
		return redirect ("/dashboard")


	return redirect("/")

def register(request):
	check=User.objects.reg_validator(request.POST)
	if type(check)== dict:  # it is an error
		if len(check):
			for tag, error in check.iteritems():
				messages.error(request, error, extra_tags='register')		
			return redirect("/")
	elif type(check)==int:
		request.session['id']=check
		return redirect ("/dashboard")


def creating(request):
	check=User.objects.course_validator(request.POST, request.session['id'])
	if type(check)== dict:  # it is an error
		if len(check):
			for tag, error in check.iteritems():
				messages.error(request, error, extra_tags='createCourse')		
			return redirect("/createCourse")
	elif type(check)==int:
		return redirect ("/dashboard")

	return redirect("/")

def enrolling(request, id=id):
	Course.objects.get(id=id).students.add(User.objects.get(id=request.session['id']))
	print("enrolled")
	return redirect("/")

def logout(request):
	if 'id' in request.session:
		del request.session['id']
	return redirect("/")

def deleteCourse(request, id=id):
	check=User.objects.delete_validator(id, request.session['id'])
	if type(check)== dict:  # it is an error
		if len(check):
			for tag, error in check.iteritems():
				messages.error(request, error, extra_tags='deleteCourse')		

	return redirect("/")

def drop(request, id=id):
	check=User.objects.drop_validator(id, request.session['id'])
	if type(check)== dict:  # it is an error
		if len(check):
			for tag, error in check.iteritems():
				messages.error(request, error, extra_tags='dropCourse')		
	return redirect("/")














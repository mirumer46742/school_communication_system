# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import csv
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, render_to_response, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from models import Student, ContactFile, Message, MessageStatus
from django.core.urlresolvers import reverse

# Create your views here.

class SendView(generic.TemplateView):
    template_name="smsapp/index.html"
    saved_students={}

    def get(self, request, *args, **kwargs):
        context={}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        global saved_students 
        student_list=Student.objects.all()
        message_list = Message.objects.all()
        context = {"student_list":student_list, "message_list":message_list}
        context["send_click"]=True

        data = request.POST
        student_class = data.get('class', None)
        student_section = data.get('section', None)
        student_roll_no = data.get('roll_no', None)
        message_text = data.get('message_text', None)

        if 'get_student_list' in data:
            print "Clicked GET LIST Button"

            
            if student_class == '' and student_section == '' and student_roll_no=='':
                # print "NOTHING IS GIVEN---GET FULL SCHOOL LIST"
                student=Student.objects.all()
                if student.count()==0:
                    context["no_student"]="No Students Available"
                    return self.render_to_response(context)


                context["all_students"]=student
                if student:
                    context["show_table"]=True
                    saved_students=student

            elif student_section == '' and student_roll_no=='':
                # print "ONLY CLASS IS GIVEN---GET CLASSWISE LIST"
                student=Student.objects.filter(classes=student_class)
                if student.count()==0:
                    context["no_student"]="No Students Available"
                    return self.render_to_response(context)

                context["all_students"]=student

                if student:
                    context["show_table"]=True
                    saved_students=student

            elif student_roll_no=='':
                # print "CLASS and SECTION GIVEN ---GET CLASS AND SECTION LIST"
                student=Student.objects.filter(classes=student_class, section=student_section)
                if student.count()==0:
                    context["no_student"]="No Such Students Available"
                    return self.render_to_response(context)

                context["all_students"]=student
                if student:
                    context["show_table"]=True
                    saved_students=student

            elif student_class != '' and student_section != '' and student_roll_no!='':
                # print "EVERYTHING IS GIVEN --- ---GET PARTICULAR STUDENT"
                student=Student.objects.filter(classes=student_class, section=student_section, roll_no=student_roll_no)
                if student.count()==0:
                    context["no_student"]="No Such Student Available"
                    return self.render_to_response(context)

                context["all_students"]=student
                if student:
                    context["show_table"]=True
                    saved_students=student

            # return self.render_to_response(context)

        
        if 'send_message_button' in data:
            print "Clicked SEND MESSAGE"
            if message_text and message_text != '':
                context["message_sent"]="Message Sent Successfully"
                print "Message is not Empty"
                message = Message(message=message_text)
                message.save()

                # message_status = MessageStatus()
                for student in saved_students:
                    message.students.add(student)
                return self.render_to_response(context)

                # print "This Message", message_text,"being sent to:"
                # for student in saved_students:
                #     print student.classes

        return self.render_to_response(context)

class BulkUploadView(generic.FormView):
    template_name="smsapp/index.html"
    model=ContactFile

    def post(self, request, *args, **kwargs):
        context={}
        data=request.POST
        # print "data-------->",data
        filename=request.FILES['bulk_upload_file']

        contacts=ContactFile(filename=filename)
        contacts.save()

        filedata = csv.reader(filename)
        # print "FILEDATA------>",filedata
        for row in filedata:
            if filedata.line_num==1:
                continue
            first_name = row[0]
            last_name = row[1]
            parentage = row[2]
            email = row[3]
            contact = row[4]
            gender = row[5]
            address = row[6]
            pincode = row[7]
            classes = row[8]
            section = row[9]
            roll_no = row[10]
            student=Student(
                        first_name = first_name, last_name = last_name,
                        parentage = parentage, email = email, contact = contact,
                        gender = gender, address = address, pincode = pincode,
                        classes = classes, section = section,roll_no = roll_no
                        )
            student.save()
        
            # context["upload"]= "Student File Uploaded Successfully"
            messages.success(request, "Student File Uploaded Successfully")
        return HttpResponseRedirect(reverse('dashboard'))
        # return self.render(request,'dashboard',context)

class DashboardView(generic.TemplateView):
    template_name = "smsapp/index.html"


    def get(self, request, *args, **kwargs):
        # print "GET METHOD OF DASHBOARD VIEW"
        student_list=Student.objects.all()
        message_list = Message.objects.all()
        user_list = User.objects.latest('id')
        context = {"student_list":student_list, "message_list":message_list,"user_list":user_list}
        context["dashboard_click"]=True

        data = request.GET

        # if 'upload_button' in data:
        #     context["upload"]="Student File Uploaded Successfully"
        #     return render_to_response(context)


        student_id=data.get('student_id')
        if student_id:
            student=Student.objects.get(id=student_id)
            context["student"]=student
            context["show"]=True
            context["edit_click"]=True
            context["dashboard_click"]=False
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {}
        student_list=Student.objects.all()
        context = {"student_list":student_list}
        
        data = request.POST
        # print "-----------data from request.POST------------------",data

        if 'add_student_button' in data:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            parentage = data.get('parentage')
            email = data.get('email')
            contact = data.get('phone')
            gender = data.get('gender')
            address = data.get('address')
            pincode = data.get('zip')
            classes = data.get('class')
            section = data.get('section')
            roll_no = data.get('roll_no')
            student=Student(
                        first_name = first_name, last_name = last_name,
                        parentage = parentage, email = email, contact = contact,
                        gender = gender, address = address, pincode = pincode,
                        classes = classes, section = section,roll_no = roll_no
                        )
            student.save()
            context["success"]="Student Added Succesfully"
            context["add_click"]=True
            # print "**************************","You Clicked Add Student Button"

        elif 'edit_student_button' in data:
            first_name = data.get('edit_first_name')
            last_name = data.get('edit_last_name')
            parentage = data.get('edit_parentage')
            email = data.get('edit_email')
            contact = data.get('edit_phone')
            gender = data.get('edit_gender')
            address = data.get('edit_address')
            pincode = data.get('edit_zip')
            classes = data.get('edit_class')
            section = data.get('edit_section')
            roll_no = data.get('edit_roll_no')
            student_id=data.get('hidden_student_id')

            student=Student.objects.filter(id=student_id).update(
                        first_name = first_name, last_name = last_name,
                        parentage = parentage, email = email, contact = contact,
                        gender=gender, address = address, pincode = pincode,
                        classes = classes, section = section,roll_no = roll_no,
                        updated_date=datetime.datetime.now()
                        )
            context["edit_success"]="Student Data Updated Succesfully"
            context["edit_click"]=True
        return self.render_to_response(context)

class LoginView(generic.TemplateView):
	template_name = "smsapp/signin.html"

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('dashboard'))
		context = {}
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		context = {"error":"Provide correct credentials"}
		data = request.POST
		username = data.get('username')
		password = data.get('password')
		user = authenticate(username=username,password=password)
		try:
			if user is not None:
				login(request,user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				return self.render_to_response(context)
		except:
			return self.render_to_response(context)

class RegisterView(generic.TemplateView):
	template_name = "smsapp/register.html"

	def get(self, request, *args, **kwargs):
		context = {}
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		context = {"success":"Profile created successfully. Kindly Login"}
		data=request.POST
		# print data
		firstname=data.get('first_name')
		lastname=data.get('last_name')
		email=data.get('email')
		username = data.get('username')
		password = data.get('password')
		user = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username)
		user.set_password(password)
		# print user,"Create User Object"
		user.save()
		# print user,"Saved to database already"
		return self.render_to_response(context)
		# return HttpResponseRedirect(reverse('login'))

class LogoutView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated():
			logout(self.request)
		return HttpResponseRedirect(reverse('login'))

class IndexView(generic.TemplateView):
    template_name="smsapp/index.html"


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

import datetime
import csv
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from models import Student, ContactFile, Message, MessageStatus
from django.core.urlresolvers import reverse
from django.http import JsonResponse
import json
from django.core import serializers

# Create your views here.

from twilio.rest import Client
from django.core.exceptions import MiddlewareNotUsed
import os
import logging

logger = logging.getLogger(__name__)

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio notification
middleware. Required enviroment variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""


def load_twilio_config():
    twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_NUMBER


    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)

class MessageClient(object):
    def __init__(self):
        (twilio_number, twilio_account_sid, twilio_auth_token) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid,
                                              twilio_auth_token)

    def send_message(self, body, to):
        self.twilio_client.messages.create(body=body, to=to,
                                           from_=self.twilio_number,
                                           # media_url=['https://demo.twilio.com/owl.png'])
                                           )

class SendView(generic.TemplateView):
    template_name="smsapp/index.html"
    saved_students={}

    def get(self, request, *args, **kwargs):
        context={}
        if request.is_ajax():
            data = request.GET
            classes=data.get('select_class')
            section=data.get('select_section')

            print "data------------>",data
            
            if 'select_section' in data:
                student=Student.objects.filter(classes=classes, section=section, user_id=current_user_id)
                student_list=[]
                for std in student:
                    if std.roll_no not in student_list:
                        student_list.append(std.roll_no)
                response_data = sorted(student_list)
                print "Response:",response_data

            elif 'select_class' in data: 
                student=Student.objects.filter(classes=classes, user_id=current_user_id)
                student_list=[]
                for std in student:
                    if std.section not in student_list:
                        student_list.append(std.section)
                response_data = sorted(student_list)
                print "RESPONSE",response_data

            return JsonResponse(response_data, safe=False)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        global saved_students 
        student_list=Student.objects.filter(user_id=current_user_id)
        message_list = Message.objects.filter(user_id=current_user_id)
        context = {"student_list":student_list, "message_list":message_list}
        context["send_click"]=True

        data = request.POST
        student_class = data.get('class', None)
        student_section = data.get('section', None)
        student_roll_no = data.get('roll_no', None)
        message_text = data.get('message_text', None)

        if 'get_student_list' in data:
            
            if student_class == '' and student_section == '' and student_roll_no=='':
                # print "NOTHING IS GIVEN---GET FULL SCHOOL LIST"
                student=Student.objects.filter(user_id=current_user_id)
                if student.count()==0:
                    context["no_student"]="No Students Available"
                    return self.render_to_response(context)


                context["all_students"]=student
                if student:
                    context["show_table"]=True
                    saved_students=student

            elif student_section == '' and student_roll_no=='':
                # print "ONLY CLASS IS GIVEN---GET CLASSWISE LIST"
                student=Student.objects.filter(classes=student_class, user_id=current_user_id)
                if student.count()==0:
                    context["no_student"]="No Students Available"
                    return self.render_to_response(context)

                context["all_students"]=student

                if student:
                    context["show_table"]=True
                    saved_students=student

            elif student_roll_no=='':
                # print "CLASS and SECTION GIVEN ---GET CLASS AND SECTION LIST"
                student=Student.objects.filter(classes=student_class, section=student_section, user_id=current_user_id)
                if student.count()==0:
                    context["no_student"]="No Such Students Available"
                    return self.render_to_response(context)

                context["all_students"]=student
                if student:
                    context["show_table"]=True
                    saved_students=student

            elif student_class != '' and student_section != '' and student_roll_no!='':
                # print "EVERYTHING IS GIVEN --- ---GET PARTICULAR STUDENT"
                student=Student.objects.filter(classes=student_class, section=student_section, roll_no=student_roll_no, user_id=current_user_id)
                if student.count()==0:
                    context["no_student"]="No Such Student Available"
                    return self.render_to_response(context)

                context["all_students"]=student
                if student:
                    context["show_table"]=True
                    saved_students=student

        if 'send_message_button' in data:
            if message_text and message_text != '':
                message = Message(message=message_text, user_id=current_user_id)
                message.save()
                context["message_sent"]="Message Sent Successfully"

                twilio_client=MessageClient()
                twilio_client.send_message(message_text,'+919596062959')
                
                # for student in saved_students:
                #     twilio_client.send_message(message_text,student.contact)

                for student in saved_students:
                    message.students.add(student)
                return self.render_to_response(context)
            else:
                context["message_not_sent"]="Message not Sent"
                return self.render_to_response(context)
                        
        return self.render_to_response(context)

class BulkUploadView(generic.FormView):
    template_name="smsapp/index.html"
    model=ContactFile

    def post(self, request, *args, **kwargs):
        context={}
        data=request.POST
        filename=request.FILES['bulk_upload_file']

        contacts=ContactFile(filename=filename)
        contacts.save()

        filedata = csv.reader(filename)
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
                        classes = classes, section = section,roll_no = roll_no,
                        user_id=current_user_id
                        )
            student.save()
        
            
        messages.success(request, "Student File Uploaded Successfully", extra_tags='alert-success')
        return HttpResponseRedirect(reverse('dashboard'))

class DashboardView(generic.TemplateView):
    template_name = "smsapp/index.html"


    def get(self, request, *args, **kwargs):
        global current_user_id

        current_user_id = request.user.id

        student_list = Student.objects.filter(user_id=current_user_id)
        message_list = Message.objects.filter(user_id=current_user_id)
        user_list = User.objects.latest('id')
        
        context = {'student_list':student_list, 'message_list':message_list,'user_list':user_list}
        context['dashboard_click']=True        
        
        data = request.GET
        student_id = data.get('student_id')
        if request.is_ajax():

            obj_json = serializers.serialize('json', Student.objects.filter(id=student_id))
            obj_list = json.loads(obj_json)
            json_data = json.dumps(obj_list)

            print "--------------------"
            print "JSON Data", json_data
            print "--------------------"
            
            return HttpResponse(json_data, content_type='application/json')

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {}
        student_list = Student.objects.filter(user_id=current_user_id)
        context = {"student_list":student_list}
        
        data = request.POST
        print "DATA POST",data

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
                        classes = classes, section = section,roll_no = roll_no,
                        user_id=current_user_id
                        )
            student.save()
            context["success"]="Student Added Succesfully"
            context["add_click"]=True

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
			current_user= request.user
			print "CURRENT USER ID", current_user.id
			return HttpResponseRedirect(reverse('dashboard'))
		context = {}
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		context = {"error":"Provide correct credentials"}
		# current_user=request.user
		data = request.POST
				
		
		username = data.get('username')
		password = data.get('password')
		print(username,password)
		# print "USER",current_user
		user = authenticate(username=username,password=password)
		try:
			if user is not None:
				print user
				
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
		username = request.GET.get('username')

		if request.is_ajax():
			context['is_taken'] = User.objects.filter(username__iexact = username).exists()
			if context['is_taken']:
				context['username_error']="Username already taken by someone"
				return JsonResponse(context)
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		context = {}
		data=request.POST

		firstname=data.get('first_name')
		lastname=data.get('last_name')
		email=data.get('email')
		username = data.get('username')
		password = data.get('password')

		context = {
			'is_taken': User.objects.filter(username__iexact = username).exists()
		}
		if context['is_taken']:
			context["username_error"]="Kindly change Username as this username already taken."
		else:
			user = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username)
			user.set_password(password)
			user.save()
			context["success"]="Profile created successfully. Kindly Login"
		return self.render_to_response(context)
		
class LogoutView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated():
			logout(self.request)
		return HttpResponseRedirect(reverse('login'))








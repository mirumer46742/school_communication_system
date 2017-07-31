# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ContactFile(models.Model):
    filename = models.FileField(upload_to = 'media/document')
 
class Student(models.Model):
	GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	parentage = models.CharField(max_length = 80)
	email = models.EmailField(null = True,blank = True)
	contact = models.CharField(max_length = 12)
	gender = models.CharField(max_length = 1, choices = GENDER_CHOICE)
	address = models.CharField(max_length = 100, null = True, blank = True)
	pincode = models.CharField(max_length = 6)
	classes = models.CharField(max_length = 10)
	section = models.CharField(max_length = 2)
	roll_no = models.CharField(max_length = 3)
	added_date = models.DateTimeField(auto_now = True)
	updated_date = models.DateTimeField(auto_now = True)
	user =models.ForeignKey(User)



class Message(models.Model):
	students = models.ManyToManyField(Student)
	user =models.ForeignKey(User)
	message = models.CharField(max_length = 1000)

class MessageStatus(models.Model):
	sent_status = models.BooleanField()
	sent_date = models.DateTimeField(auto_now = True)
	message = models.ForeignKey(Message)


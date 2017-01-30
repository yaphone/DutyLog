#coding=utf-8

from __future__ import unicode_literals

from django.db import models


# Create your models here.

#目前通过page_no关联各模型

class DutyInfo(models.Model):
    duty_time = models.DateTimeField()
    duty_leader = models.CharField(max_length = 128)
    duty_man = models.CharField(max_length = 128)
    duty_manager = models.CharField(max_length = 128)
    duty_proxy= models.CharField(max_length = 128)   #带班领导
    date = models.CharField(max_length = 128, default="2017-1-1") #日期
    weekday = models.CharField(max_length = 128) #
    weather = models.CharField(max_length = 128) #
    temp = models.CharField(max_length = 128)
    page_no = models.IntegerField()


class ContentTable(models.Model):
    content = models.CharField(max_length = 4000)
    content_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    page_no = models.IntegerField()


class InstructionTable(models.Model):
    instruction = models.CharField(max_length = 4000)
    instruction_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    page_no = models.IntegerField()

class ProxyInstructionTable(models.Model):
    proxy_instruction = models.CharField(max_length=4000)
    proxy_instruction_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    page_no = models.IntegerField()

class ResultTable(models.Model):
    result = models.CharField(max_length = 4000)
    result_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    page_no = models.IntegerField()

class RoleTable(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    #roleflag 1: 值班员 2：值班领导  3：值班
    roleflag = models.CharField(max_length=128)
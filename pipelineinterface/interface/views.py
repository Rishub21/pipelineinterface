
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import subprocess
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from interface.tasks import analysis
from interface.models import celeryResponse
import time

# Create your views here.

def index(request):


    if request.user.is_authenticated():

        #print "This is a return to the index page"
        output = subprocess.check_output("java -cp .:./gson-2.7.jar Utilities getProjectsJSON myseqpath", cwd = "/Users/anitanahar/Desktop/PythonProjects/pythonpaths/java_class/", shell = True)
        output = output.replace("miseqPath:test", "")
        output = output.replace("[", "")
        output = output.replace("]", "")
        output = output.split(",")
        context_dict = {"output" : output}

        return render(request, "interface/listings.html", context_dict)

    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

        #context_dict = {'boldmessage': "I am bold font from the context"}
        #return render(request, 'interface/index.html', context_dict)

def waiting(request):
    return render(request, "interface/waiting.html")



def chart(request, chart_title):
    pvalue_list = []
    checked_list = []
    chart_head = chart_title[1:-1]
    output  = subprocess.check_output("java -cp .:./gson-2.7.jar Utilities getProjectSamplesJSON miseqPath samplename" + chart_head, cwd = "/Users/anitanahar/Desktop/PythonProjects/pythonpaths/java_class/", shell = True)
    #consider using popen instead of subprocess
    output = output.split("],")
    for i in range(len(output)):
        output[i] = output[i].split(",")
        for u in range(3):
            output[i][u] = output[i][u].strip('"')
    #print output
    table_list = output # default list just for testing purposes
    length = len(table_list)
    emptylist = [None] * length
    context_dict = {"chart_head" : chart_head, "table_list" : table_list, "emptylist": emptylist }
    #print table_list

    if request.method == "POST":
        checked_list = request.POST.getlist("selection")
        # this is getting the sample names based on which boxes were checked
        print "this is checked_list"

        print checked_list

        for samplename in checked_list:
            boxname = samplename # the name of the respective textbox on the chartings template

            pvalue_list.append(request.POST.get(boxname)) #pvalues of checked boxes
        #print pvalue_list
        #print checked_list


        #for listing in checked_list:
        #    print listing

        analysis.delay(pvalue_list) # delay is pushing this task off to the celery que

        subprocess.call("celery worker -A pipelineinterface -l info", shell = True) #now we are firing the celery worker to execute tasks from that
        #return render(request, "interface/waiting.html", context_dict)
        #my_messages = celeryResponse.objects.order_by("output") # order the messages alphabetically
        #print my_messages
        print "can we go after asynch"


    return render(request, "interface/chartings.html", context_dict)

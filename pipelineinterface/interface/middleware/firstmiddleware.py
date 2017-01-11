from datetime import datetime
from json import dumps
from django.contrib import auth
from django.shortcuts import redirect
import sys

current_time = datetime.now()


class AutoLogout:
    def process_request(self, request):


        if not request.user.is_authenticated() :
            if "last_visit" in request.COOKIES :
                del request.COOKIES["last_visit"]
      #Can't log out if not logged int
        else:

            #print "is authenticated"
            #print request.COOKIES.get("last_visit")

            if "last_visit" in request.COOKIES :
                #print "step 1 : identify"

                last_visit = request.COOKIES["last_visit"]
                #print last_visit
                last_visit_time = datetime.strptime(last_visit[:-7],'%Y-%m-%d %H:%M:%S')
                #print current_time - last_visit_time

                if (datetime.now() - last_visit_time).seconds > 15:
                #    print "step 2: the logout"
                    request.COOKIES['last_visit'] = datetime.now()
                    #response.set_cookie("last_visit", datetime.now())
                #    print request.COOKIES.get("last_visit")
                #    print datetime.now()-last_visit_time
                #    print "cookie changed"
                    auth.logout(request)

    def process_response(self, request,response):
        if not "last_visit" in request.COOKIES:
            response.set_cookie("last_visit", datetime.now())
            #print "initial cookie set"
        return response

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm
from django.views.generic import TemplateView
#import urllib3
from django.contrib.auth import authenticate, login, logout


class HomePageView(TemplateView):
    template_name = "site/index.html"
'''
    login_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.login_form
        context['content'] = "You are in site HomePage"
        return context

    def get(self, request, *args, **kwargs):
        form = self.login_form()
        return render (request,self.template_name,self.get_context_data())
#        return render (request,self.template_name,{'login_form':form,'user':request.user})        

    def post(self, request, *args, **kwargs):
        form = self.login_form(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
        return render (request,self.template_name,self.get_context_data())
#        return render (request,self.template_name,{'login_form':form,'user':request.user})        
'''

class InprogressView(HomePageView):
    template_name = "demoweb/in_progress.html"

'''
def root_index(request):

#    if request.method == "POST":
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request,user)
    """
    else:
        user = None
    """
    login_form = LoginForm()

    return render (request,'demo/index.html',{'login_form':login_form,'user':request.user})
#    return HttpResponse("Hello, world. You're at the root index.")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
    return HttpResponseRedirect('/')


#def root_index(request):
#    return HttpResponse("Hello, world. You're at the root index.")
'''

"""
Prefix="http://www.avarun.cn:3838/"  
http = urllib3.PoolManager()
  
def proxy_api(request):  
3def root_index(request):  
    url = request.get_full_path()  
    url = Prefix+url  
  
    req = http.request("GET",url)  

    info = req.info()  
    data = req.data  
    return HttpResponse(data, content_type=info.get("content-type"))
"""




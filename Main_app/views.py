from asyncio.format_helpers import _format_callback
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
import requests
import json
from . import models,forms
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
def compare_solution(sol1,sol2,input):
    print(sol1)
    print(sol2)
    print(input)
    reqbody1 = {
        "script": sol1,
        "stdin": input,
        "language": "cpp",
        "versionIndex": "0",
        "clientId": "40a0dcdf5b223f5f5fb928e3266288bc",
        "clientSecret": "d8bfe6707673b03583f6d52a03bac9d40fd387df3a5e3d1fd096490fc25869ba"
    }
    r = requests.post('https://api.jdoodle.com/v1/execute',json=reqbody1)
    print(r)
    json_data = json.loads(r.text)
    print(json_data)
    first_output = json_data['output']
    reqbody2 = {

        "script": sol2,
        "stdin": input,
        "language": "cpp",
        "versionIndex": "0",
        "clientId": "40a0dcdf5b223f5f5fb928e3266288bc",
        "clientSecret": "d8bfe6707673b03583f6d52a03bac9d40fd387df3a5e3d1fd096490fc25869ba"
    }

    r = requests.post('https://api.jdoodle.com/v1/execute',json=reqbody2)
    print(r)
    json_data = json.loads(r.text)
    print(json_data)
    second_output = json_data['output']
    return (first_output==second_output)
@login_required
def home_page(request):
    print(request.user.pk)
    return render(request,'Main_app/home.html')
class user_login(View):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('Main_app:home'))
        else:
            return HttpResponse("Invalid login details supplied.")
    def get(self,request):
        form = forms.LoginForm()
        return render(request, 'Main_app/login.html',{'form':form})

class problem_list(ListView):
    context_object_name = 'problem_list'
    model = models.Problems
    template_name ='Main_app/problem_list.html'

class create_problem(CreateView):
    model = models.Problems
    fields = ['Title','Problem_statement','Author','Test_cases','Example_test_cases','Solution','points' ]
    template_name = 'Main_app/problem_form.html'
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        user = request.user
        if(user):
            if(user.user_info.is_problemsetter):

                return super().get(request,*args,**kwargs)
        else:
            return HttpResponse('You cannot Create a Problem, as you are not a problem setter!')
class submission_list(ListView):
    context_object_name = 'submission_list'
    model = models.Submissions
    template_name = 'Main_app/submission_list.html'
@login_required
def my_submission_list(request):

    context = {'user':request.user}
    print(request.user.submissions.all)
    return render(request,'Main_app/my_submissions.html',context)

def register_user(request):
    form_class = forms.UserForm
    template_name = 'Main_app/register_user.html'
    success_url= 'Main_app/problem'
    form1 = forms.UserForm()
    form2 = forms.UserInfoForm()
    if(request.method=='POST'):
        form1 = forms.UserForm(data=request.POST)
        form2 = forms.UserInfoForm(data=request.POST)
        if(form1.is_valid() and form2.is_valid):
            print(form1)
            user = form1.save()
            user.set_password(user.password)
            user.save()
            profile = form2.save(commit=False)
            profile.user = user
            print(form2)
            print(request.FILES)
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            
            return HttpResponseRedirect(reverse('Main_app:home'))
        else:
            return render(request,template_name,{'form1':form1,'form2':form2})

    else:
        return render(request,template_name,{'form1':form1,'form2':form2})

class problem_detail_view(FormView,DetailView):
    model = models.Problems
    context_object_name = 'problem'
    template_name=  'Main_app/problem.html'
    form_class = forms.SolutionForm
    success_url = '/Main_app/submissionlist'
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        return super().post(self,request,*args,**kwargs)
    def form_valid(self, form):
        if(self.request.user.is_authenticated):

            obj = form.save()
            obj.problem = self.get_object()
            before = obj.accepted
            is_correct = compare_solution(obj.solution,obj.problem.Solution,obj.problem.Test_cases)
            obj.accepted = is_correct
            obj.user = self.request.user
            currentobject = self.get_object()
            currentobject.Number_of_submissions = currentobject.Number_of_submissions+1
            if(obj.accepted):
                currentobject.Number_of_accepted = currentobject.Number_of_accepted+1
                userinfo = obj.user.user_info
                if(before==False):
                    userinfo.points = userinfo.points+currentobject.points
                userinfo.save()
            obj.save()
            currentobject.save()
            print(currentobject.Number_of_submissions)
            return super().form_valid(form)
        else:
            return super().form_valid(form)
class friends_list(ListView):
    model = models.Friends
    context_object_name = 'friends'
    def get_queryset(self):
        qs = models.Friends.objects.filter(user1=self.request.user)
        return qs
class user_details(DetailView,FormView):
    model = models.User_info
    context_object_name = 'user'
    template_name = 'Main_app/user_details.html'
    form_class = forms.FriendsForm
    success_url = None
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        is_friend = None
        try:
            is_friend = models.Friends.objects.get(user1 = self.request.user,user2 = context['user'].user)
        except models.Friends.DoesNotExist:
            is_friend = None
        if(is_friend):
            context['is_friend'] = is_friend
        else:
            context['is_friend'] = None
        self.context_data = context
        print(self.context_data['user'].user)
        print('This is context_data')
        print(self)
        return context
    def post(self,request,*args,**kwargs):
        print(self)
        make_friend = request.POST.get('make_friend')
        print(super().get_object().user)
        friends = models.Friends()
        friends.user1 = self.request.user
        friends.user2 = super().get_object().user
        is_friend = None
        if(make_friend):
            try:
                print('I tried coming inside post')
                is_friend = models.Friends.objects.get(user1 = self.request.user,user2 = friends.user2)
                print(is_friend)
                is_friend.delete()
            except models.Friends.DoesNotExist:
                is_friend = None
                friends.save()
        return HttpResponseRedirect(request.path)

class user_list(ListView):
    model = models.User_info
    context_object_name = 'user'
    template_name = 'Main_app/user_list.html'
    
class submission_detail(DetailView):
    model = models.Submissions
    context_object_name = 'submission'
    template_name = 'Main_app/submission_detail.html'
@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('Main_app:problemlist'))
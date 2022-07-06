from django.urls import path 
from . import views

app_name = 'Main_app' 
urlpatterns = [
    path('friends/', views.friends_list.as_view(),name='friendslist'),
    path('mysubmissions/', views.my_submission_list,name='registeruser'),
    path('challenge/', views.my_submission_list,name='registeruser'),
    path('submission/<pk>/', views.submission_detail.as_view(),name='submission'),
    path('register/', views.register_user,name='registeruser'),
    path('login/', views.user_login.as_view(),name='userlogin'),
    path('', views.home_page,name='home'),
    path('createproblem/', views.create_problem.as_view(),name='createproblem'),
    path('logout/',views.user_logout,name='logout'),
    path('problemlist/', views.problem_list.as_view(),name='problemlist'),
    path('submissionlist/', views.submission_list.as_view(),name='submissionlist'),
    path('userlist/',views.user_list.as_view(),name='userlist'),
    path('user/<pk>/',views.user_details.as_view(),name='userdetails'),
    path('<pk>/', views.problem_detail_view.as_view(),name='problem'),
]
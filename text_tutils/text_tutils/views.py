import re
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    params = {'Name': 'Arnav' , 'Place':'Lucknow'}
    return render(request, 'index.html',params)

def personal(Request):
    params={'Contact Number': 9415111172,'E-Mail':'aarnavlko@gmail.com'}
    return render(Request,'personal_info.html',params)
   # return HttpResponse(" Name: Arnav Khandelwal<br>Age:19<br>Interest: Python<br>Current Proficiency in Django: Beginner")

def Django_learn(Request):
    return HttpResponse(''' Link to study Django<br><br> <a href='https://www.youtube.com/watch?v=AepgWsROO4k&list=PLu0W_9lII9ah7DDtYtflgwMwpT3xmjXY9&index=7'> Django Playlist for Begineer</a> ''')

def Machine_Learning(Request):
    return HttpResponse(''' Access to Machine Learning tutorial is down below<br><br> <a href="https://www.youtube.com/watch?v=gmvvaobm7eQ&list=PLeo1K3hjS3uvCeTYTeyfe0-rN5r8zn9rw" > ML Playlist </a> ''')

def Functionality(Request):
    return HttpResponse(''' Based on User Descrition : <br> <a href='/' > <br>Go To Home </a><br><br> <a href='/personal' > User Details <a/>''')
    
def sentence_transformation(Request):
    punctuations_option= Request.POST.get('removepunc','off')
    text_input= Request.POST.get('text','No Input')
    option=Request.POST.get('User Details','off')
    edited_text=""
    details=""
    if punctuations_option == 'on':
        punctuations= '''.,!#"':;?/@$%^&*"<>+=_-)(~`'''
        edited_text = ''.join(char for char in text_input if char not in punctuations)
        
    if option =='on':
        pattern = 'name is ([a-zA-z ]*) ' 
        _name_=re.findall(pattern,text_input)
        pattern2='from ([a-zA-z ]*) city'
        _city_=re.findall(pattern2,text_input)
        pattern3='student in ([a-zA-Z ]*)'
        _study_=re.findall(pattern3,text_input)
        
        
        _name_ = _name_[0] if _name_ else "Not Found"
        _city_ = _city_[0] if _city_ else "Not Found"
        _study_ = _study_[0] if _study_ else "Not Found"
        details = f"Name: {_name_}<br>City: {_city_}<br>Institute: {_study_}"

    
    if option == 'off' and punctuations_option =='off':
        return HttpResponse("Error!<br>No Action Selected")
    
    params={'purpose':punctuations_option,'action':edited_text,'Information':details}
    return render(Request,'analyze.html',params)
      
def user_feedback(Request):
    name_for_complaint=Request.POST.get('User_name','Anonymous')
    contact_number_for_complaint=Request.POST.get('Contact','default')
    _text_=Request.POST.get('djtext','No Issue')
    print(contact_number_for_complaint)
    print(name_for_complaint)
    params={'NAME':name_for_complaint,'CONTACT':contact_number_for_complaint,'Issue':_text_}
    return render(Request,'HelpDesk.html',params)

def github_ML(Request):
    return HttpResponse('''Documentation is the Key to Improvement! <a href="https://github.com/Arnav-api/Kaggle_Competition"> ML projects </a> ''')

def github_DJANGO(Request):
    return HttpResponse('''Documentation is the Key to Improvement! <a href="https://github.com/Arnav-api/Django_ML-Projects"> Django Basics </a>''')
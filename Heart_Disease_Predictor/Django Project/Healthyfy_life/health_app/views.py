from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : 9415111172 , "Email-Id":"aarnavlko@gmail.com"}
    return render(request,'index.html',params)

def contact(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : 9415111172 , "Email-Id":"aarnavlko@gmail.com"}
    return render(request,'index.html',params)

def feedback(request):
    name = request.POST.get("text","User")
    email_id = request.POST.get("id")
    issue = request.POST.get("issue")
    params = {'Name':name,'Email_Id':email_id,'Feedback':issue}
    print(f"{name},{email_id},{issue}")
    return render(request,'input2.html',params)

def support(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : "9415111172" , "Email-Id":"aarnavlko@gmail.com"}
    return render(request,'input.html',params)

def Contact(request):
    params = {'Name':'Arnav Khandelwal' , "Contact_Number" : 9415111172 , "Email_Id":"aarnavlko@gmail.com"}
    return render(request,'developer.html',params)

def Heart_disease(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : 9415111172 , "Email-Id":"aarnavlko@gmail.com"}
    return render(request,'heart.html',params)
    
def requirement_details(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : 9415111172 , "Email-Id":"aarnavlko@gmail.com"}    
    return render(request,'detail.html',params)
# Create your views here.
def prediction(request):
    import joblib
    import pandas as pd

    model = joblib.load(r"C:\Users\aarna\model.pkl")
    scaler = joblib.load(r"C:\Users\aarna\scaler.pkl")
    encoder = joblib.load(r"C:\Users\aarna\encoder.pkl")

    age = request.POST.get("age","18")
    gender = request.POST.get("gender","M")
    ChestPain = request.POST.get("ChestPainType","ATA")
    RestingECG = request.POST.get("RestingECG","Normal")
    ST_Slope = request.POST.get("ST_Slope")
    Exercise_Angina = request.POST.get("ExerciseAngina")
    Old_Peak = request.POST.get("OldPeak")
    FastingBS = request.POST.get("FastingBS")
    Max_HR = request.POST.get("MaxHR")
    RestingBP = request.POST.get("RestingBP")
    Cholesterol = request.POST.get("Cholesterol")
    data_dict = {
    'Age': [int(age)],  # convert to int
    'Sex': [gender],
    'ChestPainType': [ChestPain],
    'RestingBP' : [RestingBP],
    'Cholesterol' : [Cholesterol],
    'FastingBS' : [FastingBS],
    'RestingECG': [RestingECG],
    'MaxHR' : [Max_HR],
    'ExerciseAngina' : [Exercise_Angina],
    'Oldpeak' : [Old_Peak],
    'ST_Slope': [ST_Slope],
    }

    data = pd.DataFrame(data_dict)
    scaled = scaler.transform(data[['Age','RestingBP','Cholesterol','FastingBS','MaxHR']])
    encoded = encoder.transform(data[['Sex','ChestPainType','RestingECG','ExerciseAngina','ST_Slope']])
    encoded.drop(['Sex_M','ChestPainType_ASY','RestingECG_ST','ExerciseAngina_N','ST_Slope_Flat'],axis=1,inplace=True)
    data = pd.concat([data,encoded],axis = 1).drop(['Sex','ChestPainType','RestingECG','ExerciseAngina','ST_Slope'],axis = 1)
    

# Predict
    prediction = model.predict(data)
    if prediction == 1:
        message = "Signs of a Heart Disease, Consult a doctor to be on a safer side"
        return render(request, "result.html", {"message": message})
    else:
        message = "No apparent signs of Heart Disease, keep maintaining a healthy lifestyle!"
        return render(request, "result2.html", {"message": message})
     
    #return render(request, "result.html", {"message": message})

    #return HttpResponse (f"Hey launched {age}, {gender},{ChestPain},{RestingECG},{ST_Slope},{Cholesterol},{RestingBP},{Max_HR},{FastingBS} ,{prediction}")
    

    
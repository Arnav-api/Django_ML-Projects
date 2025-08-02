from django.shortcuts import render
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def home(request):
    params= {"name":"Arnav Khandelwal"}
    return render (request,'home.html',params)
# Create your views here.
def upload_view(request):
    if request.method == "POST":
        params= {"name":"Arnav Khandelwal"}
        return render (request,"upload.html",params)
    return render(request, "upload.html")

def Heart_disease(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : 9415111172 , "Email-Id":"aarnavlko@gmail.com"}
    return render(request,'heart.html',params)

def requirement_details(request):
    params = {'Name':'Arnav Khandelwal' , "Contact Number" : 9415111172 , "Email-Id":"aarnavlko@gmail.com"}    
    return render(request,'detail.html',params)

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
    ST_Slope = request.POST.get("ST_Slope","Up")
    Exercise_Angina = request.POST.get("ExerciseAngina", "N")  # Assume "N" = No
    ST_Slope = request.POST.get("ST_Slope", "Flat")            # or whatever default was used in training
    Old_Peak = request.POST.get("OldPeak", "0.0")
    FastingBS = request.POST.get("FastingBS", "0")
    Max_HR = request.POST.get("MaxHR", "100")
    RestingBP = request.POST.get("RestingBP", "120")
    Cholesterol = request.POST.get("Cholesterol", "200")

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
    print(prediction[0])
    if prediction[0] == 1:
        message = "Signs of a Heart Disease, Consult a doctor to be on a safer side"
        return render(request, "result.html", {"message": message})
    else:
        message = "No apparent signs of Heart Disease, keep maintaining a healthy lifestyle!"
        return render(request, "result2.html", {"message": message})
     
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

def sign_prediction(request):
    import pickle
    import os
    name = request.POST.get("userid") 
    image = request.FILES.get("image")

    if not image:
        return HttpResponse("No image uploaded.")

    # Save uploaded image
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "uploads"))
    filename = fs.save(image.name, image)
    file_url = fs.url("uploads/" + filename)
    file_path = fs.path(filename)

    # Load required packages and model
    

# Replace with correct path to the .pkl file
    with open("label_map.pkl", "rb") as f:
        label_map = pickle.load(f)

# Reverse the dictionary: {0: 'a', 1: 'b', ...}
    index_to_label = {v: k for k, v in label_map.items()}

    import numpy as np
    from django.apps import apps
    from PIL import Image
    from tensorflow.keras.models import load_model

    app_path = apps.get_app_config('deep_learning').path
    model_path = os.path.join(app_path, 'ml_models', 'Cnn_model(1).h5') 
    model = load_model(model_path)

    # Prepare the image
    img = Image.open(file_path).convert('RGB').resize((64, 64))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 64, 64, 3)

    # Define class labels (must match training order)
    

    # Predict
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    result = index_to_label[predicted_index]

    print("Predicted label:", result)
    print("Prediction array:", prediction)

    # Prepare response
    params = {
        "name": name,
        "fs": fs,
        "filename": filename,
        "file_url": file_url,
        "result": result
    }
    return render(request, "image.html", params)

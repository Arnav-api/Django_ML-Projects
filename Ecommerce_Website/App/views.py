from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import Q
from django.conf import settings

from .models import UserProduct, ChatThread, ChatMessage, Profile
def home(request):
    params= {"name" : "Arnav Khandelwal" , "Contact_Number" : "9415111172"}
    return render(request,'index.html',params)
# Create your views here.
def image_processing(request):
    params={"name":"Arnav Khandelwal" , "Contact_Number" : "9415111172"}
    return render(request,'classification.html',params)

def Contact(request):
    params = {"name" : "Arnav Khandelwal" , "Contact_Number" : "9415111172","Email-Id":"aarnavlko@gmail.com"}
    return render(request,'contact.html',params)

def response (request):
    Name = request.GET.get("Username")
    Number = request.GET.get("number")
    Email = request.GET.get("email")
    Feedback = request.GET.get("feedback")
    params = {"Name" : Name , "Number" : Number , "Email" : Email , "Feedback" : Feedback}
    return render(request,'Feedback_accepted.html',params)

def ecommerce(request):
    params={"name":"Arnav Khandelwal"}  
    return render(request,'website.html',params)

    
def categories(request):
    params = {"name" : "Arnav Khandelwal"}
    return render(request,'categories.html',params)  

from django.shortcuts import render, redirect
from .models import UserProduct

@login_required
def selling(request):
    if request.method == "POST":

        product = UserProduct.objects.create(
            seller_user=request.user,                 # 🔥 FIX
            seller_name=request.user.username,        # auto
            country_code=request.POST.get("country_code"),
            mobile=request.POST.get("mobile"),

            category=request.POST.get("category"),
            price=request.POST.get("price"),
            condition=request.POST.get("condition"),
            description=request.POST.get("description"),

            original_image=request.FILES["images"]    # single image
        )

        return redirect(f"/detection/?id={product.id}")

    return render(request, "selling.html")

def object_classification(request):
    import os
    import uuid
    import cv2
    from ultralytics import YOLO
    from django.conf import settings
    from django.shortcuts import render

    if request.method != "POST":
        return render(request, "classification.html")

    uploaded_image = request.FILES.get("image")
    username = request.POST.get("userid", "User")

    if not uploaded_image:
        return render(request, "classification_result.html", {
            "error": "No image uploaded"
        })

    # ---------- Save uploaded image ----------
    input_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(input_dir, exist_ok=True)

    input_name = f"{uuid.uuid4().hex}.jpg"
    input_path = os.path.join(input_dir, input_name)

    with open(input_path, "wb+") as f:
        for chunk in uploaded_image.chunks():
            f.write(chunk)

    img = cv2.imread(input_path)

    # ---------- Load YOLO model ----------
    model = YOLO(os.path.join(settings.BASE_DIR, "models", "last.pt"))

    results = model.predict(input_path, conf=0.15, save=False)
    result = results[0]

    DAMAGE_CLASSES = {
        "damaged_phone",
        "damaged_phones",
        "damaged_tablet",
        "damaged_laptop",
        "damaged_camera",
        "damaged_region",
    }

    detected = False

    if result.boxes is not None:
        for box, cls_id, conf in zip(
            result.boxes.xyxy,
            result.boxes.cls,
            result.boxes.conf
        ):
            class_name = model.names[int(cls_id)].lower()
            confidence = float(conf)

            if class_name in DAMAGE_CLASSES and confidence > 0.15:
                detected = True
                x1, y1, x2, y2 = map(int, box)

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(
                    img,
                    f"Damaged Region {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2
                )

    # ---------- Save output ----------
    output_dir = os.path.join(settings.MEDIA_ROOT, "detections")
    os.makedirs(output_dir, exist_ok=True)

    output_name = f"detected_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(output_dir, output_name)
    cv2.imwrite(output_path, img)

    return render(request, "classification_result.html", {
        "username": username,
        "detected": detected,
        "image_url": f"{settings.MEDIA_URL}detections/{output_name}"
    })

from ultralytics import YOLO
import shutil, os
from django.conf import settings
from .models import UserProduct

def detection(request):
    import os
    import uuid
    import cv2
    from ultralytics import YOLO
    from django.conf import settings
    from django.shortcuts import render
    from .models import UserProduct

    product_id = request.GET.get("id")
    if not product_id:
        return render(request, "detection.html", {"error": "Invalid product ID"})

    product = UserProduct.objects.get(id=product_id)

    # Load original image
    img_path = product.original_image.path
    img = cv2.imread(img_path)

    # Load YOLO model
    model = YOLO(os.path.join(settings.BASE_DIR, "models", "last.pt"))

    # Run prediction (no auto-save)
    results = model.predict(img_path, conf=0.15, save=False)
    result = results[0]

    # 🔑 ALL classes that represent damage (internal)
    DAMAGE_CLASSES = {
        "damaged_phone",
        "damaged_phones",
        "damaged_tablet",
        "damaged_laptop",
        "damaged_camera",
        "damaged_region",   # future-proof
    }

    drawn_boxes = 0

    # Iterate over detections
    if result.boxes is not None:
        for box, cls_id, conf in zip(
            result.boxes.xyxy,
            result.boxes.cls,
            result.boxes.conf
        ):
            class_name = model.names[int(cls_id)].lower()
            confidence = float(conf)

            # ✅ Correct damage check
            if class_name in DAMAGE_CLASSES and confidence > 0.15:
                drawn_boxes += 1

                x1, y1, x2, y2 = map(int, box)

                # Draw bounding box
                cv2.rectangle(
                    img,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 0),
                    2
                )

                # ✅ Always show generic label to user
                cv2.putText(
                    img,
                    f"Damaged Region {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2
                )

    # ✅ Status decided ONLY by presence of damage boxes
    product.detection_status = "damaged" if drawn_boxes > 0 else "undamaged"

    # Save detected image with UNIQUE name
    output_dir = os.path.join(settings.MEDIA_ROOT, "user_products", "detected")
    os.makedirs(output_dir, exist_ok=True)

    output_name = f"detected_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(output_dir, output_name)

    cv2.imwrite(output_path, img)

    product.detected_image = f"user_products/detected/{output_name}"
    product.save()

    return render(request, "detection.html", {
        "detected_image": product.detected_image.url,
        "status": product.detection_status
    })


from .models import UserProduct
from django.db.models import Q
def product_detail(request, id):
    product = UserProduct.objects.get(id=id)
    return render(request, "product_detail.html", {"p": product})

def all_products(request):
    query = request.GET.get("q","")
    filter_status  = request.GET.get("status","")
    filter_category = request.GET.get("category", "")
    min_price = request.GET.get("min_price","")
    max_price = request.GET.get("max_price","")
    
    products = UserProduct.objects.all()
    if query:
        products = products.filter(
            Q(category__icontains=query) |
            Q(description__icontains=query) |
            Q(seller_name__icontains=query)
        )
    if filter_status == "damaged":
        products = products.filter(detection_status="damaged")

    elif filter_status == "undamaged":
        products = products.exclude(detection_status="damaged")


    # --- CATEGORY FILTER ---
    if filter_category:
        products = products.filter(category=filter_category)

    # --- PRICE FILTER ---
    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # --- ORDER BY NEWEST FIRST ---
    products = products.order_by("-uploaded_at")

    return render(request, "all_products.html", {
        "products": products,

        # keep filter values for UI
        "query": query,
        "filter_status": filter_status,
        "filter_category": filter_category,
        "min_price": min_price,
        "max_price": max_price,
    })
from django.shortcuts import render , get_object_or_404
from .models import UserProduct
def add_to_cart(request,id):
    product = get_object_or_404(UserProduct,id=id)
    return render (request , "add_to_cart.html" , {'product':product})
@login_required
def chat_view(request, product_id):
    product = get_object_or_404(UserProduct, id=product_id)

    if product.is_demo:
        return HttpResponseForbidden("Chat disabled for demo products")

    if not product.seller_user:
        return HttpResponseForbidden("Seller not linked")

    seller = product.seller_user

    # 🔹 Get or create chat ONLY if buyer
    if request.user != seller:
        thread, _ = ChatThread.objects.get_or_create(
            product=product,
            customer=request.user,
            seller=seller
        )
    else:
        # 🔹 Seller: must already have a chat
        thread = ChatThread.objects.filter(
            product=product,
            seller=seller
        ).first()

        if not thread:
            return HttpResponseForbidden("No buyer has initiated chat yet")

    # 🔐 Final permission check (VERY IMPORTANT)
    if request.user not in [thread.customer, thread.seller]:
        return HttpResponseForbidden("Unauthorized")

    # 💬 Handle message sending
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ChatMessage.objects.create(
                thread=thread,
                sender=request.user,
                message=message
            )
            return redirect("chat_view", product_id=product.id)

    messages = thread.messages.order_by("timestamp")

    return render(request, "chat.html", {
        "product": product,
        "thread": thread,
        "messages": messages
    })


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("all_products")

    return render(request, "signup.html", {"error": error})




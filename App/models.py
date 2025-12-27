import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
@deconstructible
class UniqueUploadPath:
    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f"{self.base_path}/{filename}"
class UserProduct(models.Model):

    CATEGORY_CHOICES = [
        ('Smartphones', 'Smartphones'),
        ('Camera', 'Camera'),
        ('Cars', 'Cars'),
        ('Tablets', 'Tablets'),
    ]

    DAMAGE_CHOICES = [
        ('damaged', 'Damaged'),
        ('undamaged', 'Undamaged'),
        ('undetected', 'Undetected'),
    ]

    # 🔐 Authenticated seller
    seller_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    # Seller info (display only)
    seller_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, default='+91')
    mobile = models.CharField(max_length=15)

    # Product info
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    price = models.IntegerField()
    condition = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    # 🖼️ Images (UNIQUE paths)
    original_image = models.ImageField(
        upload_to=UniqueUploadPath("user_products/original")
    )

    detected_image = models.ImageField(
        upload_to=UniqueUploadPath("user_products/detected"),
        blank=True,
        null=True
    )

    # 🤖 ML result
    detection_status = models.CharField(
        max_length=20,
        choices=DAMAGE_CHOICES,
        default='undetected'
    )

    # Demo flag
    is_demo = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} | ₹{self.price}"
class ChatThread(models.Model):
    product = models.ForeignKey(UserProduct, on_delete=models.CASCADE)

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_threads",
        null=True,
        blank=True
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller_threads",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.product.id}"
class ChatMessage(models.Model):
    thread = models.ForeignKey(
        ChatThread,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

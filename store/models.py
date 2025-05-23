from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Added back
    logo = models.ImageField(upload_to='brands/', blank=True)  # Added back
    
    def __str__(self):
        return self.name

class Phone(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='phones/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)  # Added back

    @property
    def total_price(self):
        return self.quantity * self.phone.price

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đang giao hàng'),
        ('completed', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy')
    ]
    
    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('banking', 'Chuyển khoản ngân hàng'),
        ('momo', 'Ví MoMo'),
        ('vnpay', 'VNPay'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    order_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']

    def __str__(self):
        return f'Đơn hàng #{self.id} - {self.full_name}'

    def send_status_notification(self):
        """Gửi thông báo khi cập nhật trạng thái đơn hàng"""
        status_messages = {
            'pending': 'đang chờ xử lý',
            'processing': 'đang được xử lý',
            'shipped': 'đang được giao',
            'completed': 'đã giao thành công',
            'cancelled': 'đã bị hủy'
        }
        message = f'Đơn hàng #{self.id} của bạn {status_messages.get(self.status)}'
        messages.info(self.user, message)

class Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
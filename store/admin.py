from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Brand, Phone, Cart, Order, OrderItem
from django.utils import timezone

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')
    list_select_related = ('profile',)

    def get_phone_number(self, instance):
        return instance.profile.phone_number if hasattr(instance, 'profile') else ''
    get_phone_number.short_description = 'Phone Number'

# Unregister the default UserAdmin and register our CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock', 'available')
    list_filter = ('brand', 'available')
    search_fields = ('name', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'quantity', 'total_price']
    list_filter = ['user']
    search_fields = ['user__username', 'phone__name']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('get_total',)  # Chỉ để get_total là readonly
    extra = 0
    can_delete = False

    def get_total(self, obj):
        if obj.price is None or obj.quantity is None:
            return format_html('<span>$0.00</span>')
        total = obj.price * obj.quantity
        return format_html('<span>${}</span>', '{:.2f}'.format(total))
    get_total.short_description = 'Tổng tiền'

@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'get_total', 'status', 'get_status_display', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    list_editable = ('status',)  # Cho phép sửa trạng thái trực tiếp từ danh sách
    search_fields = ('full_name', 'phone', 'address')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin khách hàng', {
            'fields': ('user', 'full_name', 'phone', 'address')
        }),
        ('Thông tin đơn hàng', {
            'fields': ('status', 'payment_method', 'total', 'order_note')
        }),
        ('Thông tin khác', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)  # Chỉ để created_at là readonly

    def get_total(self, obj):
        if obj.total is None:
            return format_html('<b>$0.00</b>')
        return format_html('<b>${}</b>', '{:.2f}'.format(obj.total))
    get_total.short_description = 'Tổng đơn hàng'

    def get_status_display(self, obj):
        status_colors = {
            'pending': '#FFA500',
            'processing': '#0000FF',
            'shipped': '#800080',
            'completed': '#008000',
            'cancelled': '#FF0000',
        }
        status_icons = {
            'pending': '⏳',
            'processing': '⚙️',
            'shipped': '🚚',
            'completed': '✅',
            'cancelled': '❌'
        }
        color = status_colors.get(obj.status, '#000000')
        icon = status_icons.get(obj.status, '')
        
        return format_html(
            '<span style="color: {}">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )
    get_status_display.short_description = 'Trạng thái'

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            from django.contrib.admin.models import LogEntry, CHANGE
            from django.contrib.contenttypes.models import ContentType
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj.id,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message=f'Đã thay đổi trạng thái sang {form.cleaned_data["status"]}'
            )
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
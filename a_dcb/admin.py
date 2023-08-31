from django.contrib import admin
from .models import Complaint, Departments
from django.core.mail import EmailMessage
from django.conf import settings

# Register your models here.
@admin.action(description="Mark selected record as completed")
def make_completed(modeladmin, request, queryset):
    ownerMail = []
    ownerMail.append(queryset[0].email)
    msg = EmailMessage(f'Complaint Completed', f'Complaint Completed', settings.EMAIL_HOST_USER, ownerMail)
    msg.content_subtype = "html"
    msg.send()
    queryset.update(complaint_status="completed")
    
@admin.action(description="Mark selected record as rejected")
def make_rejected(modeladmin, request, queryset):
    ownerMail = []
    ownerMail.append(queryset[0].email)
    msg = EmailMessage(f'Complaint Rejected', f'Complaint Rejected', settings.EMAIL_HOST_USER, ownerMail)
    msg.content_subtype = "html"
    msg.send()
    queryset.update(complaint_status="rejected")


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact", 'complaint', 'complaint_status', 'created_at')
    list_filter = ("complaint_status", "department", "created_at", )
    search_fields = ("name__startswith", 'email', 'contact',)
    actions = [make_completed, make_rejected]


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Departments)

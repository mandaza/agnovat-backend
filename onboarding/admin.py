from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import PersonalDetails, DocumentType, Document, OnboardingProgress


@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'suburb', 'state', 'is_complete', 'updated_at']
    list_filter = ['state', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number']
    readonly_fields = ['is_complete', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'phone_number')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'suburb', 'state', 'postcode')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Professional Information', {
            'fields': ('abn_number', 'tfn_number', 'bank_account_name', 'bank_bsb', 'bank_account_number')
        }),
        ('Status', {
            'fields': ('is_complete', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'is_required', 'has_expiry', 'max_file_size_mb']
    list_filter = ['is_required', 'has_expiry']
    search_fields = ['name', 'display_name']
    ordering = ['display_name']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'document_type', 'status', 'expiry_date', 
        'expiry_status', 'uploaded_at', 'reviewed_by'
    ]
    list_filter = [
        'status', 'document_type', 'uploaded_at', 
        'expiry_date', 'reviewed_at'
    ]
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'document_type__display_name', 'document_number', 'issuing_authority'
    ]
    readonly_fields = [
        'original_filename', 'file_size', 'uploaded_at', 'updated_at',
        'is_expired', 'is_expiring_soon', 'days_until_expiry'
    ]
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('user', 'document_type', 'file', 'original_filename', 'file_size')
        }),
        ('Document Details', {
            'fields': ('issue_date', 'expiry_date', 'document_number', 'issuing_authority')
        }),
        ('Review Status', {
            'fields': ('status', 'notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Expiry Information', {
            'fields': ('is_expired', 'is_expiring_soon', 'days_until_expiry'),
            'classes': ('collapse',)
        })
    )
    
    def expiry_status(self, obj):
        if not obj.expiry_date:
            return format_html('<span style="color: gray;">No expiry</span>')
        
        if obj.is_expired:
            return format_html('<span style="color: red; font-weight: bold;">EXPIRED</span>')
        elif obj.is_expiring_soon:
            days = obj.days_until_expiry
            return format_html(
                '<span style="color: orange; font-weight: bold;">Expires in {} days</span>',
                days
            )
        else:
            days = obj.days_until_expiry
            return format_html('<span style="color: green;">Valid ({} days)</span>', days)
    
    expiry_status.short_description = 'Expiry Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'document_type', 'reviewed_by'
        )
    
    actions = ['approve_documents', 'reject_documents']
    
    def approve_documents(self, request, queryset):
        count = 0
        for document in queryset:
            if document.status == 'pending':
                document.status = 'approved'
                document.reviewed_by = request.user
                document.reviewed_at = timezone.now()
                document.save()
                count += 1
        
        self.message_user(request, f'{count} documents approved successfully.')
    approve_documents.short_description = "Approve selected documents"
    
    def reject_documents(self, request, queryset):
        count = 0
        for document in queryset:
            if document.status == 'pending':
                document.status = 'rejected'
                document.reviewed_by = request.user
                document.reviewed_at = timezone.now()
                document.save()
                count += 1
        
        self.message_user(request, f'{count} documents rejected successfully.')
    reject_documents.short_description = "Reject selected documents"


@admin.register(OnboardingProgress)
class OnboardingProgressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'current_stage', 'completion_percentage', 
        'completed_at', 'updated_at'
    ]
    list_filter = ['current_stage', 'completed_at', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = [
        'completion_percentage', 'personal_details_completed_at',
        'documents_uploaded_at', 'admin_approved_at', 'completed_at',
        'created_at', 'updated_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'current_stage', 'completion_percentage')
        }),
        ('Progress Milestones', {
            'fields': (
                'personal_details_completed_at', 'documents_uploaded_at',
                'admin_approved_at', 'completed_at'
            )
        }),
        ('Admin Notes', {
            'fields': ('admin_notes', 'rejected_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    actions = ['recalculate_progress', 'complete_onboarding']
    
    def recalculate_progress(self, request, queryset):
        count = 0
        for progress in queryset:
            progress.update_stage()
            progress.calculate_completion_percentage()
            progress.save()
            count += 1
        
        self.message_user(request, f'{count} progress records recalculated successfully.')
    recalculate_progress.short_description = "Recalculate progress for selected users"
    
    def complete_onboarding(self, request, queryset):
        count = 0
        for progress in queryset:
            if progress.current_stage != 'completed':
                progress.current_stage = 'completed'
                progress.completed_at = timezone.now()
                progress.completion_percentage = 100
                progress.save()
                count += 1
        
        self.message_user(request, f'{count} onboarding processes marked as completed.')
    complete_onboarding.short_description = "Mark selected onboarding as completed"


# Customize admin site
admin.site.site_header = "Agnovat Support Worker Management"
admin.site.site_title = "Agnovat Admin"
admin.site.index_title = "Welcome to Agnovat Administration"
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from datetime import date, timedelta

User = get_user_model()


class PersonalDetails(models.Model):
    """Extended personal details for support workers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_details')
    
    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        null=True,
        blank=True
    )
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    suburb = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        null=True,
        blank=True
    )
    emergency_contact_relationship = models.CharField(max_length=100, null=True, blank=True)
    
    # Professional Information
    abn_number = models.CharField(max_length=20, null=True, blank=True, help_text="Australian Business Number")
    tfn_number = models.CharField(max_length=20, null=True, blank=True, help_text="Tax File Number")
    bank_account_name = models.CharField(max_length=255, null=True, blank=True)
    bank_bsb = models.CharField(max_length=10, null=True, blank=True)
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Personal Details - {self.user.get_full_name() or self.user.username}"
    
    @property
    def is_complete(self):
        """Check if all required personal details are provided"""
        required_fields = [
            self.date_of_birth, self.phone_number, self.address_line1,
            self.suburb, self.state, self.postcode, self.emergency_contact_name,
            self.emergency_contact_phone
        ]
        return all(field for field in required_fields)


class DocumentType(models.Model):
    """Types of documents required for onboarding"""
    DOCUMENT_TYPES = [
        ('yellow_card', 'Yellow Card (Disability Worker Screening)'),
        ('police_check', 'National Police Check'),
        ('ndis_orientation', 'NDIS Orientation Certificate'),
        ('first_aid', 'First Aid Certificate'),
        ('cpr_certificate', 'CPR Certificate'),
        ('public_liability', 'Public Liability Insurance'),
        ('professional_indemnity', 'Professional Indemnity Insurance'),
        ('car_insurance', 'Car Insurance'),
        ('drivers_licence_front', 'Driver\'s Licence (Front)'),
        ('drivers_licence_back', 'Driver\'s Licence (Back)'),
        ('car_registration', 'Car Registration'),
        ('right_to_work', 'Right to Work Check'),
        ('service_agreement', 'Signed Service Agreement'),
    ]
    
    name = models.CharField(max_length=50, choices=DOCUMENT_TYPES, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_required = models.BooleanField(default=True)
    has_expiry = models.BooleanField(default=True)
    max_file_size_mb = models.IntegerField(default=5)  # Maximum file size in MB
    allowed_extensions = models.CharField(
        max_length=255,
        default='pdf,jpg,jpeg,png',
        help_text="Comma-separated list of allowed file extensions"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        ordering = ['display_name']


class Document(models.Model):
    """Uploaded documents for compliance"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('expiring_soon', 'Expiring Soon'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    
    # File Information
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    
    # Document Details
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    document_number = models.CharField(max_length=100, null=True, blank=True)
    issuing_authority = models.CharField(max_length=255, null=True, blank=True)
    
    # Status and Review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(null=True, blank=True, help_text="Admin notes or rejection reasons")
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_documents'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.document_type.display_name} - {self.user.get_full_name() or self.user.username}"
    
    @property
    def is_expired(self):
        """Check if document is expired"""
        if not self.expiry_date:
            return False
        return self.expiry_date < date.today()
    
    @property
    def is_expiring_soon(self):
        """Check if document expires within 30 days"""
        if not self.expiry_date:
            return False
        return self.expiry_date <= date.today() + timedelta(days=30)
    
    @property
    def days_until_expiry(self):
        """Calculate days until expiry"""
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days
    
    def save(self, *args, **kwargs):
        # Auto-update status based on expiry
        if self.expiry_date:
            if self.is_expired:
                self.status = 'expired'
            elif self.is_expiring_soon and self.status == 'approved':
                self.status = 'expiring_soon'
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ['user', 'document_type']  # One document per type per user


class OnboardingProgress(models.Model):
    """Track overall onboarding progress for each user"""
    PROGRESS_STAGES = [
        ('not_started', 'Not Started'),
        ('personal_details', 'Personal Details'),
        ('documents_upload', 'Documents Upload'),
        ('admin_review', 'Admin Review'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding_progress')
    current_stage = models.CharField(max_length=20, choices=PROGRESS_STAGES, default='not_started')
    completion_percentage = models.IntegerField(default=0)
    
    # Milestone Timestamps
    personal_details_completed_at = models.DateTimeField(null=True, blank=True)
    documents_uploaded_at = models.DateTimeField(null=True, blank=True)
    admin_approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Admin Notes
    admin_notes = models.TextField(null=True, blank=True)
    rejected_reason = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Onboarding Progress - {self.user.get_full_name() or self.user.username} ({self.get_current_stage_display()})"
    
    def calculate_completion_percentage(self):
        """Calculate completion percentage based on progress"""
        total_steps = 0
        completed_steps = 0
        
        # Personal details (25%)
        total_steps += 1
        if hasattr(self.user, 'personal_details') and self.user.personal_details.is_complete:
            completed_steps += 1
        
        # Required documents (50%)
        required_doc_types = DocumentType.objects.filter(is_required=True)
        total_steps += len(required_doc_types)
        approved_docs = self.user.documents.filter(
            document_type__in=required_doc_types,
            status='approved'
        ).count()
        completed_steps += approved_docs
        
        # Admin approval (25%)
        total_steps += 1
        if self.current_stage == 'completed':
            completed_steps += 1
        
        if total_steps > 0:
            self.completion_percentage = int((completed_steps / total_steps) * 100)
        else:
            self.completion_percentage = 0
        
        return self.completion_percentage
    
    def update_stage(self):
        """Auto-update current stage based on progress"""
        if not hasattr(self.user, 'personal_details') or not self.user.personal_details.is_complete:
            self.current_stage = 'personal_details'
        elif self.user.documents.filter(document_type__is_required=True).count() == 0:
            self.current_stage = 'documents_upload'
        elif self.user.documents.filter(document_type__is_required=True, status='pending').exists():
            self.current_stage = 'admin_review'
        elif self.user.documents.filter(document_type__is_required=True, status='rejected').exists():
            self.current_stage = 'rejected'
        else:
            required_docs = DocumentType.objects.filter(is_required=True).count()
            approved_docs = self.user.documents.filter(
                document_type__is_required=True,
                status='approved'
            ).count()
            
            if approved_docs >= required_docs:
                self.current_stage = 'completed'
                if not self.completed_at:
                    from django.utils import timezone
                    self.completed_at = timezone.now()
    
    class Meta:
        verbose_name_plural = "Onboarding Progress"
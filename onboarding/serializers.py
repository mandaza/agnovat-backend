from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PersonalDetails, Document, DocumentType, OnboardingProgress

User = get_user_model()


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = [
            'id', 'date_of_birth', 'phone_number', 'address_line1', 'address_line2',
            'suburb', 'state', 'postcode', 'emergency_contact_name', 
            'emergency_contact_phone', 'emergency_contact_relationship',
            'abn_number', 'tfn_number', 'bank_account_name', 'bank_bsb',
            'bank_account_number', 'is_complete', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_complete', 'created_at', 'updated_at']
    
    def validate_date_of_birth(self, value):
        from datetime import date
        if value and value >= date.today():
            raise serializers.ValidationError("Date of birth must be in the past.")
        return value


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = [
            'id', 'name', 'display_name', 'description', 'is_required',
            'has_expiry', 'max_file_size_mb', 'allowed_extensions'
        ]


class DocumentSerializer(serializers.ModelSerializer):
    document_type_name = serializers.CharField(source='document_type.display_name', read_only=True)
    file_url = serializers.SerializerMethodField()
    days_until_expiry = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    is_expiring_soon = serializers.ReadOnlyField()
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'document_type', 'document_type_name', 'file', 'file_url',
            'original_filename', 'file_size', 'issue_date', 'expiry_date',
            'document_number', 'issuing_authority', 'status', 'notes',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at', 'uploaded_at',
            'updated_at', 'days_until_expiry', 'is_expired', 'is_expiring_soon'
        ]
        read_only_fields = [
            'id', 'file_size', 'status', 'notes', 'reviewed_by', 
            'reviewed_at', 'uploaded_at', 'updated_at'
        ]
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def validate_file(self, value):
        # Get document type from context or validated data
        document_type_id = self.initial_data.get('document_type')
        if document_type_id:
            try:
                doc_type = DocumentType.objects.get(id=document_type_id)
                
                # Check file size
                if value.size > doc_type.max_file_size_mb * 1024 * 1024:
                    raise serializers.ValidationError(
                        f"File size cannot exceed {doc_type.max_file_size_mb}MB."
                    )
                
                # Check file extension
                import os
                ext = os.path.splitext(value.name)[1][1:].lower()
                allowed_exts = [e.strip().lower() for e in doc_type.allowed_extensions.split(',')]
                if ext not in allowed_exts:
                    raise serializers.ValidationError(
                        f"File type '{ext}' not allowed. Allowed types: {', '.join(allowed_exts)}"
                    )
                
            except DocumentType.DoesNotExist:
                pass
        
        return value
    
    def create(self, validated_data):
        # Set user from request
        validated_data['user'] = self.context['request'].user
        
        # Set file metadata
        file = validated_data['file']
        validated_data['original_filename'] = file.name
        validated_data['file_size'] = file.size
        
        return super().create(validated_data)


class DocumentUploadSerializer(serializers.Serializer):
    """Simplified serializer for document upload"""
    document_type = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all())
    file = serializers.FileField()
    issue_date = serializers.DateField(required=False, allow_null=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    document_number = serializers.CharField(required=False, allow_blank=True, max_length=100)
    issuing_authority = serializers.CharField(required=False, allow_blank=True, max_length=255)
    
    def validate_file(self, value):
        # Basic file validation
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        # Check file extension
        import os
        ext = os.path.splitext(value.name)[1][1:].lower()
        allowed_exts = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
        if ext not in allowed_exts:
            raise serializers.ValidationError(
                f"File type '{ext}' not allowed. Allowed types: {', '.join(allowed_exts)}"
            )
        
        return value


class OnboardingProgressSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = OnboardingProgress
        fields = [
            'id', 'user', 'user_name', 'user_email', 'current_stage',
            'completion_percentage', 'personal_details_completed_at',
            'documents_uploaded_at', 'admin_approved_at', 'completed_at',
            'admin_notes', 'rejected_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'completion_percentage', 'personal_details_completed_at',
            'documents_uploaded_at', 'admin_approved_at', 'completed_at',
            'created_at', 'updated_at'
        ]


class DocumentReviewSerializer(serializers.ModelSerializer):
    """Serializer for admin document review"""
    class Meta:
        model = Document
        fields = ['status', 'notes']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Status must be 'approved' or 'rejected'.")
        return value


class OnboardingDashboardSerializer(serializers.Serializer):
    """Serializer for onboarding dashboard data"""
    personal_details = PersonalDetailsSerializer(read_only=True)
    progress = OnboardingProgressSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    required_document_types = DocumentTypeSerializer(many=True, read_only=True)
    missing_documents = serializers.ListField(child=serializers.CharField(), read_only=True)
    
    def to_representation(self, instance):
        # instance is the user
        data = {}
        
        # Personal details
        try:
            data['personal_details'] = PersonalDetailsSerializer(
                instance.personal_details, context=self.context
            ).data
        except PersonalDetails.DoesNotExist:
            data['personal_details'] = None
        
        # Progress
        try:
            data['progress'] = OnboardingProgressSerializer(
                instance.onboarding_progress, context=self.context
            ).data
        except OnboardingProgress.DoesNotExist:
            data['progress'] = None
        
        # Documents
        data['documents'] = DocumentSerializer(
            instance.documents.all(), many=True, context=self.context
        ).data
        
        # Required document types
        data['required_document_types'] = DocumentTypeSerializer(
            DocumentType.objects.filter(is_required=True), many=True
        ).data
        
        # Missing documents
        uploaded_types = instance.documents.values_list('document_type__name', flat=True)
        required_types = DocumentType.objects.filter(is_required=True).values_list('name', flat=True)
        data['missing_documents'] = list(set(required_types) - set(uploaded_types))
        
        return data

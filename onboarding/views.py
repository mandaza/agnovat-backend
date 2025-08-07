from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import PersonalDetails, Document, DocumentType, OnboardingProgress
from .serializers import (
    PersonalDetailsSerializer, DocumentSerializer, DocumentTypeSerializer,
    OnboardingProgressSerializer, DocumentReviewSerializer, 
    DocumentUploadSerializer, OnboardingDashboardSerializer
)

User = get_user_model()


class PersonalDetailsView(generics.RetrieveUpdateAPIView):
    """Get or update personal details for the authenticated user"""
    serializer_class = PersonalDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        personal_details, created = PersonalDetails.objects.get_or_create(
            user=self.request.user
        )
        return personal_details
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
        # Update onboarding progress
        progress, created = OnboardingProgress.objects.get_or_create(
            user=self.request.user
        )
        if serializer.instance.is_complete and not progress.personal_details_completed_at:
            progress.personal_details_completed_at = timezone.now()
        
        progress.update_stage()
        progress.calculate_completion_percentage()
        progress.save()


class DocumentTypeListView(generics.ListAPIView):
    """List all document types"""
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentListCreateView(generics.ListCreateAPIView):
    """List user's documents or upload a new document"""
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Check if document of this type already exists
        doc_type = serializer.validated_data['document_type']
        existing_doc = Document.objects.filter(
            user=self.request.user,
            document_type=doc_type
        ).first()
        
        if existing_doc:
            # Delete the old document file
            if existing_doc.file:
                existing_doc.file.delete()
            existing_doc.delete()
        
        # Save new document
        serializer.save(user=self.request.user)
        
        # Update onboarding progress
        progress, created = OnboardingProgress.objects.get_or_create(
            user=self.request.user
        )
        progress.update_stage()
        progress.calculate_completion_percentage()
        progress.save()


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific document"""
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        # Delete the file
        if instance.file:
            instance.file.delete()
        instance.delete()


@swagger_auto_schema(
    method='post',
    request_body=DocumentUploadSerializer,
    responses={201: DocumentSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_document(request):
    """Upload a document with simplified payload"""
    serializer = DocumentUploadSerializer(data=request.data)
    
    if serializer.is_valid():
        # Check if document of this type already exists
        doc_type = serializer.validated_data['document_type']
        existing_doc = Document.objects.filter(
            user=request.user,
            document_type=doc_type
        ).first()
        
        if existing_doc:
            # Delete the old document
            if existing_doc.file:
                existing_doc.file.delete()
            existing_doc.delete()
        
        # Create new document
        file = serializer.validated_data['file']
        document = Document.objects.create(
            user=request.user,
            document_type=doc_type,
            file=file,
            original_filename=file.name,
            file_size=file.size,
            issue_date=serializer.validated_data.get('issue_date'),
            expiry_date=serializer.validated_data.get('expiry_date'),
            document_number=serializer.validated_data.get('document_number'),
            issuing_authority=serializer.validated_data.get('issuing_authority'),
        )
        
        # Update onboarding progress
        progress, created = OnboardingProgress.objects.get_or_create(user=request.user)
        progress.update_stage()
        progress.calculate_completion_percentage()
        progress.save()
        
        return Response(
            DocumentSerializer(document, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnboardingProgressView(generics.RetrieveAPIView):
    """Get onboarding progress for authenticated user"""
    serializer_class = OnboardingProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        progress, created = OnboardingProgress.objects.get_or_create(
            user=self.request.user
        )
        progress.update_stage()
        progress.calculate_completion_percentage()
        progress.save()
        return progress


@swagger_auto_schema(
    method='get',
    responses={200: OnboardingDashboardSerializer}
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def onboarding_dashboard(request):
    """Get complete onboarding dashboard data for authenticated user"""
    serializer = OnboardingDashboardSerializer(
        request.user, 
        context={'request': request}
    )
    return Response(serializer.data)


# Admin Views
class AdminOnboardingListView(generics.ListAPIView):
    """List all users' onboarding progress (Admin/Coordinator only)"""
    serializer_class = OnboardingProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role not in ['admin', 'coordinator']:
            return OnboardingProgress.objects.none()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        queryset = OnboardingProgress.objects.all()
        
        if status_filter:
            queryset = queryset.filter(current_stage=status_filter)
        
        return queryset.order_by('-updated_at')


class AdminDocumentReviewView(generics.UpdateAPIView):
    """Admin view to approve/reject documents"""
    serializer_class = DocumentReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Document.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        if user.role not in ['admin', 'coordinator']:
            return Document.objects.none()
        return Document.objects.all()
    
    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user,
            reviewed_at=timezone.now()
        )
        
        # Update user's onboarding progress
        document = serializer.instance
        progress, created = OnboardingProgress.objects.get_or_create(
            user=document.user
        )
        progress.update_stage()
        progress.calculate_completion_percentage()
        progress.save()


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('Pending documents', DocumentSerializer(many=True))}
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_documents(request):
    """Get all pending documents for admin review"""
    user = request.user
    if user.role not in ['admin', 'coordinator']:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    documents = Document.objects.filter(status='pending').order_by('-uploaded_at')
    serializer = DocumentSerializer(documents, many=True, context={'request': request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('Expiring documents', DocumentSerializer(many=True))}
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def expiring_documents(request):
    """Get documents that are expiring soon or expired"""
    user = request.user
    if user.role not in ['admin', 'coordinator']:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    from datetime import date, timedelta
    expiry_threshold = date.today() + timedelta(days=30)
    
    documents = Document.objects.filter(
        expiry_date__lte=expiry_threshold,
        status='approved'
    ).order_by('expiry_date')
    
    serializer = DocumentSerializer(documents, many=True, context={'request': request})
    return Response(serializer.data)


class UserOnboardingDetailView(generics.RetrieveAPIView):
    """Admin view to see specific user's onboarding details"""
    serializer_class = OnboardingDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if user.role not in ['admin', 'coordinator']:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Permission denied")
        
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)
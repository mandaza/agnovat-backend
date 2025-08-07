from django.urls import path
from . import views

urlpatterns = [
    # User onboarding endpoints
    path('personal-details/', views.PersonalDetailsView.as_view(), name='personal-details'),
    path('dashboard/', views.onboarding_dashboard, name='onboarding-dashboard'),
    path('progress/', views.OnboardingProgressView.as_view(), name='onboarding-progress'),
    
    # Document management
    path('document-types/', views.DocumentTypeListView.as_view(), name='document-types'),
    path('documents/', views.DocumentListCreateView.as_view(), name='documents'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('upload/', views.upload_document, name='upload-document'),
    
    # Admin endpoints
    path('admin/onboarding/', views.AdminOnboardingListView.as_view(), name='admin-onboarding-list'),
    path('admin/documents/<int:pk>/review/', views.AdminDocumentReviewView.as_view(), name='admin-document-review'),
    path('admin/documents/pending/', views.pending_documents, name='pending-documents'),
    path('admin/documents/expiring/', views.expiring_documents, name='expiring-documents'),
    path('admin/users/<int:user_id>/onboarding/', views.UserOnboardingDetailView.as_view(), name='user-onboarding-detail'),
]

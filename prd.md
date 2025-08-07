Absolutely! Here's your **Product Requirements Document (PRD)** for the full **Tavonga Support Worker Management System**, following your provided structure and incorporating all features including user roles (support worker, admin, coordinator, behaviour practitioner), onboarding, scheduling, incident reporting, and more.

---

# **Agnovat Support Worker Management System**

## **Project Overview**

This project will develop a secure, web-based application to manage the onboarding, scheduling, compliance, incident reporting, shift notes, and behavior analysis for support workers involved in the care of Agnovat, a young individual with autism and intellectual disability. The system will support different user roles—Admin, Coordinator, Support Worker, and Behaviour Practitioner—and enable real-time coordination of services, data-driven care decisions, and regulatory compliance with NDIS standards in Australia.

## **Level**

Advanced

## **Type of Project**

Web Application, Compliance Management, Behavioural Support System, Role-Based Dashboard

## **Skills Required**

* Django REST Framework (Backend API)
* React + TypeScript (Frontend UI)
* PostgreSQL (Database)
* AWS S3 or Cloudinary (Document & Media Storage)
* JWT Authentication & Role-based Access Control
* Data Visualization (Charts for Behavior Analysis)
* PDF Generation & File Uploads
* Security & Compliance (NDIS, GDPR)

---

## **Key Features**

### **Milestone 1: Authentication & Role Management**

* User Registration & Login
* JWT-based secure authentication
* Four User Roles:

  * **Admin**: Full system control and access
  * **Support Worker**: Logs shifts, uploads documents, reports incidents
  * **Coordinator**: Oversees onboarding, shift approvals, incident reviews
  * **Behaviour Practitioner**: Reviews behavioral data and generates insights
* Role-based access control to different modules
* Password reset via email

---

### **Milestone 2: Onboarding & Compliance Document Management**

* Personal details form (Name, DOB, Contact info)
* Uploads for required documents:

  * Yellow Card (Disability Worker Screening)
  * National Police Check
  * NDIS Orientation Certificate
  * First Aid & CPR Certificate
  * Insurance Documents (Public Liability, Professional Indemnity, Car)
  * Driver's Licence (Front/Back)
  * Car Registration
  * Right to Work Check
  * Signed Service Agreement
* Expiry date tracking & admin alerts
* Admin can review, approve, or request updates
* Document status dashboard with progress indicators

---

### **Milestone 3: Conflict of Interest Declaration**

* Structured form to declare:

  * **Personal**: Any relation to Agnovat or family
  * **Financial**: Gifts, incentives, or dual compensation
  * **Business**: Involvement in related service businesses
* Required during onboarding
* Editable and auditable by Admin or Coordinator

---

### **Milestone 4: Service Agreement Management**

* Digital Service Agreement Form:

  * Nature of service
  * Weekly hours/days (e.g. Tuesday 8am–4pm)
  * Start and end date of the service period
  * Total hours and estimated cost
  * Additional capped charges (e.g., travel)
* PDF export of agreements
* Expiry tracking & notifications

---

### **Milestone 5: Shift Scheduling & Availability**

* Calendar-based shift planning (Admin/Coordinator)
* Worker availability input
* Assign shifts with:

  * Start/end times
  * Activity type
  * Location
* Worker receives notification for assigned shifts
* View past and upcoming shifts

---

### **Milestone 6: Shift Notes Submission**

* Each completed shift must include:

  * Summary of tasks completed
  * Concerns, observations, or incidents
  * Link to incident form (if needed)
* Must be submitted within 24 hours
* Admin/coordinator can review and leave notes
* Auto-reminders for missing notes

---

### **Milestone 7: Incident Report Module**

* Mandatory detailed form for any behavioural incident:

  1. Date of Incident
  2. Staff Involved
  3. Location (home, community, car, etc.)
  4. Activity before behavior
  5. Behavior types (e.g., aggression, self-harm, running into road, public masturbation)
  6. Warning signs (yes/no)
  7. Duration (0–30+ min)
  8. Intensity (low, medium, high)
  9. Harm to self or others
  10. Initial intervention used
  11. Free-text description
  12. Was 2:1 support required?
* Behaviour Practitioner and Admin have access to full reports
* Optional media upload (photos or video)

---

### **Milestone 8: Behaviour Analytics Dashboard (Practitioner/Admin)**

* Visual dashboards showing:

  * Daily behavior timelines
  * Monthly and yearly summaries
  * Most frequent behaviors
  * Common triggers
  * Recommended interventions
* Exportable reports (PDF, CSV)
* Filter by behavior type, intensity, duration, etc.

---

## **Client Profile**

Primary users include carers (support workers) who provide in-home and community-based support to Agnovat. Coordinators oversee rostering and service quality, while Behaviour Practitioners analyze incidents and trends to optimize interventions. Admins maintain control over onboarding, compliance, and overall system management.

---

## **Design Principles**

* **Clean, Intuitive UI**: Focus on clarity and minimalism for efficient use by support staff
* **Accessibility Focus**: High contrast, large click targets, readable type
* **Modular Dashboards**: Each role sees only relevant data
* **Compliance-Aware**: Designed for NDIS and Australian privacy law standards
* **Offline-Friendly**: Future-proofed for mobile/offline sync

---

## **Deliverables**

* ✅ Django REST API with PostgreSQL
* ✅ React-based Web Interface
* ✅ Admin Dashboard
* ✅ Media/document storage (S3/Cloudinary)
* ✅ Authentication system with RBAC
* ✅ Secure deployment-ready backend (Docker-ready)
* ✅ Exportable reports and documents
* ✅ Email notification system for compliance and alerts

---

Would you like this exported as a **PDF, Word document**, or pushed into a **ClickUp/Notion plan**?
Also, I can generate:

* A **developer milestone checklist**
* **API endpoint documentation**
* Or a **UI design system spec**

Let me know!

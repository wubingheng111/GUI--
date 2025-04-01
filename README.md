# Hospital Management System
## Project Overview
This is a comprehensive hospital management system developed using Streamlit. It aims to provide a complete solution for hospital information management, including patient registration, doctor diagnosis, and pharmacy services. The system features a modern interface design that delivers an intuitive user experience.
![image](https://github.com/user-attachments/assets/fc09b19c-8662-49eb-8fae-e226a7cb6c17)

## Key Features
The system is divided into three main modules:

### 1. Patient Registration & Appointment
New Patient Registration: Record patient's basic information including name, gender, age, ID number, contact number, home address, etc.
Department Assignment: Choose appropriate department and doctor based on patient condition
Priority Classification: Support three appointment priority levels - normal, priority, and emergency
Quick Registration for Existing Patients: Quickly find patients by ID or identity card number
Registration Statistics: Display daily registration status by department

### 2. Doctor Diagnosis & Prescription
Patient Search: Doctors can find patients by ID or name
Waiting List: Display patients waiting for diagnosis, sorted by priority
Diagnosis Records: Document vital signs, symptom description, diagnosis results, and treatment plans
Prescription Writing: Support adding multiple medications with specified dosage and duration
Follow-up Planning: Set follow-up appointment dates
#### 3. Pharmacy & Billing
Prescription Search: Find prescriptions by prescription ID, patient ID, or patient name
Medication Management: Track the status of each medication (pending, in preparation, prepared)
Cost Calculation: Automatically calculate the total cost of prescriptions
Data Management
The system uses JSON files to store data:

***patients.json***: Stores patient information
***doctors.json: Stores*** doctor information
***prescriptions.json***: Stores prescription information
The system automatically initializes these data files on startup and provides complete data read/write functionality.

Interface Features
Card-based layout for clear information display
Color coding to distinguish different priorities and statuses
Responsive design that adapts to different screen sizes
Real-time message notifications (success/error)
Sidebar navigation for easy module switching
System Requirements
Python 3.7+
Dependencies: streamlit, pandas
Operating System: Cross-platform support (Windows, MacOS, Linux)
Getting Started
***streamlit run GUI.py***
The system will automatically open in your default browser, with the default access address http://localhost:8501

# Workflow
Select the desired functional module in the sidebar
Follow the interface prompts to perform operations
The system will save data in real-time and provide feedback
# Notes
This is a demonstration version; actual deployment should consider data security and user authentication
The current version uses local JSON files for data storage; a production environment should use a database
© 2025 Hospital Management System

st.markdown

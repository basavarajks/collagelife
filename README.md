# 🎓 Student Data Management System (SDMS)

A comprehensive **Student Data Management System (SDMS)** built using **Django REST Framework** for the backend and **Flutter** for the frontend. The system streamlines college administration by providing role-based access for administrators, faculty, students, and other departments.

---

## ⚡ Phase 1 Add-on (React + Flask Foundation)

This repository now also contains a **separate Phase 1 implementation** for a public college website + login/auth foundation:

- React app: `/home/runner/work/collagelife/collagelife/frontend-react`
- Flask app: `/home/runner/work/collagelife/collagelife/backend-flask`

Existing Flutter (`frontend/`) and Django (`backend/`) code is kept intact.

### Reused demo assets (copied from Flutter app)

Source assets:

- `/home/runner/work/collagelife/collagelife/frontend/assets/images/carousel1.jpg`
- `/home/runner/work/collagelife/collagelife/frontend/assets/images/carousel2.jpg`
- `/home/runner/work/collagelife/collagelife/frontend/assets/images/carousel3.jpg`
- `/home/runner/work/collagelife/collagelife/frontend/assets/images/logo.png`

Copied to:

- `/home/runner/work/collagelife/collagelife/frontend-react/src/assets/images/`

All college details/statistics/contact/notices are placeholders in this phase and must be updated with verified information.

### Phase 1 frontend features

- Responsive homepage sections: header/nav, hero, about/stats, principal message placeholder, departments, activities, gallery, notices, footer
- Shared login route (`/login`) from header and hero CTA
- Forgot-password placeholder route (`/forgot-password`) with not-configured message
- Accessible mobile menu, password show/hide button, image fallbacks, validation/loading/error states
- Protected route foundation (`/portal`) with backend-provided authenticated role usage
- Configurable content from central file: `frontend-react/src/config/collegeData.js`
- API base URL from env: `frontend-react/.env` (`VITE_API_BASE_URL`)

### Phase 1 backend features

- Flask application factory + Blueprints
- SQLAlchemy models (`User`, `Role`) with hashed passwords, active flag, timestamps
- Flask-Migrate setup with initial migration in `backend-flask/migrations/`
- CORS restricted by `FRONTEND_ORIGIN`
- Auth endpoints:
  - `POST /api/v1/auth/login`
  - `POST /api/v1/auth/forgot-password` (returns not configured)
- API endpoints:
  - `GET /api/v1/api/health`
  - `GET /api/v1/api/protected`
  - `GET /api/v1/api/principal-only`
- Secure local admin seed command (no default admin credentials):
  - `flask --app run.py seed-admin`

### Windows 11 + XAMPP + phpMyAdmin setup (Phase 1 Flask + React)

1. Start database service from XAMPP:
   - Open **XAMPP Control Panel**
   - Start **MySQL** (MariaDB)
2. Open phpMyAdmin:
   - `http://localhost/phpmyadmin`
3. Create/select database:
   - Create DB named `sdms_db` (or your preferred name)
4. Backend setup in PowerShell:
   ```powershell
   cd C:\path\to\collagelife\backend-flask
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   copy .env.example .env
   ```
5. Edit `.env` and set database connection:
   - Recommended:
     - `DATABASE_URL=mysql+pymysql://<username>:<password>@127.0.0.1:3306/sdms_db`
   - Also set:
     - `FRONTEND_ORIGIN=http://localhost:5173`
     - `SECRET_KEY=<strong-random-value>`
6. Run migrations:
   ```powershell
   flask --app run.py db upgrade
   ```
   If you start without existing migration state:
   ```powershell
   flask --app run.py db init
   flask --app run.py db migrate -m "create auth tables"
   flask --app run.py db upgrade
   ```
7. (Optional local admin) Create one secure admin user:
   ```powershell
   flask --app run.py seed-admin
   ```
8. Start Flask backend:
   ```powershell
   flask --app run.py run
   ```
9. Frontend setup in another terminal:
   ```powershell
   cd C:\path\to\collagelife\frontend-react
   npm install
   copy .env.example .env
   ```
10. Set `frontend-react/.env`:
    - `VITE_API_BASE_URL=http://127.0.0.1:5000/api/v1`
11. Start React:
    ```powershell
    npm run dev
    ```

### Phase 1 limitations

- No role dashboards are implemented yet (Admin/Principal, HOD, Faculty, Student, Office Staff, Library Staff).
- Forgot-password delivery is intentionally not configured in this phase.
- Placeholder content is used for institution identity, principal details, statistics, notices, and contacts until verified data is provided.

---

## 📌 Features

### 👨‍🎓 Student Management
- Student registration and profile management
- Admission ID generation
- Student academic history
- Document management
- Photo and signature upload

### 👨‍🏫 Faculty Management
- Faculty profile management
- Subject allocation
- Attendance management
- Internal Assessment (IA) marks entry

### 🏫 Academic Management
- Departments
- Courses
- Semesters
- Subjects
- Timetable management
- Academic year management

### 📊 Attendance System
- Daily attendance tracking
- Attendance reports
- Student attendance history

### 📝 Internal Assessment
- IA Test creation
- Marks entry
- Marks analysis
- Student performance reports

### 📚 Library Management
- Book management
- Book issue & return
- Fine calculation
- E-Book support

### 💰 Fee Management
- Fee structure management
- Student fee assignment
- Online payment records
- Receipt generation

### 📄 Document Management
- Student documents
- Faculty documents
- Secure file uploads

### 🎓 External Results
- External examination result management
- Semester-wise results

### 📢 Grievance System
- Raise grievances
- Track grievance status
- Department-wise grievance handling

### 🔐 Authentication & Security
- JWT Authentication
- Role-Based Access Control (RBAC)
- Password encryption
- Secure REST APIs

---

# 👥 User Roles

- Administrator
- Principal
- Head of Department (HOD)
- Faculty
- Student
- Library Staff
- Fee Department
- Examination Department

---

# 🛠 Tech Stack

## Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Frontend

- Flutter
- Dart

## Database

- PostgreSQL

## Tools

- Git
- GitHub
- Postman
- VS Code

---

# 📂 Project Structure

```
SDMS/
│
├── backend/
│   ├── academics/
│   ├── attendance/
│   ├── students/
│   ├── faculty/
│   ├── fees/
│   ├── library/
│   ├── grievances/
│   ├── subjects/
│   ├── timetable/
│   ├── userlogin/
│   ├── SDMS/
│   └── manage.py
│
├── frontend/
│   ├── lib/
│   ├── assets/
│   ├── web/
│   └── pubspec.yaml
│
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/SDMS.git

cd SDMS
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure PostgreSQL database in `settings.py`.

Run migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

Start the backend

```bash
python manage.py runserver
```

Backend URL

```
http://127.0.0.1:8000/
```

---

## Frontend Setup

```bash
cd frontend

flutter pub get
```

Run

```bash
flutter run
```

---

# 🔐 Authentication

The system uses:

- JWT Authentication
- Role Based Authorization
- Secure API endpoints

---

# 📦 Major Modules

- Authentication
- Student Management
- Faculty Management
- Attendance
- Internal Assessment
- Fee Management
- Library
- Timetable
- Subject Management
- Academic Management
- Grievance Management
- External Results
- Document Management

---

# 🌟 Future Enhancements

- AI-based Student Performance Prediction
- Face Recognition Attendance
- Parent Portal
- Online Fee Payment Gateway
- Notification System
- Mobile Push Notifications
- Dashboard Analytics
- AI Chatbot Support

---

# 📷 Screenshots

Add screenshots of:

- Login Page
- Dashboard
- Student Profile
- Attendance Module
- Fee Module
- Library Module
- IA Marks Module

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your branch.
5. Create a Pull Request.

---

# 📄 License

This project is developed for educational and academic purposes.

---

# 👨‍💻 Developed By

**Shabber**

Computer Science Engineering

Python | Django | Flutter | PostgreSQL | REST API

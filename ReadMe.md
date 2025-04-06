# 📦 Lost & Found System – Django Backend API

This is a backend-only **Lost & Found System for Ghana**, built using **Django REST Framework**, JWT authentication, and tested entirely using **Postman**. It allows **passengers**, **drivers**, and **admins** to register, report lost/found items, and automatically match them based on descriptions and location.

---

## 🚀 Features

- ✅ User registration & login (role-based)
- ✅ JWT-based authentication
- ✅ Role selection: **Passenger**, **Driver**, **Admin**
- ✅ Drivers can enter vehicle details
- ✅ Report **Lost** and **Found** items
- ✅ Automatic matching system with match score logic
- ✅ Admin can view all users, items, and matches
- ✅ SMS/Notification alert placeholder
- ✅ API tested with Postman only (No frontend)

---

## 🛠️ Tech Stack

- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite (default DB)
- JWT (Simple JWT)
- Postman for testing

---

##  Installation & Setup  
### Clone the Repository  
git clone https://github.com/IreneAbbey/Lost-Found.git
cd Lost-Found


## 📌 API Endpoints

| Method | Endpoint            | Description                            | Auth Required      |
|--------|---------------------|----------------------------------------|--------------------|
| POST   | `/register/`        | Register user (passenger or driver)    | ❌ No              |
| POST   | `/login/`           | Login to get JWT token                 | ❌ No              |
| POST   | `/lost/`            | Report a lost item                     | ✅ Yes             |
| GET    | `/profile/`         | View user profile                      | ✅ Yes             |
| POST   | `/found/`           | Report a found item                    | ✅ Yes             |
| POST   | `/matches/`         | Trigger item matching manually         | ✅ Yes             |
| GET    | `/dashboard/`       | Admin: view all users                  | ✅ Admin only      |

## Sample Test Data

### Register Passenger

POST /register/
{
  "username": "ama",
  "email": "ama@example.com",
  "password": "Ama1234!",
  "phone_number": "0551234567",
  "role": "passenger"
}


## Install requirements
pip install django djangorestframework djangorestframework-simplejwt

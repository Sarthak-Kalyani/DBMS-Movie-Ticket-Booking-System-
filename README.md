# DBMS-Movie-Ticket-Booking-System
# 🎬 Movie Ticket Booking System

A web-based movie ticket reservation system built using **Python Flask and MySQL**.  
Users can view movie shows, select seats visually, and book tickets online.  
The system prevents double booking using database transactions and stores all records digitally.


## ✨ Features
- User registration & login  
- View shows by city and format (2D / 3D / IMAX / 4DX)  
- Interactive seat map showing booked & available seats  
- Seat types: Regular, Premium, VIP, Recliner  
- Automatic ticket generation  
- Booking & payment records stored in database  
- Prevents double booking using seat locking  


## 🛠 Technologies Used

### Frontend
- HTML  
- CSS  
- JavaScript  

### Backend
- Python (Flask)

### Database
- MySQL

### Tools
- VS Code  
- MySQL Workbench  


## 📁 Project Structure

moving_booking/
│── app.py  
│── schema.sql  
│── test_app.py  

templates/  
├── index.html  
└── index_v2.html  

.venv/  
├── Lib/  
├── Scripts/  
├── .gitignore  
└── pyvenv.cfg  

## ⚙️ How to Run the Project

### 1. Open Project Folder
cd moving_booking

### 2. Activate Virtual Environment (Windows)
.venv\Scripts\activate

### 3. Install Required Libraries
pip install flask mysql-connector-python werkzeug

### 4. Setup Database
Open MySQL Workbench and run:

CREATE DATABASE movie_booking;  
USE movie_booking;  
SOURCE schema.sql;

### 5. Configure Database Password
Edit `app.py` and update your MySQL password.

### 6. Run Application
python app.py

Open browser:  
http://127.0.0.1:5000

## 🧠 How the System Works
1. User registers or logs in  
2. System loads shows from MySQL database  
3. User selects seats visually  
4. Seats are locked using SQL transaction  
5. Booking & payment saved in database  
6. Ticket is generated instantly  


## 🔒 Double Booking Prevention
The system locks seats during booking using SQL row locking to ensure the same seat cannot be booked by multiple users.


## 📊 Database Tables
- Movie  
- Theater  
- Screen  
- Seat  
- Show  
- MovieUser  
- Booking  
- Ticket  
- Payment  


## 👨‍💻 Project Type
Academic mini-project for DBMS / Software Engineering Lab.

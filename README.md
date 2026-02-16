# DBMS-Movie-Ticket-Booking-System
🎬 Movie Ticket Booking System

A web-based movie ticket reservation system built using Python Flask and MySQL.
Users can view movie shows, select seats visually, and book tickets online.
The system prevents double booking using database transactions and stores all records digitally.

✨ Features
1. User registration & login
2. View shows by city and format (2D / 3D / IMAX / 4DX)
3. Interactive seat map (shows booked & available seats)
4. Seat types: Regular, Premium, VIP, Recliner
5. Automatic ticket generation
6. Booking & payment records stored in database
7. Prevents double booking using seat locking

🛠 Technologies Used

Frontend
.HTML
.CSS
.JavaScript

Backend
.Python (Flask)

Database
.MySQL

Tools
.VS Code
.MySQL Workbench

📁 Project Structure
moving_booking/
│── app.py
│── schema.sql
│── test_app.py
│
├── templates/
│     ├── index.html
│     └── index_v2.html
│
└── .venv/
      ├── Lib/
      ├── Scripts/
      ├── .gitignore
      └── pyvenv.cfg

⚙️ How to Run the Project
1️⃣ Open Project Folder

Open the project in VS Code or Terminal

cd moving_booking

2️⃣ Activate Virtual Environment

Windows:

.venv\Scripts\activate

3️⃣ Install Required Libraries (if needed)
pip install flask mysql-connector-python werkzeug

4️⃣ Setup Database

Open MySQL Workbench and run:

CREATE DATABASE movie_booking;
USE movie_booking;
SOURCE schema.sql;

5️⃣ Configure Database Password

Open app.py and update:

db_cfg = {
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',
    'host': '127.0.0.1',
    'database': 'movie_booking'
}

6️⃣ Run the Application
python app.py


Now open browser:

http://127.0.0.1:5000

🧠 How the System Works

1. User registers or logs in
2.System loads shows from MySQL database
3.User selects seats visually
4.Seats are locked using SQL transaction
5.Booking & payment saved in database
6.Ticket is generated instantly

🔒 Double Booking Prevention

The system locks seats during booking:

SELECT id FROM Seat WHERE id IN (...) FOR UPDATE;


This ensures the same seat cannot be booked by multiple users.

📊 Database Tables

.Movie
.Theater
.Screen
.Seat
.Show
.MovieUse
.Booking
.Ticket
.Payment

📌 Note

.venv folder is included only for local development and should normally be ignored in GitHub using .gitignore.

👨‍💻 Project Type

Academic mini-project for DBMS / Software Engineering lab.

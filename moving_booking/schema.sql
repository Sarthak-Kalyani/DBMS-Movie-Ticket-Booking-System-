-- ==========================================================
--  MOVIE BOOKING SYSTEM DATABASE SCHEMA
--  Works 100% in MySQL Workbench
-- ==========================================================

-- Create database
DROP DATABASE IF EXISTS movie_booking;
CREATE DATABASE movie_booking;
USE movie_booking;

-- ==========================================================
-- 1. THEATER TABLE
-- ==========================================================
CREATE TABLE Theater (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100)
);

-- ==========================================================
-- 2. SCREEN TABLE
-- ==========================================================
CREATE TABLE Screen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    theater_id INT NOT NULL,
    name VARCHAR(100),
    total_seats INT,
    FOREIGN KEY (theater_id) REFERENCES Theater(id) ON DELETE CASCADE
);

-- ==========================================================
-- 3. MOVIE TABLE
-- ==========================================================
CREATE TABLE Movie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    duration_min INT,
    language VARCHAR(50),
    genre VARCHAR(100),
    release_date DATE
);

-- ==========================================================
-- 4. SHOW TABLE
-- ==========================================================
CREATE TABLE `Show` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    screen_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES Movie(id) ON DELETE CASCADE,
    FOREIGN KEY (screen_id) REFERENCES Screen(id) ON DELETE CASCADE,
    UNIQUE (screen_id, start_time)
);

-- ==========================================================
-- 5. SEAT TABLE
-- ==========================================================
CREATE TABLE Seat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    screen_id INT NOT NULL,
    row_label VARCHAR(5),
    seat_number INT,
    seat_type ENUM('Regular','Premium','VIP') DEFAULT 'Regular',
    UNIQUE(screen_id, row_label, seat_number),
    FOREIGN KEY (screen_id) REFERENCES Screen(id) ON DELETE CASCADE
);

-- ==========================================================
-- 6. USER TABLE
-- ==========================================================
CREATE TABLE MovieUser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255)
);

-- ==========================================================
-- 7. BOOKING TABLE
-- ==========================================================
CREATE TABLE Booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    show_id INT NOT NULL,
    booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(9,2),
    status ENUM('CONFIRMED','CANCELLED','PENDING') DEFAULT 'PENDING',
    FOREIGN KEY (user_id) REFERENCES MovieUser(id),
    FOREIGN KEY (show_id) REFERENCES `Show`(id)
);

-- ==========================================================
-- 8. TICKET TABLE
-- ==========================================================
CREATE TABLE Ticket (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    show_id INT NOT NULL,
    seat_id INT NOT NULL,
    price DECIMAL(8,2),
    status ENUM('BOOKED','CANCELLED') DEFAULT 'BOOKED',
    FOREIGN KEY (booking_id) REFERENCES Booking(id) ON DELETE CASCADE,
    FOREIGN KEY (show_id) REFERENCES `Show`(id),
    FOREIGN KEY (seat_id) REFERENCES Seat(id)
);

-- ==========================================================
-- 9. PAYMENT TABLE
-- ==========================================================
CREATE TABLE Payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(9,2),
    method ENUM('CARD','UPI','CASH') DEFAULT 'CARD',
    payment_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('SUCCESS','FAILED') DEFAULT 'SUCCESS',
    FOREIGN KEY (booking_id) REFERENCES Booking(id)
);

-- ==========================================================
-- INSERT SAMPLE DATA
-- ==========================================================

-- THEATERS
INSERT INTO Theater (name, address, city) VALUES
('Galaxy Cinemas', 'Sector 18, Noida', 'Noida'),
('City Mall Multiplex', 'MG Road, Lucknow', 'Lucknow');

-- SCREENS
INSERT INTO Screen (theater_id, name, total_seats) VALUES
(1, 'Screen 1', 60),
(1, 'Screen 2', 40),
(2, 'Screen A', 50);

-- MOVIES
INSERT INTO Movie (title, duration_min, language, genre, release_date) VALUES
('The Last Heist', 120, 'English', 'Action', '2025-03-15'),
('The Silent Lake', 95, 'Hindi', 'Thriller', '2025-05-01');

-- SHOWS
INSERT INTO `Show` (movie_id, screen_id, start_time, price) VALUES
(1, 1, '2025-12-01 18:00:00', 250.00),
(2, 1, '2025-12-01 21:00:00', 180.00),
(2, 2, '2025-12-02 20:00:00', 200.00);

-- MOVIE USERS
INSERT INTO MovieUser (name, email, phone, password_hash) VALUES
('Sarthak Kalyani', 'sarthak@example.com', '9999999999', 'hashed_password');

-- ==========================================================
-- AUTO-GENERATE 60 SEATS FOR SCREEN 1 (A–F, 10 seats each)
-- ==========================================================
INSERT INTO Seat (screen_id, row_label, seat_number, seat_type)
SELECT 
    1,
    r.row_label,
    s.seat_number,
    CASE 
        WHEN r.row_label = 'A' THEN 'VIP'
        WHEN r.row_label = 'B' THEN 'Premium'
        ELSE 'Regular'
    END AS seat_type
FROM 
    (SELECT 'A' AS row_label UNION
     SELECT 'B' UNION
     SELECT 'C' UNION
     SELECT 'D' UNION
     SELECT 'E' UNION
     SELECT 'F') r,
    (SELECT 1 AS seat_number UNION
     SELECT 2 UNION
     SELECT 3 UNION
     SELECT 4 UNION
     SELECT 5 UNION
     SELECT 6 UNION
     SELECT 7 UNION
     SELECT 8 UNION
     SELECT 9 UNION
     SELECT 10) s;

-- ==========================================================
-- DONE
-- ==========================================================


CREATE DATABASE IF NOT EXISTS blood_donation_db;
USE blood_donation_db;

-- Donors Table
CREATE TABLE IF NOT EXISTS donors (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    blood_type VARCHAR(5) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    eligibility_status VARCHAR(20) DEFAULT 'Eligible',
    last_donation_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Blood Inventory Table
CREATE TABLE IF NOT EXISTS blood_inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    blood_type VARCHAR(5) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    unit VARCHAR(10) DEFAULT 'units',
    min_stock_level INT NOT NULL DEFAULT 10,
    expiry_date DATE,
    storage_location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_blood_type (blood_type)
);

-- Donations Table
CREATE TABLE IF NOT EXISTS donations (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    donation_date DATE NOT NULL,
    blood_type VARCHAR(5) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit VARCHAR(10) DEFAULT 'units',
    collection_location VARCHAR(100),
    staff_name VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id) ON DELETE CASCADE
);

-- Blood Requests Table
CREATE TABLE IF NOT EXISTS blood_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    requester_name VARCHAR(100) NOT NULL,
    requester_type VARCHAR(50) NOT NULL,
    request_date DATE NOT NULL,
    blood_type VARCHAR(5) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit VARCHAR(10) DEFAULT 'units',
    urgency_level VARCHAR(20) DEFAULT 'Normal',
    patient_name VARCHAR(100),
    hospital_name VARCHAR(100),
    contact_number VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Pending',
    fulfilled_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample blood inventory
INSERT INTO blood_inventory (blood_type, quantity, min_stock_level, storage_location) VALUES
('A+', 25, 10, 'Refrigerator A1'),
('A-', 15, 5, 'Refrigerator A2'),
('B+', 30, 10, 'Refrigerator B1'),
('B-', 12, 5, 'Refrigerator B2'),
('AB+', 18, 8, 'Refrigerator AB1'),
('AB-', 8, 3, 'Refrigerator AB2'),
('O+', 40, 15, 'Refrigerator O1'),
('O-', 20, 8, 'Refrigerator O2');

-- Insert sample donors
INSERT INTO donors (full_name, date_of_birth, gender, blood_type, phone_number, email, address, eligibility_status, last_donation_date) VALUES
('Kristine Joy Dimayuga', '2002-05-15', 'Female', 'O+', '0985-119-7247', 'kristinejoydimayuga@email.com', '123 Bagbag St, Batangas City', 'Eligible', '2024-01-15'),
('Dianalyn Mayari', '2005-08-22', 'Female', 'A+', '0910-060-8421', 'dianalynmayari@email.com', '456 D.Limon St, Calaca City', 'Eligible', '2024-02-10'),
('Blessie Catibog', '2004-11-30', 'Female', 'B+', '0970-300-9135', 'blessiecatibpog@email.com', '789 G.Limjoco St, Lipa City', 'Eligible', '2024-01-20'),
('Rhyzel Benitez', '2005-03-18', 'Female', 'AB-', '0995-671-5790', 'rhyzelbenitez@email.com', '321 Acacia St, Batangas City', 'Eligible', NULL),
('Reyniel Calape', '2004-07-05', 'Male', 'O-', '0950-249-0449', 'reynielcalape@email.com', '654 Centro St, LipaCity', 'Eligible', '2024-02-05');

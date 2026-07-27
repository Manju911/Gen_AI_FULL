import sqlite3

conn = sqlite3.connect("data/hospital.db")
cursor = conn.cursor()

# =====================================================
# Patients
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    patient_name TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    disease TEXT,
    doctor_name TEXT,
    department TEXT,
    room_no TEXT,
    admission_date TEXT,
    discharge_date TEXT,
    patient_status TEXT,
    bill_amount INTEGER,
    insurance_provider TEXT,
    city TEXT
)
""")

patients = [
("P001","Rahul Sharma",45,"Male","O+","Diabetes","Dr. Anil Kumar","General Medicine","101","2025-01-10","2025-01-18","Discharged",45000,"Star Health","Bangalore"),
("P002","Priya Nair",30,"Female","A+","Migraine","Dr. Kavya Rao","Neurology","102","2025-02-05","2025-02-08","Discharged",18000,"HDFC Ergo","Hyderabad"),
("P003","Amit Verma",58,"Male","B+","Heart Disease","Dr. Suresh Iyer","Cardiology","201","2025-03-01","2025-03-15","Discharged",175000,"ICICI Lombard","Pune"),
("P004","Sneha Kapoor",24,"Female","AB+","Dengue","Dr. Pooja Shah","General Medicine","103","2025-04-12","2025-04-18","Discharged",38000,"Niva Bupa","Delhi"),
("P005","Vikram Singh",67,"Male","O-","Kidney Stones","Dr. Nitin Mehta","Urology","202","2025-05-20","2025-05-28","Discharged",92000,"Star Health","Mumbai"),
("P006","Neha Reddy",41,"Female","B-","Asthma","Dr. Kavya Rao","Neurology","104","2025-06-08",None,"Admitted",28000,"Care Health","Hyderabad"),
("P007","Arjun Mehta",36,"Male","A-","Fracture","Dr. Akash Patel","Orthopedics","203","2025-06-18","2025-06-25","Discharged",56000,"HDFC Ergo","Ahmedabad"),
("P008","Divya Menon",52,"Female","O+","Hypertension","Dr. Anil Kumar","General Medicine","105","2025-07-02",None,"Admitted",34000,"Star Health","Chennai"),
("P009","Rohan Das",29,"Male","A+","Appendicitis","Dr. Shweta Gupta","Surgery","204","2025-07-10","2025-07-15","Discharged",67000,"ICICI Lombard","Kolkata"),
("P010","Meera Joshi",61,"Female","B+","Arthritis","Dr. Ramesh Nair","Orthopedics","205","2025-07-18",None,"Admitted",48000,"Care Health","Pune"),
("P011","Suresh Patil",55,"Male","O+","Pneumonia","Dr. Pooja Shah","General Medicine","106","2025-08-01","2025-08-08","Discharged",52000,"Niva Bupa","Bangalore"),
("P012","Kiran Rao",33,"Male","AB-","Malaria","Dr. Pooja Shah","General Medicine","107","2025-08-03","2025-08-09","Discharged",31000,"Star Health","Mysore"),
("P013","Ananya Roy",47,"Female","A-","Thyroid","Dr. Anil Kumar","Endocrinology","108","2025-08-12",None,"Admitted",26000,"HDFC Ergo","Delhi"),
("P014","Harish Kumar",50,"Male","B+","High BP","Dr. Anil Kumar","General Medicine","109","2025-08-18","2025-08-23","Discharged",22000,"Care Health","Hyderabad"),
("P015","Pooja Singh",38,"Female","O+","Kidney Infection","Dr. Nitin Mehta","Urology","210","2025-09-01",None,"Admitted",71000,"Star Health","Mumbai"),
("P016","Ravi Gupta",43,"Male","A+","Stroke","Dr. Suresh Iyer","Cardiology","211","2025-09-05",None,"Critical",210000,"ICICI Lombard","Noida"),
("P017","Lakshmi Iyer",65,"Female","B-","Heart Disease","Dr. Suresh Iyer","Cardiology","212","2025-09-10","2025-09-20","Discharged",189000,"Star Health","Chennai"),
("P018","Nikhil Jain",27,"Male","O-","Food Poisoning","Dr. Pooja Shah","General Medicine","110","2025-09-15","2025-09-17","Discharged",15000,"None","Jaipur"),
("P019","Deepa Sharma",49,"Female","AB+","Migraine","Dr. Kavya Rao","Neurology","111","2025-09-18",None,"Admitted",41000,"Care Health","Bangalore"),
("P020","Manoj Verma",60,"Male","A+","Diabetes","Dr. Anil Kumar","General Medicine","112","2025-09-22",None,"Admitted",39000,"HDFC Ergo","Lucknow")
]

cursor.executemany(
    "INSERT OR REPLACE INTO patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    patients
)

conn.commit()
conn.close()

print("Hospital database created successfully!")
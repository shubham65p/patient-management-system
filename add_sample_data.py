import sqlite3
from datetime import datetime, timedelta
import random

def add_sample_patients():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    
    # Sample data
    first_names = ["Rajesh", "Priya", "Amit", "Sunita", "Vikram", "Anita", "Rahul", "Deepika", 
                   "Arjun", "Sneha", "Karan", "Neha", "Rohan", "Pooja", "Sanjay", "Kavita",
                   "Rahul", "Ritu", "Suresh", "Meera", "Vishal", "Anjali", "Mohit", "Swati", "Nitin"]
    
    last_names = ["Kumar", "Sharma", "Singh", "Patel", "Verma", "Gupta", "Reddy", "Rao",
                  "Desai", "Mehta", "Joshi", "Nair", "Iyer", "Kapoor", "Malhotra", "Chopra",
                  "Agarwal", "Bansal", "Saxena", "Mishra", "Pandey", "Jain", "Shah", "Bose", "Das"]
    
    genders = ["Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
               "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
               "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male"]
    
    complaints = [
        "Persistent headache and dizziness for 2 weeks",
        "Chest pain and shortness of breath",
        "Lower back pain radiating to legs",
        "Chronic cough and fever",
        "Abdominal pain and digestive issues",
        "High blood pressure management",
        "Diabetes type 2 monitoring",
        "Skin rash and itching",
        "Joint pain in knees and elbows",
        "Anxiety and sleep disturbances",
        "Migraine episodes",
        "Thyroid disorder follow-up",
        "Asthma management",
        "Acid reflux and heartburn",
        "Vision problems and eye strain",
        "Ear infection and hearing difficulty",
        "Allergic rhinitis",
        "Fatigue and weakness",
        "Depression and mood swings",
        "Hypertension control",
        "Arthritis pain management",
        "Upper respiratory infection",
        "Gastrointestinal discomfort",
        "Chronic sinusitis",
        "Vitamin D deficiency"
    ]
    
    addresses = [
        "123 MG Road, Bangalore",
        "45 Park Street, Kolkata",
        "67 Marine Drive, Mumbai",
        "89 Connaught Place, Delhi",
        "12 Anna Salai, Chennai",
        "34 MG Road, Pune",
        "56 Brigade Road, Bangalore",
        "78 Park Lane, Hyderabad",
        "90 Salt Lake, Kolkata",
        "23 Bandra West, Mumbai",
        "45 Sector 18, Noida",
        "67 Malviya Nagar, Jaipur",
        "89 Jubilee Hills, Hyderabad",
        "12 Jayanagar, Bangalore",
        "34 Karol Bagh, Delhi",
        "56 T Nagar, Chennai",
        "78 Koramangala, Bangalore",
        "90 Worli, Mumbai",
        "23 Gachibowli, Hyderabad",
        "45 Rajouri Garden, Delhi",
        "67 Whitefield, Bangalore",
        "89 Andheri East, Mumbai",
        "12 Indiranagar, Bangalore",
        "34 Dwarka, Delhi",
        "56 Powai, Mumbai"
    ]
    
    phone_prefixes = ["98", "99", "97", "96", "95", "94", "93", "92", "91", "90",
                      "89", "88", "87", "86", "85", "84", "83", "82", "81", "80",
                      "79", "78", "77", "76", "75"]
    
    # Generate 25 patient records
    for i in range(25):
        name = f"{first_names[i]} {last_names[i]}"
        age = random.randint(18, 85)
        gender = genders[i]
        
        # Generate date of birth based on age
        today = datetime.now()
        dob = (today - timedelta(days=age*365)).strftime("%Y-%m-%d")
        
        # Generate phone number
        phone = f"+91 {phone_prefixes[i]}{random.randint(10000000, 99999999)}"
        
        address = addresses[i]
        
        # Generate first appointment date (random date in last 60 days)
        days_ago = random.randint(1, 60)
        first_appointment = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        major_complain = complaints[i]
        
        # Generate follow-up date (random date in next 30 days)
        days_ahead = random.randint(1, 30)
        followup_date = (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        total_followups = random.randint(0, 10)
        
        # Insert into database
        cursor.execute('''
            INSERT INTO patients (name, age, gender, dob, phone, address, 
                                first_appointment, major_complain, followup_date, total_followups)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, dob, phone, address, first_appointment, 
              major_complain, followup_date, total_followups))
    
    conn.commit()
    conn.close()
    print("✅ Successfully added 25 sample patient records to the database!")
    print("You can now run the Patient Management System to view them.")

if __name__ == "__main__":
    add_sample_patients()
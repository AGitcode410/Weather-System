import requests
import mysql.connector # type: ignore
import time
from datetime import datetime
api_key='55f5312003c036ce48901b62a8350172'
session=requests.Session()
conn=mysql.connector.connect(host='localhost', user='root', password='anishG2010', database='weather')
cursor=conn.cursor()
cities = [
    # Andhra Pradesh
    "Amaravati", "Visakhapatnam", "Vijayawada", "Tirupati", "Chittoor",

    # Arunachal Pradesh
    "Itanagar", 

    # Assam
    "Dispur", "Guwahati",  

    # Bihar
    "Patna", "Gaya", "Bhagalpur",

    # Chhattisgarh
    "Raipur", "Bilaspur",

    # Goa
    "Panaji", "Margao",

    # Gujarat
    "Ahmedabad", "Surat", "Vadodara", "Rajkot", 

    # Haryana
    "Gurugram", "Faridabad", "Panipat",

    # Himachal Pradesh
    "Shimla", "Manali",

    # Jharkhand
    "Ranchi", "Jamshedpur", 
    
    # Karnataka
    "Bengaluru", "Mysuru", "Mangaluru", 
    "Belagavi", "Tumakuru", "Udupi",

    # Kerala
    "Thiruvananthapuram", "Kochi", "Kozhikode",
    "Thrissur", "Kannur", "Kollam",

    # Madhya Pradesh
    "Bhopal", "Indore", "Jabalpur",

    # Maharashtra
    "Mumbai", "Pune", "Nagpur", "Kolhapur",

    # Manipur
    "Imphal", 

    # Meghalaya
    "Shillong", "Mawsynram",

    # Mizoram
    "Aizawl", 

    # Nagaland
    "Kohima", 

    # Odisha
    "Bhubaneswar", "Cuttack", "Rourkela", 

    # Punjab
    "Ludhiana", "Amritsar", "Jalandhar", "Patiala",

    # Rajasthan
    "Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer",

    # Sikkim
    "Gangtok", "Namchi",

    # Telangana
    "Hyderabad", "Warangal", "Nizamabad",

    # Tripura
    "Agartala", "Dharmanagar",

    # Uttar Pradesh
    "Lucknow", "Kanpur", "Varanasi", "Agra",
    "Noida", "Ayodhya", "Bareilly",

    # Uttarakhand
    "Dehradun", "Haridwar", "Rishikesh", "Nainital",

    # West Bengal
    "Kolkata", "Durgapur", "Howrah",

    # Tamil Nadu - North
    "Chennai", "Tambaram", "Avadi", "Pallavaram",
    "Poonamallee", "Sriperumbudur", "Kanchipuram",
    "Chengalpattu", "Tiruvallur", "Vellore",
    "Ranipet", "Tiruvannamalai", "Krishnagiri",
    "Dharmapuri", "Villupuram", "Cuddalore",
    "Tindivanam", "Maraimalai Nagar",

    # Tamil Nadu - West
    "Coimbatore", "Tiruppur", "Erode", "Salem",
    "Namakkal", "Karur", "Pollachi", "Mettupalayam",
    "Udumalaipettai", "Attur", "Mettur",
    "Ooty", "Coonoor", "Yercaud",

    # Tamil Nadu - Central
    "Tiruchirappalli", "Thanjavur", "Kumbakonam",
    "Nagapattinam", "Mayiladuthurai", "Mannargudi",
    "Thiruvarur", "Pudukkottai", "Chidambaram",

    # Tamil Nadu - South
    "Madurai", "Tirunelveli", "Thoothukudi",
    "Nagercoil", "Rameswaram", "Dindigul",
    "Sivakasi", "Rajapalayam", "Virudhunagar",
    "Theni", "Tenkasi", "Karaikudi",
    "Kovilpatti", "Paramakudi", "Palani",
    "Tiruchendur", "Velankanni", "Kodaikanal",

    # Union Territories
    "New Delhi", "Chandigarh", "Puducherry",
    "Port Blair", "Srinagar", "Jammu",
    "Leh", "Kavaratti", "Daman",
    "Diu", "Silvassa",

    # Additional Major Cities
    "Junagadh", "Jamnagar", "Porbandar",
     "Rohtak", "Solan",
    "Bokaro", "Anantapur", "Nellore",
    "Darbhanga", "Jagdalpur", "Vasco da Gama",
    "Kalaburagi", "Palakkad", "Malappuram",
    "Satna", "Akola", "Jalgaon",
    "Mokokchung", "Sambalpur", "Bikaner", 
    "Moradabad", "Roorkee", "Surathkal"
]


def log(message):
    with open("weather_update_log.txt",'a') as file:
        file.write(f"{datetime.now()} - {message}\n")
        

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response=session.get(url,timeout=5)#this statement asks the platform for the data using the API key 
    
        scode=response.status_code
        if scode!=200:
            log(f"{city} : {scode}")
            return None
        data=response.json() #this gives the data in dictionary format
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"{city} : {e}")
        log(f"{city} : {e}")
        return None

def create_city_tables():    
    cursor.execute(f"""create table if not exists weather_data (id int primary key auto_increment, city varchar(100), temperature float,humidity int, pressure int, wind_speed float, weather_condition varchar(255), timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
create_city_tables()

def add_data(city,weather):
    global cursor
    temperature=weather['main']['temp']
    humidity=weather['main']['humidity']
    condition=weather['weather'][0]['description']
    wind_speed=weather['wind']['speed']
    pressure=weather['main']['pressure']

    try:
        cursor.execute(f"""insert into weather_data (city,temperature,humidity,pressure,wind_speed,weather_condition) values (%s,%s,%s,%s,%s,%s)""",(city,temperature, humidity, pressure, wind_speed, condition))

    except mysql.connector.Error as e:
        print(e)
        log(f"MySQL Error while inserting {city} : {e}")
        try:
            if not conn.is_connected():
                conn.reconnect(attempts = 3, delay = 1)
                cursor = conn.cursor()

            cursor.execute(f"""insert into weather_data (city,temperature,humidity,pressure,wind_speed,weather_condition) values (%s,%s,%s,%s,%s,%s)""",(city,temperature, humidity, pressure, wind_speed, condition))

        except mysql.connector.Error as e1:
            log(f"Retry insert failed for {city} : {e1}")

def auto_update():
    while True:
        log("\n\n\n\n")
        global cursor
        if not conn.is_connected():
            conn.reconnect(attempts = 3, delay = 1)
            cursor = conn.cursor()

        failures = []
        still_failed = []
        successes = 0
        print("Starting Update...")
        log("Starting Update...")
        for city in cities:
            try:
                weather = get_weather(city)
            
                if weather:
                    add_data(city,weather)
                    successes += 1
                    log(f"{city} updated successfully.")
                else:
                    failures.append(city)
                    log(f"{city} failed on first attempt.")
            
            except Exception as e:
                failures.append(city)
                log(f"Unexpected error for {city} : {e}")

            time.sleep(1)
        
        conn.commit()

        print("Failed cities:")
        print(*failures, sep = "\n")
        for entity in failures:
            for attempt in range(3):
                try:
                    weather = get_weather(entity)

                    if weather:
                        add_data(entity,weather)
                        successes += 1
                        log(f"{entity} recovered on retry {attempt+1}.")
                        break

                except Exception as e:
                    log(f"Retry error for {entity} : {e}")
                
                time.sleep(2)
            
            else:
                still_failed.append(entity)
                log(f"{entity} failed after 3 retries.")

        conn.commit()
        
        failures=still_failed
        print(f"Successes : {successes}")
        print(f"Failures : {len(failures)}")
        print("Update Complete..")
        log("Update Complete..")
        log("\n\n\n\n")

        time.sleep(1800)
auto_update()


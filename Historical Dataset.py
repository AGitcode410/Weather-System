import requests
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(host="localhost",user="root",password="K3nilaniganesh:)",database="weather_data")
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
    "Tindivanam",

    # Tamil Nadu - West
    "Coimbatore", "Tiruppur", "Erode", "Salem",
    "Namakkal", "Karur", "Pollachi", "Mettupalayam",
    "Attur", "Mettur",
    "Ooty", "Coonoor", "Yercaud",

    # Tamil Nadu - Central
    "Tiruchirappalli", "Thanjavur", "Kumbakonam",
    "Nagapattinam", "Mayiladuthurai", "Mannargudi",
    "Thiruvarur", "Pudukkottai", "Chidambaram",

    # Tamil Nadu - South
    "Madurai", "Tirunelveli", "Thoothukudi",
    "Nagercoil", "Rameswaram", "Dindigul",
    "Sivakasi", "Rajapalayam",
    "Theni", "Tenkasi", "Karaikudi",
    "Kovilpatti", "Palani",
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

cursor.execute("""create table if not exists historical_data 
                            (id int primary key auto_increment, city varchar(100), 
                            date date, temp_mean float, temp_max float, temp_min float, 
                            precipitation_sum float, precipitation_hours float,
                            cloud_cover_max int, cloud_cover_mean int, cloud_cover_min int,
                            surface_pressure_mean float, surface_pressure_max float, surface_pressure_min float,
                            wind_speed_max float, wind_direction_dominant int, wind_speed_min float, wind_speed_mean float, 
                            relative_humidity_mean int, relative_humidity_max int, relative_humidity_min int, unique (city, date))""")
conn.commit()

def retrieve_data(cities):
    coords = []
    cnt = 0
    ls=[]
    lf=[]
    for cty in cities:
        cursor.execute("""select city, latitude, longitude from city_coords where city = %s""", (cty,))
        coord = cursor.fetchone()
        if coord is not None:
            coords.append(coord)
    print(len(coords))
    for i in coords:
        print(i)
        city = i[0]
        lat = i[1]
        lon = i[2]
            
        url = f"https://archive-api.open-meteo.com/v1/archive"
        parameters = {
                        "latitude": lat,
                        "longitude": lon,
                        "start_date": "2026-10-01",
                        "end_date": "2026-10-15",
                        "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", 
                                "precipitation_sum", "precipitation_hours", 
                                "cloud_cover_max", "cloud_cover_mean", "cloud_cover_min", 
                                "surface_pressure_mean", "surface_pressure_max", "surface_pressure_min", 
                                "winddirection_10m_dominant", "wind_speed_10m_max", "wind_speed_10m_min", "wind_speed_10m_mean", 
                                "relative_humidity_2m_mean", "relative_humidity_2m_max", "relative_humidity_2m_min"],
                        "timezone": "Asia/Kolkata",
                        "wind_speed_unit": "ms"
                     }
        try:
            response = requests.get(url, params=parameters, timeout=10)
            response.raise_for_status()
            data = response.json()

            print(f"Data retrieved for {city}: {data}")
             

            dt=data['daily']['time']
            dtem=data['daily']['temperature_2m_mean']
            dtex=data['daily']['temperature_2m_max']
            dten=data['daily']['temperature_2m_min']
            dps=data['daily']['precipitation_sum']
            dph=data['daily']['precipitation_hours']
            dccx=data['daily']['cloud_cover_max']
            dccm=data['daily']['cloud_cover_mean']
            dccn=data['daily']['cloud_cover_min']
            dspm=data['daily']['surface_pressure_mean']
            dspx=data['daily']['surface_pressure_max']
            dspn=data['daily']['surface_pressure_min']
            dwd=data['daily']['winddirection_10m_dominant']
            dwsx=data['daily']['wind_speed_10m_max']
            dwsn=data['daily']['wind_speed_10m_min']
            dwsm=data['daily']['wind_speed_10m_mean']
            drhm=data['daily']['relative_humidity_2m_mean']
            drhx=data['daily']['relative_humidity_2m_max']
            drhn=data['daily']['relative_humidity_2m_min']


            for i in range(len(dt)):
                cursor.execute("""insert ignore into historical_data (city, date, temp_mean, temp_max, temp_min, 
                                precipitation_sum, precipitation_hours, cloud_cover_max, cloud_cover_mean, cloud_cover_min,
                                surface_pressure_mean, surface_pressure_max, surface_pressure_min,
                                wind_speed_max, wind_direction_dominant, wind_speed_min, wind_speed_mean,
                                relative_humidity_mean, relative_humidity_max, relative_humidity_min) 
                                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                               (city, dt[i], dtem[i], dtex[i], dten[i], dps[i], dph[i], dccx[i], dccm[i], dccn[i], dspm[i], dspx[i], dspn[i], dwsx[i], dwd[i], dwsn[i], dwsm[i], drhm[i], drhx[i], drhn[i]))
            conn.commit()
            cnt += 1 
            ls.append(city)  
            

        except requests.RequestException as e:
            print(f"Error retrieving data for {city}: {e}")
            lf.append(city)
            continue
    print("Data retrieval complete.")
    print(f"Total success: {cnt}")
    print(f"Cities with data: {ls}")
    print(f"Cities without data: {lf}")


retrieve_data(cities)





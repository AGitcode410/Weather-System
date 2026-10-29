import mysql.connector
import requests

conn = mysql.connector.connect(host="localhost",user="root",password="K3nilaniganesh:)",database="weather_data")
cursor=conn.cursor()
cursor.execute("""create table if not exists city_coords(id int unique key auto_increment, city varchar(100) primary key, latitude decimal(9,6), longitude decimal(9,6), country_code char(2), state varchar(100), timezone varchar(100), geocoded_name varchar(100))""")
conn.commit()
d={}

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


def get_coordinates(cities):
    for i in cities:
        try:
            url = f"https://geocoding-api.open-meteo.com/v1/search"
            response = requests.get(url,params={"name": i, "count": 1, "countryCode": "IN"},timeout=10)
            data = response.json()
            place = data['results']
            if place:
                ctry_code = place[0]['country_code']
                if ctry_code == "IN":
                    lat = place[0]['latitude']
                    long = place[0]['longitude']
                    state_name = place[0]['admin1']
                    timezone = place[0]['timezone']
                    geocoded_name = place[0]['name']
                    lst=[lat,long,ctry_code,state_name,timezone,geocoded_name]
                    d[i]=lst
                else:
                    print(f"{i} is not in India")
            else:
                print(f"No results found for {i}")

        except Exception as e:
            print(f"Error occurred while fetching coordinates for {i}: {e}")
            print(data)

    return d

D=get_coordinates(cities)

def insert_data(D):
    for i in cities:
        cursor.execute("""insert into city_coords (city, latitude, longitude, country_code, state, timezone, geocoded_name) values(%s,%s,%s,%s,%s,%s,%s)""",(i,D[i][0],D[i][1],D[i][2],D[i][3],D[i][4],D[i][5]))
    conn.commit()
print(len(get_coordinates(cities)))
insert_data(D)   
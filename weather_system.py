import requests
import tkinter as tk
import mysql.connector # type: ignore
import pandas as pd
import matplotlib.pyplot as plt



window=tk.Tk()
window.title("Weather App")
window.geometry("500x500")
main_frame = tk.Frame(window)
main_frame.pack(fill='both',expand=True)
graph_frame = tk.Frame(window)
title=tk.Label(main_frame,text="Weather App",font=("Arial",20,"bold"))
title.pack(pady=5)
entry=tk.Entry(main_frame,width=40)
entry.pack(pady=10)
result=tk.Label(main_frame,text="",justify="left",font=("Segoe UI Emoji",11))
result.pack(pady=10)
api_key=''#this is the API key which is like a key to a door which opens to a world of data provided by a platform

cursor=conn.cursor()
cursor.execute("""create table if not exists search_history(id int primary key auto_increment, city varchar(100))""")
conn.commit()

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



def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response=requests.get(url)#this statement asks the platform for the data using the API key 
    
    scode=response.status_code
    print(scode)
    if scode!=200:
        return None
    data=response.json() #this gives the data in dictionary format
    return data



def search(city):
    cursor.execute("""insert into search_history (city)
                   values(%s)""",(city,))
    conn.commit()

def fetch():
    city=entry.get()
    if not city:
        result.config(text="Please enter a city name.")
        return
    
    weather=get_weather(city)

    if weather is None:
        result.config(text=f'{city} not found. Try Again')
    else:
        info=process(weather)
        result.config(text=info)
        search(city)
      

    entry.delete(0,tk.END)
    entry.focus()

def search_history():
    cursor.execute("select * from search_history order by id desc limit 5")
    rows=cursor.fetchall()

    if not rows:
        result.config(text='No history yet.')
        return
    
    text='Last searches:\n\n'
    for row in rows:
        text+=f'{row[1]}\n'

    result.config(text=text)


def process(weather):
    temperature=weather['main']['temp']
    humidity=weather['main']['humidity']
    condition=weather['weather'][0]['description']
    windspeed=weather['wind']['speed']
    pressure=weather['main']['pressure']
    
    if 'clear' in condition:
        icon='☀️'
    elif 'cloud' in condition:
        icon='☁️'
    elif 'rain' in condition:
        icon='🌧️'
    elif 'thunderstorm' in condition:
        icon='⛈️'
    elif 'snow' in condition:
        icon='❄️'
    elif 'mist' in condition or 'fog' in condition:
        icon='🌫️'
    else:
        icon='🌍'
    
    info=f"""City: {weather['name']}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nCondition:{icon} {condition.strip()}\nWind Speed: {windspeed}m/s\nPressure: {pressure}hPa"""

    return info

def create_city_tables():    
    cursor.execute(f"""create table if not exists weather_data (id int primary key auto_increment, city varchar(100), temperature float,humidity int, pressure int, wind_speed float, weather_condition varchar(255), timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
create_city_tables()

def graph():
    main_frame.pack_forget()
    graph_frame.pack(fill='both',expand=True)

    back_btn=tk.Button(graph_frame,text='⬅ Back',font=('Calibri',10),command=back)
    back_btn.pack(pady=10)
    x=tk.Label(graph_frame,text='X-axis:',font=('Times New Roman',11))
    x.pack(pady=5)
    xaxis=tk.Entry(graph_frame,width=20)
    xaxis.pack(pady=5)

    y=tk.Label(graph_frame,text='Y-axis:',font=('Times New Roman',11))
    y.pack(pady=5)
    yaxis=tk.Entry(graph_frame,width=20)
    yaxis.pack(pady=5)

    cty_entry=tk.Label(graph_frame,text='City:',font=('Times New Roman',11))
    cty_entry.pack(pady=5)
    cty=tk.Entry(graph_frame,width=20)
    cty.pack(pady=5)

    run_btn=tk.Button(graph_frame,text='Get Graph',font=('Calibri',12),command=lambda: create_graph(xaxis,yaxis,cty))
    run_btn.pack(pady=10)


def create_graph(xaxis,yaxis,cty):

    x_axis = xaxis.get()    
    y_axis = yaxis.get()
    cty=cty.get()

    cursor.execute(f"select {x_axis},{y_axis} from weather_data where city = %s order by {x_axis}",(cty,))
    rows=cursor.fetchall()
    df=pd.DataFrame(rows,columns=[x_axis,y_axis])
    if xaxis.get() == "Time":
        x_axis="Timestamp"
        df[x_axis]=pd.to_datetime(df[x_axis])

    plt.plot(df[x_axis],df[y_axis])
    plt.show()

def back():
    graph_frame.pack_forget()
    main_frame.pack(fill='both',expand=True)




graph_btn=tk.Button(main_frame,text='Graph',font=('Calibri',12),command=graph)
graph_btn.pack(pady=5)    
history_btn=tk.Button(main_frame,text='Show History', font=("Calibri",12), command = search_history)
history_btn.pack(pady=5)
button=tk.Button(main_frame,text='Get Weather',font=("Calibri",12),command=fetch)
button.pack(pady=7)
button=tk.Button(main_frame,text='Exit',font=("Calibri",12),command=exit)
button.pack(pady=5)
window.mainloop()

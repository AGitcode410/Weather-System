import requests
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt


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

api_key = "f8803b057a26b14a151cad16b89329cd"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="K3nilaniganesh:)",
    database="weather"
)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS search_history 
               (id INT PRIMARY KEY AUTO_INCREMENT,city VARCHAR(100))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS weather_data 
                (id INT PRIMARY KEY AUTO_INCREMENT,
                city VARCHAR(100),
                temperature FLOAT,
                humidity INT,
                pressure FLOAT,
                wind_speed FLOAT,
                weather_condition VARCHAR(255),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                """)

cursor.execute("""CREATE TABLE IF NOT EXISTS alerts 
                (id INT PRIMARY KEY AUTO_INCREMENT,
                city VARCHAR(100),
                forecast_date DATE,
                parameter VARCHAR(100),
                value FLOAT,
                threshold_value FLOAT,
                message VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                """)

conn.commit()


window = tk.Tk()
window.title("Weather App")
window.geometry("800x600")
window.minsize(650, 500)

main_frame = tk.Frame(window, padx=15, pady=10)
graph_frame = tk.Frame(window, padx=15, pady=10)
forecast_frame = tk.Frame(window, padx=15, pady=10)
report_frame = tk.Frame(window, padx=15, pady=10)
role_frame = tk.Frame(window, padx=15, pady=10)
password_frame = tk.Frame(window, padx=15, pady=10)


def show_page(page):
    main_frame.pack_forget()
    graph_frame.pack_forget()
    forecast_frame.pack_forget()
    report_frame.pack_forget()
    role_frame.pack_forget()
    password_frame.pack_forget()

    page.pack(fill="both", expand=True)


def back():
    show_page(main_frame)


# ROLE SELECTION PAGE

tk.Label(
    role_frame,
    text="Weather App",
    font=("Arial", 18, "bold")
).pack(pady=15)

tk.Label(
    role_frame,
    text="Choose how you want to enter:",
    font=("Arial", 11)
).pack(pady=8)

def normal_user():
    admin_stats_button.pack_forget()
    show_page(main_frame)

def admin_login():
    password_entry.delete(0, tk.END)
    password_message.config(text="")
    show_page(password_frame)

def check_password():
    if password_entry.get() == "AGapp":
        password_entry.delete(0, tk.END)
        password_message.config(text="")
        admin_stats_button.pack(before=exit_button, pady=3)
        show_page(main_frame)
    else:
        password_message.config(text="Incorrect password. Try again.")
        password_entry.delete(0, tk.END)

tk.Button(
    role_frame,
    text="Admin",
    font=("Arial", 10),
    width=22,
    command=admin_login
).pack(pady=4)

tk.Button(
    role_frame,
    text="Normal User",
    font=("Arial", 10),
    width=22,
    command=normal_user
).pack(pady=4)

tk.Label(
    password_frame,
    text="Admin Login",
    font=("Arial", 14, "bold")
).pack(pady=10)

tk.Label(
    password_frame,
    text="Enter admin password:"
).pack(pady=4)

password_entry = tk.Entry(password_frame, show="*", width=25)
password_entry.pack(pady=5)

password_message = tk.Label(password_frame, text="", fg="red")
password_message.pack(pady=4)

tk.Button(
    password_frame,
    text="Login",
    width=22,
    command=check_password
).pack(pady=4)

tk.Button(
    password_frame,
    text="Back",
    width=22,
    command=lambda: show_page(role_frame)
).pack(pady=4)


title = tk.Label(
    main_frame,
    text="Weather App",
    font=("Arial", 18, "bold"))
title.pack(pady=8)

entry = tk.Entry(main_frame, width=30, font=("Arial", 11))
entry.pack(pady=5)

result = tk.Label(
    main_frame,
    text="Enter a city to get live weather.",
    justify="left",
    font=("Arial", 10),
    wraplength=550)
result.pack(pady=8)

def search(city):
    cursor.execute("""
        INSERT INTO search_history (city)
        VALUES (%s)""", (city,))

    conn.commit()


def search_history():
    cursor.execute("""
        SELECT city
        FROM search_history
        ORDER BY id DESC
        LIMIT 5""")

    rows = cursor.fetchall()

    if not rows:
        result.config(text="No search history yet.")
        return

    text = "Last 5 searches:\n\n"

    for row in rows:
        text = text + row[0] + "\n"

    result.config(text=text)

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"}

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        return None

    return response.json()


def fetch():
    city = entry.get().strip()

    if city == "":
        messagebox.showerror(
            "Missing City",
            "Please enter a city name.")
        return

    if api_key == "":
        messagebox.showerror(
            "Missing API Key",
            "Enter your OpenWeatherMap API key in the code.")
        return

    try:
        weather = get_weather(city)

        if weather is None:
            messagebox.showerror(
                "City Not Found",
                "City not found. Check the spelling and try again.")
            return

        temperature = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
        wind_speed = weather["wind"]["speed"]
        condition = weather["weather"][0]["description"]

        info = (
            "City: " + weather["name"] + "\n"
            "Temperature: " + str(temperature) + " °C\n"
            "Humidity: " + str(humidity) + " %\n"
            "Condition: " + condition + "\n"
            "Wind speed: " + str(wind_speed) + " m/s\n"
            "Pressure: " + str(pressure) + " hPa")

        result.config(text=info)

        cursor.execute("""INSERT INTO weather_data
                (city, temperature, humidity, pressure,
                wind_speed, weather_condition)
                VALUES (%s, %s, %s, %s, %s, %s)""", 
                (weather["name"], temperature,
                humidity, pressure,
                wind_speed, condition))

        search(weather["name"])
        conn.commit()

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Connection Error",
            "Could not connect to OpenWeatherMap.")

    except mysql.connector.Error as error:
        conn.rollback()
        messagebox.showerror("Database Error", str(error))

    entry.delete(0, tk.END)


def get_coordinates(city):
    cursor.execute("""
        SELECT latitude, longitude
        FROM city_coords
        WHERE LOWER(city) = LOWER(%s)
        LIMIT 1
    """, (city,))

    return cursor.fetchone()


# ==================================================
# WEATHER CONDITION
# ==================================================

def get_condition(code):
    if code == 0:
        return "Clear sky"
    elif code in [1, 2, 3]:
        return "Partly cloudy"
    elif code in [45, 48]:
        return "Fog"
    elif code in [51, 53, 55, 56, 57]:
        return "Drizzle"
    elif code in [61, 63, 65, 66, 67]:
        return "Rain"
    elif code in [71, 73, 75, 77]:
        return "Snow"
    elif code in [80, 81, 82]:
        return "Rain showers"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    else:
        return "Unknown condition"


# ==================================================
# HISTORICAL WEATHER LINE GRAPH
# ==================================================

def correlation_graph():
    show_page(graph_frame)


tk.Label(
    graph_frame,
    text="Historical Weather Line Graph",
    font=("Arial", 14, "bold")
).pack(pady=8)

tk.Label(
    graph_frame,
    text="Select City:",
    font=("Arial", 10)
).pack()

graph_city = tk.StringVar(value=cities[0])

# Scrollable city list: displays five cities at a time
city_list_frame = tk.Frame(graph_frame)
city_list_frame.pack(pady=4)

city_scrollbar = tk.Scrollbar(city_list_frame, orient=tk.VERTICAL)
city_listbox = tk.Listbox(
    city_list_frame,
    height=5,
    width=25,
    font=("Arial", 10),
    yscrollcommand=city_scrollbar.set,
    exportselection=False
)
city_scrollbar.config(command=city_listbox.yview)

city_listbox.pack(side=tk.LEFT)
city_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

for city_name in cities:
    city_listbox.insert(tk.END, city_name)

city_listbox.selection_set(0)
city_listbox.activate(0)

def select_graph_city(event=None):
    selection = city_listbox.curselection()
    if selection:
        graph_city.set(city_listbox.get(selection[0]))

city_listbox.bind("<<ListboxSelect>>", select_graph_city)

tk.Label(
    graph_frame,
    text="Weather Parameter:",
    font=("Arial", 10)
).pack()

graph_parameter = tk.StringVar(value="Temperature")

parameter_menu = tk.OptionMenu(
    graph_frame,
    graph_parameter,
    "Temperature",
    "Cloud Cover",
    "Humidity",
    "Pressure",
    "Wind Speed",
    "Precipitation"
)

parameter_menu.config(font=("Arial", 10), width=22)
parameter_menu.pack(pady=4)


def create_graph():
    city = graph_city.get()
    parameter = graph_parameter.get()

    if parameter == "Temperature":
        column = "temp_max"
        label = "Maximum Temperature (°C)"

    elif parameter == "Cloud Cover":
        column = "cloud_cover_max"
        label = "Cloud Cover (%)"

    elif parameter == "Humidity":
        column = "relative_humidity_max"
        label = "Humidity (%)"

    elif parameter == "Pressure":
        column = "surface_pressure_max"
        label = "Pressure (hPa)"

    elif parameter == "Wind Speed":
        column = "wind_speed_max"
        label = "Wind Speed (m/s)"

    else:
        column = "precipitation_sum"
        label = "Precipitation (mm)"

    try:
        cursor.execute(
            "SELECT date, " + column +
            " FROM historical_data "
            "WHERE LOWER(city) = LOWER(%s) "
            "ORDER BY date",
            (city,)
        )

        rows = cursor.fetchall()

        dates = []
        values = []

        for row in rows:
            if row[0] is not None and row[1] is not None:
                dates.append(str(row[0]))
                values.append(row[1])

        if len(dates) < 2:
            messagebox.showinfo(
                "Not Enough Data",
                "At least two historical records are required for "
                + city + "."
            )
            return

        plt.figure(figsize=(9, 4.5))
        plt.plot(dates, values, marker="o", linestyle="-")

        plt.xlabel("Date")
        plt.ylabel(label)
        plt.title(parameter + " History - " + city)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))


tk.Button(
    graph_frame,
    text="Generate Line Graph",
    font=("Arial", 10),
    width=22,
    command=create_graph
).pack(pady=6)

tk.Button(
    graph_frame,
    text="Back",
    font=("Arial", 10),
    width=22,
    command=back
).pack(pady=3)


def forecast_page():
    show_page(forecast_frame)


tk.Label(
    forecast_frame,
    text="Weather Forecast",
    font=("Arial", 14, "bold")
).pack(pady=8)

tk.Label(
    forecast_frame,
    text="City name:",
    font=("Arial", 10)
).pack()

forecast_city = tk.Entry(forecast_frame, width=25, font=("Arial", 10))
forecast_city.pack(pady=4)

tk.Label(
    forecast_frame,
    text="Date (YYYY-MM-DD):",
    font=("Arial", 10)
).pack()

forecast_date = tk.Entry(forecast_frame, width=25, font=("Arial", 10))
forecast_date.pack(pady=4)

forecast_result = tk.Label(
    forecast_frame,
    text="",
    justify="left",
    wraplength=550,
    font=("Arial", 10)
)
forecast_result.pack(pady=8)


def get_forecast():
    city = forecast_city.get().strip()
    chosen_date = forecast_date.get().strip()

    if city == "" or chosen_date == "":
        messagebox.showerror(
            "Missing Information",
            "Enter both the city and the date."
        )
        return

    parts = chosen_date.split("-")

    if (
        len(parts) != 3
        or len(parts[0]) != 4
        or len(parts[1]) != 2
        or len(parts[2]) != 2
        or not (
            parts[0].isdigit()
            and parts[1].isdigit()
            and parts[2].isdigit()
        )
    ):
        messagebox.showerror(
            "Invalid Date",
            "Use YYYY-MM-DD, for example 2026-10-20."
        )
        return

    location = get_coordinates(city)

    if location is None:
        messagebox.showerror(
            "City Not Found",
            "This city is not in your city_coords table."
        )
        return

    latitude = location[0]
    longitude = location[1]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "precipitation_sum,precipitation_probability_max,"
            "weather_code,wind_speed_10m_max"
        ),
        "forecast_days": 16,
        "wind_speed_unit": "ms",
        "timezone": "Asia/Kolkata"
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            messagebox.showerror(
                "Forecast Error",
                "Open-Meteo could not return the forecast."
            )
            return

        data = response.json()
        daily = data["daily"]

        if chosen_date not in daily["time"]:
            messagebox.showinfo(
                "Date Unavailable",
                "Choose a date in the available forecast period."
            )
            return

        position = daily["time"].index(chosen_date)

        temp_max = daily["temperature_2m_max"][position]
        temp_min = daily["temperature_2m_min"][position]
        rain = daily["precipitation_sum"][position]
        rain_probability = daily["precipitation_probability_max"][position]
        wind = daily["wind_speed_10m_max"][position]
        code = daily["weather_code"][position]

        condition = get_condition(code)

        info = (
            "City: " + city.title() + "\n"
            "Date: " + chosen_date + "\n"
            "Condition: " + condition + "\n"
            "Maximum temperature: " + str(temp_max) + " °C\n"
            "Minimum temperature: " + str(temp_min) + " °C\n"
            "Precipitation: " + str(rain) + " mm\n"
            "Precipitation probability: " + str(rain_probability) + " %\n"
            "Maximum wind speed: " + str(wind) + " m/s"
        )

        warnings = []

        if temp_max is not None and temp_max >= 40:
            warnings.append((
                "Maximum temperature", temp_max, 40,
                "Very high temperature forecast."
            ))

        if temp_min is not None and temp_min <= 5:
            warnings.append((
                "Minimum temperature", temp_min, 5,
                "Very low temperature forecast."
            ))

        if rain is not None and rain >= 50:
            warnings.append((
                "Precipitation", rain, 50,
                "Heavy daily precipitation forecast."
            ))

        if rain_probability is not None and rain_probability >= 70:
            warnings.append((
                "Precipitation probability", rain_probability, 70,
                "High probability of precipitation."
            ))

        if wind is not None and wind >= 15:
            warnings.append((
                "Maximum wind speed", wind, 15,
                "High wind speed forecast."
            ))

        for alert in warnings:
            cursor.execute("""
                INSERT INTO alerts
                    (city, forecast_date, parameter,
                     value, threshold_value, message)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                city.title(),
                chosen_date,
                alert[0],
                alert[1],
                alert[2],
                alert[3]
            ))

        conn.commit()

        if warnings:
            info = info + "\n\nWEATHER WARNINGS:\n"

            for alert in warnings:
                info = info + "WARNING: " + alert[3] + "\n"
        else:
            info = info + "\n\nNo configured warning thresholds were reached."

        forecast_result.config(text=info)

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Connection Error",
            "Could not connect to Open-Meteo."
        )

    except mysql.connector.Error as error:
        conn.rollback()
        messagebox.showerror("Database Error", str(error))

    except Exception as error:
        messagebox.showerror("Error", str(error))


tk.Button(
    forecast_frame,
    text="Get Forecast",
    font=("Arial", 10),
    width=22,
    command=get_forecast
).pack(pady=6)

tk.Button(
    forecast_frame,
    text="Back",
    font=("Arial", 10),
    width=22,
    command=back
).pack(pady=3)

def reports_page():
    show_page(report_frame)

    report_list.delete(0, tk.END)
    report_location.config(
        text="Select a filename to see its saved location."
    )

    try:
        cursor.execute("""
            SELECT file_name
            FROM weekly_report_files
            ORDER BY start_date DESC
        """)

        rows = cursor.fetchall()

        for row in rows:
            report_list.insert(tk.END, row[0])

        if not rows:
            report_location.config(
                text="No reports found. Run report.py first."
            )

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))


def show_report_location(event):
    selection = report_list.curselection()

    if not selection:
        return

    selected_name = report_list.get(selection[0])

    cursor.execute("""
        SELECT file_path
        FROM weekly_report_files
        WHERE file_name = %s
        LIMIT 1
    """, (selected_name,))

    row = cursor.fetchone()

    if row:
        report_location.config(
            text="Filename: " + selected_name +
                 "\n\nFile location:\n" + row[0]
        )


tk.Label(
    report_frame,
    text="Weekly Reports",
    font=("Arial", 14, "bold")
).pack(pady=8)

tk.Label(
    report_frame,
    text="Click a filename to see its saved location.",
    font=("Arial", 10)
).pack(pady=4)

report_list = tk.Listbox(
    report_frame,
    width=55,
    height=10,
    font=("Arial", 10)
)

report_list.pack(
    pady=5,
    fill="both",
    expand=True
)

report_list.bind("<<ListboxSelect>>", show_report_location)

report_location = tk.Label(
    report_frame,
    text="",
    wraplength=550,
    justify="left",
    font=("Arial", 10)
)
report_location.pack(pady=6)

tk.Button(
    report_frame,
    text="Refresh Reports",
    font=("Arial", 10),
    width=22,
    command=reports_page
).pack(pady=3)

tk.Button(
    report_frame,
    text="Back",
    font=("Arial", 10),
    width=22,
    command=back
).pack(pady=3)

def database_statistics():
    tables = [
        "search_history",
        "weather_data",
        "forecast",
        "weekly_report_files",
        "historical_data",
        "alerts",
        "city_coords"
    ]

    info = "DATABASE STATISTICS\\n\\n"

    for table in tables:
        try:
            cursor.execute("SELECT COUNT(*) FROM " + table)
            row = cursor.fetchone()
            info = info + table + ": " + str(row[0]) + " records\\n"
        except mysql.connector.Error:
            conn.rollback()
            info = info + table + ": table not found or unavailable\\n"

    messagebox.showinfo("Database Statistics", info)

tk.Button(
    main_frame,
    text="Get Weather",
    font=("Arial", 10),
    width=22,
    command=fetch
).pack(pady=3)

tk.Button(
    main_frame,
    text="Show Search History",
    font=("Arial", 10),
    width=22,
    command=search_history
).pack(pady=3)

tk.Button(
    main_frame,
    text="Historical Line Graph",
    font=("Arial", 10),
    width=22,
    command=correlation_graph
).pack(pady=3)

tk.Button(
    main_frame,
    text="Forecast",
    font=("Arial", 10),
    width=22,
    command=forecast_page
).pack(pady=3)

tk.Button(
    main_frame,
    text="Reports",
    font=("Arial", 10),
    width=22,
    command=reports_page
).pack(pady=3)

exit_button = tk.Button(
    main_frame,
    text="Exit",
    font=("Arial", 10),
    width=22,
    command=window.destroy
)
exit_button.pack(pady=3)

admin_stats_button = tk.Button(
    main_frame,
    text="Database Statistics",
    font=("Arial", 10),
    width=22,
    command=database_statistics
)



show_page(role_frame)
window.mainloop()

cursor.close()
conn.close()

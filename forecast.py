
import requests
import mysql.connector

conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="K3nilaniganesh:)",
        database="weather"
    )
cursor = conn.cursor()
cursor.execute("""drop table if exists forecast""")

def update_forecasts():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast (
            id INT PRIMARY KEY AUTO_INCREMENT,
            city VARCHAR(100),
            date DATE,
            temp_max FLOAT,
            temp_min FLOAT,
            precipitation_sum FLOAT,
            precipitation_probability INT,
            weather_code INT,
            UNIQUE (city, date)
        )
    """)
    conn.commit()

    cursor.execute("""
        SELECT city, latitude, longitude
        FROM city_coords
    """)
    cities = cursor.fetchall()

    success = 0
    failed = []

    for city_data in cities:
        city = city_data[0]
        lat = city_data[1]
        lon = city_data[2]

        url = "https://api.open-meteo.com/v1/forecast"

        parameters = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "weather_code"
            ],
            "forecast_days": 15,
            "timezone": "Asia/Kolkata"
        }

        try:
            response = requests.get(
                url, params=parameters, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            daily = data["daily"]

            dates = daily["time"]
            temp_max = daily["temperature_2m_max"]
            temp_min = daily["temperature_2m_min"]
            rain = daily["precipitation_sum"]
            rain_probability = daily["precipitation_probability_max"]
            weather = daily["weather_code"]

            for i in range(len(dates)):
                cursor.execute("""
                    INSERT INTO forecast
                    (city, date, temp_max, temp_min,
                     precipitation_sum, precipitation_probability,
                     weather_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        temp_max = VALUES(temp_max),
                        temp_min = VALUES(temp_min),
                        precipitation_sum = VALUES(precipitation_sum),
                        precipitation_probability = VALUES(precipitation_probability),
                        weather_code = VALUES(weather_code)
                """, (
                    city, dates[i], temp_max[i], temp_min[i],
                    rain[i], rain_probability[i], weather[i]
                ))

            conn.commit()
            success += 1
            print("Forecast updated for:", city)

        except (requests.RequestException,
                mysql.connector.Error, KeyError) as e:
            conn.rollback()
            print("Error for", city, ":", e)
            failed.append(city)

    print("Forecast update completed.")

    print("Cities updated:", success)
    print("Cities failed:", failed)

    cursor.close()
    conn.close()


update_forecasts()


import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="K3nilaniganesh:)",
    database="weather_data"
)

cursor = conn.cursor()

# Create the database table for report records
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weekly_report_files (
        id INT PRIMARY KEY AUTO_INCREMENT,
        file_name VARCHAR(255),
        start_date DATE,
        end_date DATE,
        file_path VARCHAR(500),
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (start_date, end_date)
    )
""")

conn.commit()

# Find the first and last dates in historical data
cursor.execute("""
    SELECT MIN(date), MAX(date)
    FROM historical_data
""")

dates = cursor.fetchone()

if dates[0] is None:
    print("No historical data available.")

else:
    period_start = dates[0]
    latest_date = dates[1]

    period_start = str(period_start)
    latest_date = str(latest_date)

    # Repeat until all dates have been covered
    while period_start <= latest_date:

        # Find the end date of this 7-day period
        cursor.execute("""
            SELECT LEAST(
                DATE_ADD(%s, INTERVAL 6 DAY),
                %s
            )
        """, (period_start, latest_date))

        period_end = cursor.fetchone()[0]

        start_date = str(period_start)
        end_date = str(period_end)

        # Create the report filename
        file_name = "weekly_report_" + start_date + "_to_" + end_date + ".txt"

        # Find the folder containing this Python script
        script_path = __file__

        folder_path = "\\".join(script_path.split("\\")[:-1])

        if folder_path == "":
            file_path = file_name
        else:
            file_path = folder_path + "\\" + file_name

        # Get weather statistics for every city
        cursor.execute("""
            SELECT
                c.city,
                COUNT(h.date),
                MAX(h.temp_max),
                MIN(h.temp_min),
                MAX(h.surface_pressure_max),
                MIN(h.surface_pressure_min),
                MAX(h.relative_humidity_max),
                MIN(h.relative_humidity_min),
                MAX(h.cloud_cover_max),
                MIN(h.cloud_cover_min),
                MAX(h.wind_speed_max),
                MIN(h.wind_speed_min),
                SUM(h.precipitation_sum)
            FROM city_coords c
            LEFT JOIN historical_data h
                ON c.city = h.city
                AND h.date BETWEEN %s AND %s
            GROUP BY c.city
            ORDER BY c.city
        """, (start_date, end_date))

        cities = cursor.fetchall()

        # Write the report file
        file = open(file_path, "w", encoding="utf-8")

        file.write("WEEKLY WEATHER REPORT\n")
        file.write("=" * 50 + "\n")
        file.write("Period: " + start_date + " - " + end_date + "\n")
        file.write("=" * 50 + "\n\n")

        for city in cities:
            file.write("CITY: " + city[0] + "\n")
            file.write("-" * 40 + "\n")

            if city[1] == 0:
                file.write("No historical data available for this period.\n\n")
            else:
                file.write("Days of data: " + str(city[1]) + "\n")
                file.write("Maximum temperature: " + str(city[2]) + " °C\n")
                file.write("Minimum temperature: " + str(city[3]) + " °C\n")
                file.write("Maximum pressure: " + str(city[4]) + " hPa\n")
                file.write("Minimum pressure: " + str(city[5]) + " hPa\n")
                file.write("Maximum humidity: " + str(city[6]) + " %\n")
                file.write("Minimum humidity: " + str(city[7]) + " %\n")
                file.write("Maximum cloud cover: " + str(city[8]) + " %\n")
                file.write("Minimum cloud cover: " + str(city[9]) + " %\n")
                file.write("Maximum wind speed: " + str(city[10]) + " m/s\n")
                file.write("Minimum wind speed: " + str(city[11]) + " m/s\n")
                file.write("Total precipitation: " + str(city[12]) + " mm\n\n")

        file.close()

        # Save the report details in MySQL
        cursor.execute("""
            INSERT INTO weekly_report_files
                (file_name, start_date, end_date, file_path)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                file_name = VALUES(file_name),
                file_path = VALUES(file_path),
                generated_at = CURRENT_TIMESTAMP
        """, (file_name, start_date, end_date, file_path))

        conn.commit()

        print("Report created:", file_name)
        print("Period:", start_date, "to", end_date)
        print("Full file location:", file_path)
        print("Cities included:", len(cities))
        print("-----------------------------------")

        # Move to the next 7-day period
        cursor.execute("""
            SELECT DATE_ADD(%s, INTERVAL 1 DAY)
        """, (period_end,))

        period_start = cursor.fetchone()[0]

    print("All reports generated successfully!")

cursor.close()
conn.close()

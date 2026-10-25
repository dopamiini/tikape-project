import csv
import sqlite3
from pathlib import Path

csv_files = [Path("csv") / f"2023-{m:02d}.csv" for m in range(4, 11)]

for file in csv_files:
    if not file.exists():
        raise FileNotFoundError(file)

connection = sqlite3.connect("bikes_2023.db")

connection.executescript("""
    DROP TABLE IF EXISTS Trips;
    DROP TABLE IF EXISTS Stations;

    CREATE TABLE Stations (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE Trips (
        id INTEGER PRIMARY KEY,
        start_time TEXT,
        end_time TEXT,
        start_station_id INTEGER REFERENCES Stations,
        end_station_id INTEGER REFERENCES Stations,
        distance INTEGER,
        duration INTEGER
    );"""
)

trip_sql = """INSERT INTO Trips
              (start_time, end_time, start_station_id, end_station_id, distance, duration)
              VALUES (?, ?, ?, ?, ?, ?)"""

stations = {}
trips = []

try:
    for file in csv_files:
        with open(file, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if (
                    not row["Covered distance (m)"].strip() 
                    or not row["Duration (sec.)"].strip()
                ):
                    continue

                start_id = int(row["Departure station id"])
                end_id = int(row["Return station id"])

                stations.setdefault(start_id, row["Departure station name"])
                stations.setdefault(end_id, row["Return station name"])

                trips.append((
                    row["Departure"], row["Return"], start_id, end_id,
                    int(float(row["Covered distance (m)"])),
                    int(float(row["Duration (sec.)"]))
                ))

                if len(trips) >= 10000:
                    connection.executemany(trip_sql, trips)
                    trips.clear()

    connection.executemany(trip_sql, trips)
    connection.executemany(
        "INSERT INTO Stations VALUES (?, ?)", stations.items()
    )
    connection.commit()

    for table in ("Stations", "Trips"):
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]
        print(f"{table}: {count}")

    print("Station 100:", connection.execute(
        "SELECT * FROM Stations WHERE id = 100"
    ).fetchone())

    print("Trip 123456:", connection.execute(
        "SELECT * FROM Trips WHERE id = 123456"
    ).fetchone())

finally:
    connection.close()

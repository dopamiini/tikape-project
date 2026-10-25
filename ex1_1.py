import sqlite3
import sys


db = sqlite3.connect("bikes_2024.db")


def trips_from_station(station_name):
    sql = """SELECT COUNT(*)
             FROM Trips AS T
             JOIN Stations AS S ON T.start_station_id = S.id
             WHERE S.name = ?"""
    result = db.execute(sql, [station_name])
    return result.fetchone()[0]


def trips_to_station(station_name):
    sql = """SELECT COUNT(*)
             FROM Trips AS T
             JOIN Stations AS S ON T.end_station_id = S.id
             WHERE S.name = ?"""
    result = db.execute(sql, [station_name])
    return result.fetchone()[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <station_name>")
        sys.exit(1)

    station_name = sys.argv[1]

    print(f"Asemalta {station_name} alkaneiden matkojen määrä on: "
          f"{trips_from_station(station_name)}")

    print(f"Asemalle {station_name} päättyneiden matkojen määrä on: "
          f"{trips_to_station(station_name)}")

    db.close()

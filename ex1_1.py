import sqlite3
import sys


def get_connection():
    return sqlite3.connect("bikes_2024.db")


def query(sql, params=()):
    con = get_connection()
    try:
        return con.execute(sql, params).fetchone()
    finally:
        con.close()


def trips_from_station(station_name):
    return query("""
        SELECT COUNT(*)
        FROM Trips AS T
        JOIN Stations AS S ON T.start_station_id = S.id
        WHERE S.name = ?
    """, (station_name,))[0]


def trips_to_station(station_name):
    return query("""
        SELECT COUNT(*)
        FROM Trips AS T
        JOIN Stations AS S ON T.end_station_id = S.id
        WHERE S.name = ?
    """, (station_name,))[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <station_name>")
        sys.exit(1)

    station_name = sys.argv[1]

    print(f"The number of trips starting at {station_name} is: "
          f"{trips_from_station(station_name)}")

    print(f"The number of trips ending at {station_name} is: "
          f"{trips_to_station(station_name)}")

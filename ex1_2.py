import sqlite3
import sys


db = sqlite3.connect("bikes_2024.db")


def longest_distance_trips(limit):
    sql = """SELECT S1.name, S2.name, T.distance
             FROM Trips AS T
             JOIN Stations AS S1 ON T.start_station_id = S1.id
             JOIN Stations AS S2 ON T.end_station_id = S2.id
             ORDER BY T.distance DESC
             LIMIT ?"""
    result = db.execute(sql, [limit])
    return result.fetchall()


def longest_duration_trips(limit):
    sql = """SELECT S1.name, S2.name, T.duration
             FROM Trips AS T
             JOIN Stations AS S1 ON T.start_station_id = S1.id
             JOIN Stations AS S2 ON T.end_station_id = S2.id
             ORDER BY T.duration DESC
             LIMIT ?"""
    result = db.execute(sql, [limit])
    return result.fetchall()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ex1_2.py <limit>")
        sys.exit(1)

    limit = int(sys.argv[1])

    print("Pisin matkaetäisyys on seuraavilla matkoilla:")
    for start_station, end_station, distance in longest_distance_trips(limit):
        print(f"{start_station:<25} => {end_station:<25} = {distance} m")

    print("\nPisin kestoiset matkat ovat:")
    for start_station, end_station, duration in longest_duration_trips(limit):
        print(f"{start_station:<25} => {end_station:<25} = {duration} s")

    db.close()

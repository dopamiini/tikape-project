
import sqlite3
import sys


db = sqlite3.connect("bikes_2024.db")


def most_popular_start_stations(limit):
    sql = """SELECT S.name, COUNT(*) AS departures
             FROM Trips AS T
             JOIN Stations AS S ON T.start_station_id = S.id
             GROUP BY S.id
             ORDER BY departures DESC
             LIMIT ?"""
    result = db.execute(sql, [limit])
    return result.fetchall()


def least_popular_start_stations(limit):
    sql = """SELECT S.name, COUNT(*) AS departures
             FROM Trips AS T
             JOIN Stations AS S ON T.start_station_id = S.id
             GROUP BY S.id
             ORDER BY departures ASC
             LIMIT ?"""
    result = db.execute(sql, [limit])
    return result.fetchall()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ex1_4.py <limit>")
        sys.exit(1)

    limit = int(sys.argv[1])

    print("Suosituimmat lähtöasemat ovat:")
    for value in most_popular_start_stations(limit):
        print(f"{value[0]}: {value[1]}")

    print("\nVähiten suositut lähtöasemat ovat:")
    for value in least_popular_start_stations(limit):
        print(f"{value[0]}: {value[1]}")

    db.close()

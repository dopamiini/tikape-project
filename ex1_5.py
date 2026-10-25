
import sqlite3
import sys


db = sqlite3.connect("bikes_2024.db")


def largest_differences(limit):
    sql = """WITH departures AS (
                 SELECT start_station_id, COUNT(*) AS starting
                 FROM Trips
                 GROUP BY start_station_id
             ),
             arrivals AS (
                 SELECT end_station_id, COUNT(*) AS ending
                 FROM Trips
                 GROUP BY end_station_id
             )
             SELECT S.name,
                    IFNULL(D.starting, 0),
                    IFNULL(A.ending, 0),
                    ABS(IFNULL(D.starting, 0) -
                        IFNULL(A.ending, 0)) AS difference
             FROM Stations AS S
             LEFT JOIN departures AS D ON S.id = D.start_station_id
             LEFT JOIN arrivals AS A ON S.id = A.end_station_id
             ORDER BY difference DESC
             LIMIT ?"""
    result = db.execute(sql, [limit])
    return result.fetchall()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ex1_5.py <limit>")
        sys.exit(1)

    limit = int(sys.argv[1])

    print("Suurimmat erot alkaneiden ja päättyneiden matkojen määrässä:")
    print(
        f"{'Asema':<30} {'Alkaneet matkat':>15} "
        f"{'Päättyneet matkat':>18} {'Määrien ero':>12}"
    )

    for value in largest_differences(limit):
        print(f"{value[0]:<30} {value[1]:>15} {value[2]:>18} {value[3]:>12}")

    db.close()


import sqlite3
import sys


db = sqlite3.connect("bikes_2024.db")


months = [
    "Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu",
    "Toukokuu", "Kesäkuu", "Heinäkuu", "Elokuu",
    "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"
]

weekdays = [
    "Maanantai", "Tiistai", "Keskiviikko", "Torstai",
    "Perjantai", "Lauantai", "Sunnuntai"
]


def trips_during_month(month):
    sql = """SELECT COUNT(*)
             FROM Trips
             WHERE CAST(strftime('%m', start_time) AS INTEGER) = ?"""
    result = db.execute(sql, [month])
    return result.fetchone()[0]


def trips_during_weekday(day):
    sql = """SELECT COUNT(*)
             FROM Trips
             WHERE (CAST(strftime('%w', start_time) AS INTEGER) + 6) % 7 + 1 = ?"""
    result = db.execute(sql, [day])
    return result.fetchone()[0]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ex1_3.py <month> <weekday>")
        sys.exit(1)

    month = (int(sys.argv[1]) - 1) % 12 + 1
    day = (int(sys.argv[2]) - 1) % 7 + 1

    print(f"{months[month - 1]}n matkojen määrä on: "
          f"{trips_during_month(month)}")

    print(f"{weekdays[day - 1]}n matkojen määrä on: "
          f"{trips_during_weekday(day)}")

    db.close()

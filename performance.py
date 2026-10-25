import sqlite3
import random
import string
import time
import os


def create_movies(db):
    db.execute("DROP TABLE IF EXISTS Movies")
    db.execute("""CREATE TABLE Movies (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      release_year INTEGER)""")


def insert_movies(db):
    movies = []

    for _ in range(1000000):
        title = "".join(random.choices(string.ascii_letters, k=8))
        year = random.randint(1900, 2000)
        movies.append((title, year))

    start = time.perf_counter()

    db.execute("BEGIN")
    db.executemany(
        "INSERT INTO Movies (name, release_year) VALUES (?, ?)", movies
    )
    db.execute("COMMIT")

    return time.perf_counter() - start


def query_movies(db):
    years = [random.randint(1900, 2000) for _ in range(1000)]

    start = time.perf_counter()

    for year in years:
        db.execute(
            "SELECT COUNT(*) FROM Movies WHERE release_year = ?", (year,)
        ).fetchone()

    return time.perf_counter() - start


def test_without_index():
    filename = "movies1.db"
    db = sqlite3.connect(filename)
    create_movies(db)
    insert_time = insert_movies(db)
    query_time = query_movies(db)
    db.close()
    size = os.path.getsize(filename)

    return insert_time, query_time, size


def test_with_index_before_insert():
    filename = "movies2.db"
    db = sqlite3.connect(filename)
    create_movies(db)
    db.execute(
        "CREATE INDEX idx_release_year ON Movies(release_year)"
    )
    insert_time = insert_movies(db)
    query_time = query_movies(db)
    db.close()
    size = os.path.getsize(filename)

    return insert_time, query_time, size


def test_with_index_before_queries():
    filename = "movies3.db"
    db = sqlite3.connect(filename)
    create_movies(db)
    insert_time = insert_movies(db)
    db.execute(
        "CREATE INDEX idx_release_year ON Movies(release_year)"
    )
    query_time = query_movies(db)
    db.close()
    size = os.path.getsize(filename)

    return insert_time, query_time, size


if __name__ == "__main__":
    results = []

    results.append(("Ei indeksiä", test_without_index()))
    results.append(("Indeksi ennen lisäystä", test_with_index_before_insert()))
    results.append(("Indeksi ennen kyselyitä", test_with_index_before_queries()))

    for name, (insert_time, query_time, size) in results:
        print(f"{name}:")
        print(f"Rivien lisäys: {insert_time:.3f} s")
        print(f"Kyselyt:       {query_time:.3f} s")

    for name, (insert_time, query_time, size) in results:
        print(f"{name}: {size / 1000000:.2f} MB")

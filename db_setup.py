from database.db_config import get_connection
import pandas as pd

def create_IMDB_table():
    cnx = cur = None
    try:
        # ---- 1. Connect to MySQL ----
        cnx = get_connection()
        cur = cnx.cursor()

        # ---- 2. Create database and use it ----
        cur.execute("CREATE DATABASE IF NOT EXISTS scraped_data")
        cur.execute("USE scraped_data")

        # ---- 3. Create table ----
        cur.execute("""
            CREATE TABLE IF NOT EXISTS IMDB_table (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                movie_name VARCHAR(200),
                genre VARCHAR(100),
                rating FLOAT NULL,
                vote_count INT NULL,
                duration INT NULL   -- store in minutes (safer than TIME)
            )ENGINE=InnoDB ROW_FORMAT=DYNAMIC
        """)

        # ---- 4. Read CSV ----
        dataframe = pd.read_csv("imdb_cleaned.csv")

        # ---- 5. Prepare tuples ----
        data_tuples = [
            (
                row.movie_name,
                row.genre.title() if pd.notna(row.genre) else None,
                float(row.rating) if pd.notna(row.rating) else None,
                int(row.vote_count) if pd.notna(row.vote_count) else None,
                int(row.duration) if pd.notna(row.duration) else None
            )
            for row in dataframe.itertuples(index=False)
        ]

        # ---- 6. Insert ----
        insert_query = """
            INSERT INTO IMDB_table (movie_name, genre, rating, vote_count, duration)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.executemany(insert_query, data_tuples)
        cnx.commit()
        print(" Database and table are ready, and data inserted successfully!")

    except Exception as e:
        print(f" Error: {e}")
    finally:
        if cur: cur.close()
        if cnx: cnx.close()

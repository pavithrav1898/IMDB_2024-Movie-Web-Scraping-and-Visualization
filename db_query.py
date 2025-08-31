from database.db_config import get_connection
import pandas as pd

def get_filter_values():
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    filters = {}

    # Fetch unique genres
    cur.execute("SELECT DISTINCT genre FROM IMDB_table ORDER BY genre;")
    filters['genres'] = [row['genre'] for row in cur.fetchall()]

    # Fetch min and max for numeric filters
    cur.execute("""
        SELECT MIN(rating) AS min_rating, MAX(rating) AS max_rating,
               MIN(vote_count) AS min_votes, MAX(vote_count) AS max_votes,
               MIN(TIME_TO_SEC(duration)/3600) AS min_duration,
               MAX(TIME_TO_SEC(duration)/3600) AS max_duration
        FROM IMDB_table;
    """)
    row = cur.fetchone()
    filters['rating'] = {'min': row['min_rating'], 'max': row['max_rating']}
    filters['vote_count'] = {'min': row['min_votes'], 'max': row['max_votes']}
    filters['duration'] = {'min': row['min_duration'], 'max': row['max_duration']}

    print(filters)
    cur.close()
    cnx.close()
    return filters

def fetch_filtered_data(
    selected_genres=None,
    rating_range=None,
    vote_count_range=None,
    duration_range=None
):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    query = """
        SELECT movie_name, genre, rating, vote_count, duration, CONCAT(HOUR(duration), 'h ', MINUTE(duration), 'm') AS duration_hm
        FROM IMDB_table
        WHERE 1=1
    """
    params = []

    # --- Genre filter ---
    if selected_genres:
        placeholders = ', '.join(['%s'] * len(selected_genres))
        query += f" AND genre IN ({placeholders})"
        params.extend(selected_genres)

    # --- Rating filter ---
    if rating_range:
        if rating_range.get('min') is not None and rating_range.get('max') is not None:
            query += " AND rating BETWEEN %s AND %s"
            params.extend([rating_range['min'], rating_range['max']])
        elif rating_range.get('min') is not None:
            query += " AND rating >= %s"
            params.append(rating_range['min'])
        elif rating_range.get('max') is not None:
            query += " AND rating <= %s"
            params.append(rating_range['max'])

    # --- Vote count filter ---
    if vote_count_range:
        if vote_count_range.get('min') is not None and vote_count_range.get('max') is not None:
            query += " AND vote_count BETWEEN %s AND %s"
            params.extend([vote_count_range['min'], vote_count_range['max']])
        elif vote_count_range.get('min') is not None:
            query += " AND vote_count >= %s"
            params.append(vote_count_range['min'])
        elif vote_count_range.get('max') is not None:
            query += " AND vote_count <= %s"
            params.append(vote_count_range['max'])

    # --- Duration filter ---
    if duration_range:
        if duration_range.get('min') is not None and duration_range.get('max') is not None:
            query += " AND TIME_TO_SEC(duration)/3600 BETWEEN %s AND %s"
            params.extend([duration_range['min'], duration_range['max']])
        elif duration_range.get('min') is not None:
            query += " AND TIME_TO_SEC(duration)/3600 >= %s"
            params.append(duration_range['min'])
        elif duration_range.get('max') is not None:
            query += " AND TIME_TO_SEC(duration)/3600 <= %s"
            params.append(duration_range['max'])

    cur.execute(query, params)
    #print("Query:", query)
    #print("Params:", params)

    results = cur.fetchall()
    filter_output = pd.DataFrame(results)
    cur.close()
    cnx.close()

    return filter_output









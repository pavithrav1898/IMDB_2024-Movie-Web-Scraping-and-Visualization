from scraper import web_scrap
from eda import eda
from database.db_config import get_connection
from database.db_setup import create_IMDB_table
from database.db_query import get_filter_values, fetch_filtered_data
#from movie_dashboard import visualization


def main():
    print("🔎 Starting pipeline...")

    web_scrap()
    print("Scraping complete")

    eda()
    print("EDA complete, imdb_cleaned.csv ready")

    create_IMDB_table()
    print("Data inserted into MySQL")

    filters = get_filter_values()
    print("Available filters:", filters)

    data = fetch_filtered_data()
    print("Fetched rows:", len(data))

    # 5. Dashboard (optional)
    # visualization()

if __name__ == "__main__":
    main()


import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from database.db_query import get_filter_values, fetch_filtered_data
import pandas as pd

def visualization():
    st.set_page_config(
        page_title="IMDb Movie Analytics Dashboard",
        page_icon="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
    /*Background Color*/
        html, body, [class*="stApp"] {
            background-color: white !important;            
        }
        div.block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 2rem;
        }
    /* Text colors */
        h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown, .css-10trblm {
            color: black !important;
        }
    /* Sidebar colors*/
        section[data-testid="stSidebar"]{
            background-color: white !important;
            border-right: 2px solid #ddd;   /* light gray line */
        }
    /* Button Color */
       section[data-testid="stSidebar"] div.stButton > button {
            background-color: #f97316 !important;
        }
    /* Metric box border */
        div[data-testid="stMetric"] {
            border: 2px solid #ddd;   /* border color */
            border-radius: 10px;
            padding: 10px;
        }        
    /* Metric value */
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #f97316 !important;  /* orange */
            font-size: 20px !important;
            font-weight: bold !important;
        }
    </style>
    """,unsafe_allow_html=True)
    logo_col, title_col = st.columns([1, 10])
    with logo_col:
        st.markdown(
            """
            <div style="margin-top:20px; margin-left:20px">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" width="80">
            </div>
            """,
            unsafe_allow_html=True
        )
    with title_col:
        st.header("IMDb 2024 Movie Analytics Dashboard")
    st.sidebar.header("Filter Data")

    # Load Filters
    filters = get_filter_values()

    # --- Genre ---
    st.sidebar.subheader("Genre")
    selected_genres = st.sidebar.multiselect("Select Genres", filters['genres'])

    # --- Rating Filter ---
    st.sidebar.subheader("Ratings")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        min_rating_in = st.text_input("Min", value="", placeholder="eg.2", label_visibility="collapsed")
        min_rating = float(min_rating_in) if min_rating_in.strip() != "" else None
        if min_rating is not None and not (filters['rating']['min'] <= min_rating <= filters['rating']['max']):
            st.markdown(f"<span style='color:red'> error </span>", unsafe_allow_html=True)

    with col2:
        max_rating_in = st.text_input("Max", value="", placeholder="eg.10", label_visibility="collapsed")
        max_rating = float(max_rating_in) if max_rating_in.strip() != "" else None
        if max_rating is not None and not (filters['rating']['min'] <= max_rating <= filters['rating']['max']):
            st.markdown(f"<span style='color:red'></span>", unsafe_allow_html=True)

    # --- Vote Count Filter ---
    st.sidebar.subheader("Vote Count")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        min_votes_in = st.text_input("Min votes", value="", placeholder="eg.100", label_visibility="collapsed")
        min_votes = int(min_votes_in) if min_votes_in.strip() != "" else None
        if min_votes is not None and not (filters['vote_count']['min'] <= min_votes <= filters['vote_count']['max']):
            st.markdown(f"<span style='color:red'></span>", unsafe_allow_html=True)

    with col2:
        max_votes_in = st.text_input("Max votes", value="", placeholder="eg.10000", label_visibility="collapsed")
        max_votes = int(max_votes_in) if max_votes_in.strip() != "" else None
        if max_votes is not None and not (filters['vote_count']['min'] <= max_votes <= filters['vote_count']['max']):
            st.markdown(f"<span style='color:red'></span>", unsafe_allow_html=True)

    # --- Duration Filter (Hours) ---
    st.sidebar.subheader("Run Time")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        min_duration_in = st.text_input("Min hours", value="", placeholder="eg.1h", label_visibility="collapsed")
        min_duration = int(min_duration_in) if min_duration_in.strip() != "" else None
        if min_duration is not None and not (filters['duration']['min'] <= min_duration <= filters['duration']['max']):
            st.markdown(f"<span style='color:red'></span>", unsafe_allow_html=True)

    with col2:
        max_duration_in = st.text_input("Max hours", value="", placeholder="eg.1h", label_visibility="collapsed")
        max_duration = int(max_duration_in) if max_duration_in.strip() != "" else None
        if max_duration is not None and not (filters['duration']['min'] <= max_duration <= filters['duration']['max']):
            st.markdown(f"<span style='color:red'></span>", unsafe_allow_html=True)

    # Apply filters and fetch data
    if st.sidebar.button("Apply Filters", ):

        #print("DEBUG - UI Filters:")
        #print("Genres:", selected_genres)
        #print("Ratings:", {"min": min_rating, "max": max_rating})
        #print("Votes:", {"min": min_votes, "max": max_votes})
        #print("Duration:", {"min": min_duration, "max": max_duration})

        data = fetch_filtered_data(
            selected_genres=selected_genres,
            rating_range={'min': min_rating, 'max': max_rating},
            vote_count_range={'min': min_votes, 'max': max_votes},
            duration_range={'min': min_duration, 'max': max_duration}
        )
        print(data)
    else:
        data = fetch_filtered_data()

    st.sidebar.header("Navigation")
    menu=st.sidebar.radio(
        "Go to",
        ["Dashboard","Data"], index=0
    )

    if menu=="Dashboard":
        if not data.empty:
            #shortest & longest movie
            def metric():
                col1, col2 = st.columns(2)
                data["duration"] = pd.to_timedelta(data["duration"])
                shortest_duration = data["duration"].min()
                shortest_row = \
                data.loc[data['duration'] == shortest_duration, ['movie_name', 'genre', 'duration_hm']].iloc[0]

                col1.metric(
                    label="Shortest Movie",
                    value=shortest_row['movie_name'],
                    delta=f"{shortest_row['duration_hm']} | {shortest_row['genre']}",
                    border=True,
                )

                longest_duration = data["duration"].max()
                longest_row = \
                data.loc[data['duration'] == longest_duration, ['movie_name', 'genre', 'duration_hm']].iloc[0]

                col2.metric(
                    label="Longest Movie",
                    value=longest_row['movie_name'],
                    delta=f"{longest_row['duration_hm']} | {longest_row['genre']}",
                    border=True
                )
            metric()

            #Top 10 Movies by Rating and Voting
            col3, col4= st.columns([1,1])
            # compute WR (Weighted Rating)
            m = data['vote_count'].quantile(0.80)  # threshold
            C = data['rating'].mean()
            data['weighted_rate'] = (
                    (data['vote_count'] / (data['vote_count'] + m)) * data['rating']
                    + (m / (data['vote_count'] + m)) * C
            )

            #filter + sort + take top 10
            top_movies_rating_voting = (
                data[data['vote_count'] >= m]
                .sort_values(by=['weighted_rate', 'vote_count'], ascending=[False, False])
                .head(10)
            )
            def movie_by_rating():
                with col3:
                    x = top_movies_rating_voting["movie_name"]
                    y = top_movies_rating_voting["rating"]
                    sizes = top_movies_rating_voting["rating"] *20 # bubble size scaled by rating
                    colors = top_movies_rating_voting["genre"].astype("category").cat.codes  # convert genre to numeric codes
                    fig, ax = plt.subplots(figsize=(6, 4), facecolor='none')  # transparent background
                    ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='nipy_spectral')
                    ax.set_xlabel("Movie",weight="bold")
                    ax.set_ylabel("Rating",weight="bold")
                    ax.set_title("Top 10 Movies by Rating", weight="bold")
                    plt.xticks(rotation=60, ha='right', fontsize=8)
                    st.pyplot(fig)
            movie_by_rating()

            def movie_by_vote_count():
                with col4:
                    top_movies_vote_count = data.sort_values(by='vote_count', ascending=False).head(10)
                    x = top_movies_rating_voting["movie_name"]
                    y = top_movies_rating_voting["vote_count"]
                    sizes = top_movies_rating_voting["vote_count"] /100  # bubble size scaled by rating
                    colors = top_movies_rating_voting["genre"].astype("category").cat.codes  # convert genre to numeric codes
                    fig, ax = plt.subplots(figsize=(6, 4), facecolor='none')  # transparent background
                    ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='nipy_spectral')
                    ax.set_xlabel("Movie", weight="bold")
                    ax.set_ylabel("Vote Count",weight="bold")
                    ax.set_title("Top 10 Movies by Vote Count", weight="bold")
                    plt.xticks(rotation=60, ha='right', fontsize=8)
                    st.pyplot(fig)
            movie_by_vote_count()

            col5, col6 = st.columns([1,1])
            def avg_duration_genre():
                with col5:
                    avg_duration = data.groupby('genre')['duration'].mean().sort_values()
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.barh(avg_duration.index, avg_duration.values, color="blue")
                    ax.set_xlabel("Average Duration (hm)", fontsize=12, weight="bold")
                    ax.set_ylabel("Genre", fontsize=12, weight="bold")
                    ax.set_title("Average Duration by Genre", weight="bold")
                    plt.tight_layout()
                    st.pyplot(fig, use_container_width=True)
            avg_duration_genre()

            def  voting_trend_genre():
                with col6:
                    avg_votes = data.groupby('genre')['vote_count'].mean().sort_values()
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.barh(avg_votes.index, avg_votes.values, color="green")
                    ax.set_xlabel("Average Vote Count", fontsize=12, weight="bold")
                    ax.set_ylabel("Genre", fontsize=12, weight="bold")
                    ax.set_title("Voting Trends by Genre", weight="bold")
                    ax.ticklabel_format(style='plain', axis='x')
                    plt.tight_layout()
                    st.pyplot(fig, use_container_width=True)
            voting_trend_genre()

            col7, col8 = st.columns([1, 1])
            def rating_distribution():
                with col7:
                    fig, ax = plt.subplots(figsize=(5, 3))
                    ax.hist(data['rating'], bins=20, color='purple', edgecolor='black', alpha=0.7)
                    ax.set_title("Distribution of Ratings", fontsize=10, weight="bold")
                    ax.set_xlabel("Rating", fontsize=8, weight="bold")
                    ax.set_ylabel("Movie Count", fontsize=8, weight="bold")
                    st.pyplot(fig)
            rating_distribution()

            def popular_genres_voting():
                with col8:
                    genre_votes = data.groupby('genre')['vote_count'].sum()
                    fig, ax = plt.subplots(figsize=(6, 6))
                    labels = [f"{genre} ({vote_count:,})" for genre, vote_count in genre_votes.items()]
                    ax.pie(
                        genre_votes,
                        labels=labels,
                        startangle=140,
                        autopct=lambda p: f"{p:.0f}%"
                    )
                    ax.set_title("Most Popular Genres by Voting", fontsize=14, weight="bold")
                    ax.axis("equal")
                    st.pyplot(fig)
            popular_genres_voting()

            col9, col10 = st.columns([1, 1])
            def ratings_genre():
                with col9:
                    avg_rating = data.groupby("genre")["rating"].mean().to_frame(name="Average Rating")
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.heatmap(
                        avg_rating,
                        annot=True,
                        cmap="coolwarm",
                        fmt=".1f",
                        linewidths=0.5,
                        ax=ax
                    )
                    ax.set_title("Ratings by Genre", fontsize=10, weight="bold")
                    st.pyplot(fig)
            ratings_genre()

            def correlation_analysis():
                with col10:
                    corr = data[['rating', 'vote_count']].corr()
                    fig, ax = plt.subplots(figsize=(4, 2))
                    sns.heatmap(
                        corr,
                        annot=True,  # show correlation values
                        cmap="coolwarm",  # color scheme
                        vmin=-1, vmax=1,  # fix scale
                        fmt=".2f",  # 2 decimal places
                        cbar=True,  # show colorbar
                        ax=ax
                    )
                    ax.set_title("Correlation Matrix", fontsize=10, weight="bold")
                    st.pyplot(fig)
            correlation_analysis()

            col11, col12 = st.columns([1, 1])
            def movie_count_genre():
                with col11:
                    genre_counts = data["genre"].value_counts().sort_values(ascending=False)
                    x = genre_counts.index
                    y = genre_counts.values
                    fig, ax = plt.subplots(figsize=(7, 4), facecolor='none')
                    ax.bar(x, y, color="orange")
                    ax.set_xlabel("Genre", weight="bold")
                    ax.set_ylabel("Count", weight="bold")
                    ax.set_title("Genre Distribution", weight="bold")
                    ax.tick_params(axis='x', rotation=45)  # rotate labels for readability
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
            movie_count_genre()

            def genre_rating_movies():
                with col12:
                    movies = data.loc[data.groupby('genre')['rating'].idxmax()][['genre', 'movie_name', 'rating']]
                    movies = movies.rename(columns={
                        "genre": "Genre",
                        "movie_name": "Movie Name",
                        "rating": "Rating"
                    })
                    movies = movies.reset_index(drop=True)
                    movies["Rating"] = movies["Rating"].round(1)
                    styled_movies = movies.style.set_properties(
                        **{
                            'background-color': 'white',
                            'color': 'black',
                            'border': '1px solid #ddd',
                            'padding': '8px'
                        }
                    ).set_table_styles(
                        [
                            {'selector': 'thead th', 'props': [('background-color', '#f2f2f2'),
                                                               ('color', 'black'),
                                                               ('font-weight', 'bold'),
                                                               ('text-align', 'center')
                                                               ]}
                        ]
                    )
                    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
                    st.table(styled_movies)
            genre_rating_movies()
        else:
            st.write("No Record Found for Applied Filter")

    elif menu=="Data":
        if data.empty:
            st.write("No Record Found for Applied Filter")
        else:
            st.dataframe(data, use_container_width=True, height=550)


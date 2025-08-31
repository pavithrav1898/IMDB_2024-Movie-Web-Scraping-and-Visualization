import pandas as pd
import numpy as np


def eda():
    csv_files = ["thriller.csv", "documentary.csv", "drama.csv", "comedy.csv", "horror.csv"]
    combine_data = [pd.read_csv(file) for file in csv_files]
    dataframe = pd.concat(combine_data, ignore_index=True)
    """
    print("Data shape:", dataframe.shape)
    print(dataframe.head())
    print(dataframe.info())
    print(dataframe.describe())
    """

    # ----  Duration formatting function ----
    def convert_duration_to_minutes(duration_str):
        if pd.isna(duration_str) or duration_str in ['N/A', '', None]:
            return np.nan

        total_minutes = 0
        parts = str(duration_str).split()

        for part in parts:
            if 'h' in part:
                total_minutes += int(part.replace('h', '')) * 60
            elif 'm' in part:
                total_minutes += int(part.replace('m', ''))
            elif 's' in part:
                total_minutes += int(part.replace('s', ''))//60

        return total_minutes

    # ---- Apply the function ----
    dataframe['duration'] = dataframe['duration'].apply(convert_duration_to_minutes)
    print(dataframe.head(50))
    invalid_duration = dataframe[(dataframe["duration"].isna() | (dataframe["duration"] <= 15))]
    print("\n Invalid duration rows:")
    print(invalid_duration)

    dataframe.drop(invalid_duration.index, inplace=True)

    print("\n Cleaned Data Shape:", dataframe.shape)

    remaining_invalid = dataframe[(dataframe["duration"].isna()) | (dataframe["duration"] <= 15)]
    if remaining_invalid.empty:
        print("\n No invalid durations remain after cleaning!")
    else:
        print("\n Still found invalid durations:")
        print(remaining_invalid)

    def minutes_to_hhmmss(minutes):
        if pd.isna(minutes) or minutes in ['N/A', '', None]:
            return None

        total_minutes = int(minutes)
        hours = total_minutes // 60
        mins = total_minutes % 60
        return f"{hours:02}:{mins:02}:00"

    dataframe['duration'] = dataframe['duration'].apply(minutes_to_hhmmss)
    print(dataframe.head(50))

    dataframe.to_csv("imdb_cleaned.csv", index=False, encoding="utf-8")
    print("\n Cleaned data saved to 'imdb_cleaned.csv'")

#eda()
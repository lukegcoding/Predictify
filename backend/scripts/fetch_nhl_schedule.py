import requests
from datetime import datetime, timedelta
import pandas as pd
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Game  # Adjusted import statement

# Use a test database URL
DATABASE_URL = "postgresql://lukegosnell@localhost:5432/predictify"  # For PostgreSQL testing

# Set up database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fetch_schedule_for_week(date):
    """Fetch the NHL Schedule for a given date"""
    url = f"https://api-web.nhle.com/v1/schedule/{date}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        game_weeks = data.get("gameWeek", [])

        schedule_data = []

        for week in game_weeks:
            date = week.get("date")
            games = week.get("games", [])

            for game in games:
                schedule_data.append({
                    "game_id": game.get("id"),
                    "date": date,
                    "season": game.get("season"),
                    "game_type": game.get("gameType"),
                    "venue": game.get("venue", {}).get("default"),
                    "neutral_site": game.get("neutralSite"),
                    "start_time": game.get("startTimeUTC"),
                    "home_team": game.get("homeTeam", {}).get("placeName", {}).get("default"),
                    "home_team_score": game.get("homeTeam", {}).get("score"),
                    "away_team": game.get("awayTeam", {}).get("placeName", {}).get("default"),
                    "away_team_score": game.get("awayTeam", {}).get("score"),
                    "game_state": game.get("gameState"),
                    "game_center_link": game.get("gameCenterLink")
                })
        
        df = pd.DataFrame(schedule_data)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch schedule data: {e}")
        return pd.DataFrame()

def fetch_schedule_for_year(start_year):
    """Fetches the schedule for the whole year (i.e. fetch_schedule_for_year(2024) = 2024-25 NHL Schedule)"""
    start_date = f"{start_year}-10-01"
    end_date = f"{start_year + 1}-07-15"

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    entire_schedule_data = []

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        week_schedule = fetch_schedule_for_week(date_str)

        if not week_schedule.empty:
            entire_schedule_data.append(week_schedule)

            last_date_str = week_schedule['date'].iloc[-1]
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            current_date = last_date + timedelta(days=1)
        else:
            break

    if entire_schedule_data:
        entire_schedule_df = pd.concat(entire_schedule_data, ignore_index=True)
        return entire_schedule_df
    else:
        print("No schedule data found for the specified year.")
        return pd.DataFrame()

def insert_schedule_into_db(schedule_df):
    """Insert the fetched schedule into the database using pandas to_sql"""
    try:
        schedule_df.to_sql('games', con=engine, if_exists='append', index=False)
        print("Schedule data inserted successfully.")
    except Exception as e:
        print(f"Failed to insert schedule into database: {e}")

if __name__ == "__main__":
    nhl_schedule_2024 = fetch_schedule_for_year(2024)
    print(nhl_schedule_2024.head())  # To verify it works
    insert_schedule_into_db(nhl_schedule_2024)

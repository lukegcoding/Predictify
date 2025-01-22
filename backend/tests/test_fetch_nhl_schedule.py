import unittest
from unittest.mock import patch
import json
from scripts.fetch_nhl_schedule import fetch_schedule_for_week

class TestFetchNhlSchedule(unittest.TestCase):
    @patch('scripts.fetch_nhl_schedule.requests.get')
    def test_fetch_schedule_success(self, mock_get):
        """Test fetching the NHL schedule successfully."""
        mock_response = {
            "gameWeek": [
                {
                    "date": "2021-10-04",
                    "games": [
                        {
                            "id": 2021020001,
                            "season": "2021-2022",
                            "gameType": 1,
                            "venue": {"default": "Venue Name"},
                            "neutralSite": "No",
                            "startTimeUTC": "2021-10-04T23:00:00Z",
                            "homeTeam": {"placeName": {"default": "Home Team"}, "score": 3},
                            "awayTeam": {"placeName": {"default": "Away Team"}, "score": 2},
                            "gameState": "Final",
                            "gameCenterLink": "http://example.com"
                        }
                    ]
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        date = "2021-10-04"
        schedule_df = fetch_schedule_for_week(date)
        self.assertFalse(schedule_df.empty)
        self.assertEqual(schedule_df.iloc[0]["game_id"], 2021020001)

    @patch('scripts.fetch_nhl_schedule.requests.get')
    def test_fetch_schedule_failure(self, mock_get):
        """Test fetching the NHL schedule with a failure response."""
        mock_get.return_value.status_code = 404

        date = "2021-10-04"
        schedule_df = fetch_schedule_for_week(date)
        self.assertTrue(schedule_df.empty)

if __name__ == "__main__":
    unittest.main()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Game  # Adjusted import statement
import unittest
import os

# Use a test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"  # For in-memory testing

# Set up test database engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Create the database tables before each test."""
        Base.metadata.create_all(bind=engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        """Drop the database tables after each test."""
        Base.metadata.drop_all(bind=engine)
        self.db.close()

    def test_create_user(self):
        """Test creating a user."""
        user = User(username="testuser", email="testuser@example.com", hashed_password="hashedpassword")
        self.db.add(user)
        self.db.commit()

        db_user = self.db.query(User).filter(User.username == "testuser").first()
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, "testuser")

    def test_bulk_create_users(self):
        """Test creating multiple users."""
        users = [
            User(username=f"testuser{i}", email=f"testuser{i}@example.com", hashed_password="hashedpassword")
            for i in range(1000)  # Adjust the number as needed
        ]
        self.db.bulk_save_objects(users)
        self.db.commit()

        count = self.db.query(User).count()
        self.assertEqual(count, 1000, "Not all users were created")

        # Clean up by deleting all users
        self.db.query(User).delete()
        self.db.commit()

    def test_create_game(self):
        """Test creating a game."""
        game = Game(
            game_id=2021020001,
            date="2021-10-04T23:00:00Z",
            season="2021-2022",
            game_type=1,
            venue="Venue Name",
            neutral_site="No",
            start_time="2021-10-04T23:00:00Z",
            home_team="Home Team",
            home_team_score=3,
            away_team="Away Team",
            away_team_score=2,
            game_state="Final",
            game_center_link="http://example.com"
        )
        self.db.add(game)
        self.db.commit()

        db_game = self.db.query(Game).filter(Game.game_id == 2021020001).first()
        self.assertIsNotNone(db_game)
        self.assertEqual(db_game.home_team, "Home Team")

    @classmethod
    def tearDownClass(cls):
        """Dump the in-memory database to a file after all tests."""
        dump_engine = create_engine("sqlite:///test_dump.db")
        Base.metadata.create_all(bind=dump_engine)
        with dump_engine.connect() as conn:
            for table in Base.metadata.tables.values():
                conn.execute(text(f"INSERT INTO {table.name} SELECT * FROM {table.name}"))

if __name__ == "__main__":
    unittest.main()

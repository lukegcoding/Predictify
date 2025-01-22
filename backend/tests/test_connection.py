import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect
from app.models import Base  # Adjusted import statement

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.connection_string = "sqlite:///:memory:"  # For in-memory testing
        self.engine = create_engine(self.connection_string)
        Base.metadata.create_all(bind=self.engine)

    def test_connection(self):
        try:
            with self.engine.connect() as connection:
                self.assertFalse(connection.closed)

        except OperationalError as e:
            self.fail(f"Database connection failed: {e}")

    def test_users_table_exists(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        self.assertIn("users", tables, "Table 'users' does not exist")

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
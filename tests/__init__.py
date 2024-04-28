from dotenv import load_dotenv
import os
from pathlib import Path

test_base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = Path(os.path.abspath(__file__)).parent.parent
env_file_path = os.path.join(env_path, ".env")
load_dotenv(env_file_path)
TEST_DUMMY_API_KEY = os.getenv("TEST_DUMMY_API_KEY_DEV")
TEST_DUMMY_API_URL = os.getenv("TEST_DUMMY_API_URL_DEV")
TEST_DUMMY_USER_ID = os.getenv("TEST_DUMMY_USER_ID_DEV")
user_stage = "dev"

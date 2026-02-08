import os
from dotenv import load_dotenv

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

if COINGECKO_API_KEY is None:
    raise ValueError("COINGECKO_API_KEY not found in environment variables")

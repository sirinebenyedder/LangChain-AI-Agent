from app import launch_app
import os
from dotenv import load_dotenv

# This is the "switch" that turns on the connection
load_dotenv() 

# Double check if it's loaded (print this once to verify)
print(f"Tracing is: {os.getenv('LANGCHAIN_TRACING_V2')}")
# Now you can call it directly
launch_app(os.getenv("GEMINI_API_KEY"))


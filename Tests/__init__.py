# This file will initialize what needed to run the test script standalone

import sys
import os

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

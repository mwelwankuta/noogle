import sqlite3
import os

absolute_path = os.path.dirname(__file__)
relative_path = "../spider/database/database.db"
full_path = os.path.join(absolute_path, relative_path)

conn = sqlite3.connect(full_path)

import os
from dataclasses import dataclass


@dataclass
class Settings:
    project_root: str = os.path.dirname(__file__)
    db_name: str = "dbname"

settings = Settings()
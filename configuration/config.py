import os
import dotenv
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    database: str         
    db_host: str          
    db_user: str          
    db_password: str      
    db_port: str          
    def to_dict(self) -> dict[str, str]:
        return {"database": self.database, 
                "db_host": self.db_host, 
                "db_user": self.db_user, 
                "db_password": self.db_password,
                "db_port": self.db_port}


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config() -> Config:
    dotenv.load_dotenv()
    return Config(
        tg_bot=TgBot(token=os.getenv('BOT_TOKEN')),
        db=DatabaseConfig(
            database=os.getenv('DATABASE'),
            db_host=os.getenv('DB_HOST'),
            db_user=os.getenv('DB_USER'),
            db_password=os.getenv('DB_PASSWORD'),
            db_port=os.getenv('DB_PORT')
        )
    )

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Kitty Fun_Dacja'
    app_description: str = 'Lets support all kitties!'
    database_url: str = 'sqlite+aiosqlite:///./kitty_fun_dacja.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()

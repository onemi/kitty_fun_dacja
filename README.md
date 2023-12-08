# Kitty Fun_Dacja

### Stack
- Python 3.7+
- FastAPI
- Alembic
- Pydantic
- SQLAlchemy
- SQLite

### Описание проекта  

This project helps to track and automatically distribute the donations to the projects in the order in which they were added to the database.

### Launch

Close the repo and navigate to it:

```
git clone git@github.com:onemi/kitty_fun_dacja.git
```

```
cd kitty_fun_dacja
```

Create and activate venv:

```
python3 -m venv venv
```

* Linux/macOS

    ```
    source venv/bin/activate
    ```

* Windows

    ```
    source venv/scripts/activate
    ```

Install the dependencies from requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


Create in root .env:
```
APP_TITLE=YOUR_TITLE
APP_DESCRIPTION=YOUR_DESCRIPTION
DATABASE_URL=sqlite+aiosqlite:///./your_database_name.db
SECRET='supercalifragilisticexpialidocious'  # any sequence of symbols
```

Database and migrations management:
- apply existing migrations
```
alembic upgrade head
```

To run locally:
```
    uvicorn app.main:app --reload
```

Help `uvicorn --help`.

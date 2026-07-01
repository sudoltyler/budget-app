# Budget App

A personal budgeting web app pulling transaction data via SimpleFIN.

## Stack

- **Backend**: Django + Django Ninja + SQLite
- **Frontend**: React + Vite
- **Data source**: [SimpleFIN](https://www.simplefin.org/)

## Project structure

```
budget-app/
├── backend/
│   ├── config/           # Django project config (settings, urls, api)
│   ├── simplefin_app/    # Django app: models, SimpleFIN client, routers
│   │   ├── migrations/
│   │   ├── routers/
│   │   ├── models.py
│   │   └── simplefin.py  # Framework-agnostic SimpleFIN client
│   ├── tests/
│   ├── manage.py
│   ├── pytest.ini
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/client.js
    │   ├── components/
    │   └── App.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## How the SimpleFIN flow works

1. Connect your bank through a SimpleFIN bridge (e.g. https://bridge.simplefin.org)
   and copy the one-time **setup token** it gives you.
2. Paste that token into the app's Connect form. The backend decodes the base64
   token to get a claim URL, POSTs to it, and receives back a permanent
   **access URL** with embedded Basic Auth credentials. This is stored in SQLite.
3. From then on, the backend uses that access URL to fetch accounts and
   transactions, with rate limiting and exponential backoff built in.

The access URL is a long-lived credential — guard the SQLite file like a password.
Never commit `budget.db` or `.env` to version control.

## Running the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

Interactive API docs at: http://localhost:8000/api/docs

Run tests:

```bash
pytest
```

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

App at http://localhost:5173. The Vite dev server proxies `/api` → `localhost:8000`
automatically, so no CORS issues in development.

## Key differences from FastAPI version

|                | FastAPI                      | Django Ninja                            |
|----------------|------------------------------|-----------------------------------------|
| ORM            | SQLAlchemy (`create_all`)    | Django ORM (migrations)                 |
| Migrations     | None (auto create_all)       | Explicit files — makemigrations/migrate |
| API style      | FastAPI native               | Django Ninja (same Pydantic DX)         |
| Test client    | httpx.AsyncClient            | ninja.testing.TestClient                |
| Admin panel    | None                         | django.contrib.admin (optional)         |

## Next steps

- Persist fetched transactions in a `Transaction` model so you can categorize them
- Add a `Budget` model with category limits
- Add simple single-user authentication before deploying beyond localhost
- Add a scheduled sync job (e.g. `django-apscheduler`) to pull transactions periodically

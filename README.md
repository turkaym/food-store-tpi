# Food Store

Food Store is a full-stack ordering application for a small restaurant. Customers can browse the active catalog, keep a persisted cart, place orders, review their order history, and cancel eligible orders. Administrators can manage categories, products, stock, customer accounts, order states, and operational summary data.

## Public Delivery Links

- Public GitHub repository: `https://github.com/turkaym/food-store-tpi`
- Public 10-15 minute video: `https://drive.google.com/file/d/18gjGltyKD6nJ_FkiW6IfGc-MJ185bmbg/view?usp=sharing`

## Quick Path

1. Install Python 3.11+, Node.js 20+, and pnpm.
2. Configure the backend environment and start PostgreSQL, or use the documented SQLite fallback for local checks.
3. Install dependencies, run the idempotent seed, and start the API and frontend.
4. Open `http://localhost:5173` and use the customer or administrator demo flow below.

## Architecture

```text
TP_Integrador_Final/
├── backend/       FastAPI, SQLModel, JWT cookie authentication, transactional services
│   └── app/       core, database seed, auth, catalog, category, product, and order modules
└── frontend/      Vite, React, TypeScript, TanStack Query/Form/Table, and Zustand
    └── src/       routes, customer features, administrator features, shared API and stores
```

The backend exposes versioned routes under `/api/v1`. Authentication is cookie-only: the API writes an HttpOnly `access_token` cookie and the frontend sends it with credentialed Axios requests. The order service owns a unit of work so stock changes and order creation commit or roll back together.

## Requirements

- Python 3.11 or newer
- PostgreSQL 15 or newer for the intended database setup
- Node.js 20 or newer
- pnpm 10 or compatible pnpm version

SQLite is supported by the current backend configuration for isolated local checks. It is not a substitute for required PostgreSQL verification.

## Installation

Run these commands from `TP_Integrador_Final/`.

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Never commit `.env`. On non-PowerShell shells, use the equivalent copy command.

### Frontend

```powershell
cd frontend
pnpm install --frozen-lockfile
Copy-Item .env.example .env
```

The frontend template points to the versioned local API at `http://localhost:8000/api/v1`.

## Environment Variables

### Backend: `backend/.env`

| Variable | Purpose | Local example |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy database URL | `postgresql://postgres:postgres@localhost:5432/foodstore_db` |
| `SECRET_KEY` | Private JWT signing secret of at least 32 characters | `replace-with-a-private-32-character-value` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Cookie token lifetime | `30` |
| `FRONTEND_ORIGIN` | Exact frontend origin allowed by CORS | `http://localhost:5173` |

The backend has a SQLite fallback of `sqlite:///./foodstore.db` when no `.env` is present. Use a private secret outside local smoke checks.

### Frontend: `frontend/.env`

| Variable | Purpose | Local example |
| --- | --- | --- |
| `VITE_API_URL` | Versioned API base URL used by Axios | `http://localhost:8000/api/v1` |

Vite exposes `VITE_*` values to the browser. Do not place secrets in the frontend environment.

## Database Setup

Create the PostgreSQL database before starting the API:

```sql
CREATE DATABASE foodstore_db;
```

Set `DATABASE_URL` in `backend/.env` to match the local PostgreSQL user, password, host, port, and database. The application creates missing tables during startup. Run the idempotent seed command from `backend/`:

```powershell
python -m app.db.seed
```

Repeated runs do not duplicate the administrator, categories, or products identified by their unique names. The seed creates:

- Administrator username: `admin`
- Administrator password: `Admin1234!`
- Three categories
- Eight stocked products

Change the demonstration password before using the application outside local evaluation.

## Run And Build

Start the backend from `backend/`:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation is available through Swagger UI at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`. The OpenAPI document is at `http://localhost:8000/openapi.json`.

Start the frontend from `frontend/`:

```powershell
pnpm dev
```

The production build and type check are:

```powershell
pnpm typecheck
pnpm build
```

## Complete Demo Script

### Customer flow

1. Open `http://localhost:5173` and confirm the seeded catalog is visible.
2. Filter by category or product name, add products to the cart, and change quantities.
3. Register a customer account with a valid email and a password of at least eight characters.
4. Sign in, open the cart, continue to checkout, enter an address, choose a payment method, and submit the order.
5. Verify copied item names, prices, quantities, subtotals, and total on the order detail page.
6. Open `My orders`, return to the order detail, and cancel the pending order.
7. Confirm the status changes to `CANCELADO` and then sign out.

### Administrator flow

1. Sign in with username `admin` and password `Admin1234!`.
2. Open `Admin` and verify pending, preparation, delivered, cancelled, today, and revenue summary cards.
3. Create, edit, and deactivate a category.
4. Create a product in an active category, edit it, update stock, and deactivate it.
5. Expand an order, move a pending order to `EN_PREPARACION`, then to `ENTREGADO` when valid.
6. Cancel another eligible order and verify cancellation and stock restoration.
7. Activate or deactivate a non-administrator customer account.
8. Use `/docs` to inspect versioned endpoint contracts and authentication behavior.

## Verification

The final bounded verification record is maintained in `odd/tasks/tp-integrador-final.md`. It records backend compilation/import/OpenAPI, isolated seed idempotency, frontend installation/type checking/build, and controlled HTTP checks with their limitations.

Create a fresh backend virtual environment and install the runtime and test dependencies from `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

`requirements-dev.txt` includes the runtime requirements and pins the test runner used by the project.

## Known Limitations

- PostgreSQL integration is not claimed unless a real PostgreSQL instance is available during verification.
- Browser-driven smoke testing is not claimed; the frontend HTTP check only proves that the development server serves a page.
- The frontend production bundle reports a Vite warning about a JavaScript chunk larger than 500 kB.
- The seeded administrator password is a demonstration credential and must be changed for non-local deployment.
- There is no production deployment infrastructure, password reset, payment processing, image hosting, or automated end-to-end browser suite.

## Delivery Package

The delivery archive is `TP_Integrador_Final.zip`. It contains only the `TP_Integrador_Final/` directory with source, configuration templates, dependency manifests, and documentation. Dependency directories, build output, caches, `.env` files, and temporary database files are excluded.

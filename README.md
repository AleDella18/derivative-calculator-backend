# derivative-calculator-backend

Backend API for a derivative calculator application. The service authenticates users, validates mathematical expressions, computes symbolic derivatives, stores previously computed functions in a Turso/libSQL database, and generates PNG plots in memory and stores them in Vercel Blob.


## Features

- User signup and signin with hashed passwords and JWT cookies.
- Authenticated derivative computation endpoint.
- Expression validation for invalid characters, parenthesis issues, missing operators, missing function arguments, and division by zero.
- Symbolic differentiation and simplification for supported arithmetic operators and mathematical functions.
- Reuse of cached derivatives already stored in the database.
- In-memory PNG graph generation with public storage in Vercel Blob.
- Built-in FastAPI OpenAPI and Swagger UI documentation.

## Architecture overview

The application is a FastAPI service organized around API routers, service-layer derivative logic, repository functions, and a Turso/libSQL database connection manager.

- `app/main.py` creates the FastAPI application, configures CORS, validates required storage configuration, initializes logging, and opens/closes the database connection during the application lifespan.
- `app/api/endpoints/` exposes authentication and expression endpoints.
- `app/services/` contains parser, differentiator, simplifier, derivative orchestration, and graph generation logic.
- `app/validator/` validates and normalizes incoming expression strings before differentiation.
- `app/repository/` contains database access functions for users, functions, derivatives, and generated graph URLs.
- `app/schemas/` defines Pydantic request and response models.

For a new expression, the endpoint computes the derivative, renders its graph
into an in-memory PNG buffer, and delegates the upload to the reusable Vercel
Blob REST client. Only after Blob returns a validated public URL does the
repository insert the derivative and URL into `FUNCTIONS`. Cached expressions
skip graph rendering and upload and return the value already stored in
`path_graph`.

## Tech stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Turso/libSQL (`libsql`)
- python-jose for JWT handling
- Passlib with bcrypt-sha256 password hashing
- SymPy for expression conversion and simplification support
- Matplotlib and NumPy for graph generation
- Vercel Blob for public graph storage
- HTTPX for asynchronous Blob REST API requests
- pytest test suite

## Project structure

```text
.
├── app/
│   ├── api/endpoints/      # FastAPI routers for auth and expression APIs
│   ├── core/               # Database manager and logging configuration
│   ├── models/             # Expression tree model
│   ├── repository/         # Database query helpers
│   ├── schemas/            # Pydantic request/response schemas
│   ├── services/           # Parsing, differentiation, simplification, graph generation
│   ├── utils/              # Shared utility, JWT, formula, and password helpers
│   ├── validator/          # Expression validation and preprocessing
│   └── main.py             # FastAPI application entry point
├── db/                     # Local database file used as a schema/reference artifact
├── tests/                  # Unit and API tests
├── requirements.txt        # Python runtime dependencies
└── README.md               # Project documentation
```

## Prerequisites

- Python 3.11 or newer is recommended.
- A Turso/libSQL database with the expected `USERS` and `FUNCTIONS` tables.
- A public Vercel Blob store and its read/write token.
- `pip` and a Python virtual environment tool.

## Installation

```bash
git clone <repository-url>
cd derivative-calculator-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

The application loads environment variables from the process environment and supports `.env` files through `python-dotenv`.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `TURSO_DATABASE_URL` | Yes | None | Turso/libSQL database URL passed to `libsql.connect`. The application fails at startup if it is missing. |
| `TURSO_AUTH_TOKEN` | Yes | None | Turso/libSQL authentication token passed to `libsql.connect`. The application fails at startup if it is missing. |
| `SECRET_KEY` | No | Development default | Secret used to sign and verify JWT authentication cookies. Set this in every non-local environment. |
| `BLOB_READ_WRITE_TOKEN` | Yes | None | Read/write token for the public Vercel Blob store. Startup fails with a clear error when it is missing or empty. |

Example `.env` file:

```env
TURSO_DATABASE_URL=libsql://your-database.turso.io
TURSO_AUTH_TOKEN=your-turso-token
SECRET_KEY=replace-with-a-secure-random-secret
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_your-token
```

## Running the project

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000` by default.

### Built-in documentation

FastAPI automatically exposes interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

### Endpoint summary

| Method | Path | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | `/signup` | Register a new user. | No |
| `POST` | `/signin` | Authenticate a user and set the JWT cookie. | No |
| `POST` | `/expression` | Compute or retrieve a derivative and return its public graph URL. | Yes |

## API documentation

### `POST /signup`

Registers a new user.

Request body:

```json
{
  "username": "user@example.com",
  "password": "Str0ng!Password"
}
```

Successful response:

```json
{
  "message": "User successfully registered"
}
```

Validation and error behavior:

- Returns `400` if the user already exists.
- Returns `400` if the password is invalid.
- Passwords must be at least 8 characters and include lowercase, uppercase, numeric, and special characters.

### `POST /signin`

Authenticates an existing user and sets an `auth_token` HTTP-only cookie.

Request body:

```json
{
  "username": "user@example.com",
  "password": "Str0ng!Password"
}
```

Successful response:

```json
{
  "message": "Login completed"
}
```

Validation and error behavior:

- Returns `400` if the user does not exist.
- Returns `400` if the password is incorrect.

### `POST /expression`

Computes the derivative, generates its graph in memory, uploads the PNG to Vercel Blob, and stores the complete public URL with the derivative. Cached expressions return their stored URL without another upload. This endpoint requires the `auth_token` cookie created by `POST /signin`.

Request body:

```json
{
  "expr": "(ln(x) ^ 2) * sin(x)",
  "diff_var": "x"
}
```

Successful response:

```json
{
  "derivative": "(x*log(x)*cos(x) + 2*sin(x))*log(x)/x",
  "img_path": "https://store.public.blob.vercel-storage.com/graphs/550e8400-e29b-41d4-a716-446655440000.png"
}
```

Validation and error behavior:

- Returns `401` when the authentication cookie is missing.
- Returns `401` when the token is invalid or expired.
- Returns `400` when expression validation or derivative computation fails.
- Returns `500` for unexpected internal errors.

## Authentication

Authentication is implemented with JWTs stored in an HTTP-only cookie named `auth_token`.

- `POST /signin` signs a JWT containing the username in the `sub` claim.
- Tokens expire after 30 minutes.
- Cookies are set with `HttpOnly`, `SameSite=None`, and `Secure` attributes.
- `POST /expression` reads the cookie, decodes the JWT, and uses the username when saving derivative records.

## Error handling

The API uses FastAPI `HTTPException` responses with JSON `detail` fields.

Common error response format:

```json
{
  "detail": "Error message"
}
```

Implemented validation includes:

- Missing or invalid authentication token.
- Duplicate signup username.
- Invalid signin credentials.
- Password policy violations.
- Invalid expression characters.
- Invalid, redundant, or mismatched parentheses.
- Missing operators or missing operator arguments.
- Missing function arguments.
- Division by zero detection.
- Unexpected expression-processing failures.

## Dependencies

Runtime dependencies are pinned or declared in `requirements.txt`:

```text
fastapi==0.115.0
uvicorn==0.33.0
libsql>=0.1.11
python-jose[cryptography]
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
python-dotenv
sympy==1.13.3
matplotlib==3.10.8
numpy==2.4.4
httpx==0.28.1
```

## Development notes

- The repository currently does not include Docker or Docker Compose configuration.
- The repository currently does not include a Makefile or package-level script runner.
- CORS is configured for the deployed frontend, local frontend development at `http://localhost:3000`, and `http://derivator.duckdns.org`.
- The checked-in `db/db_function.db` file shows the expected local schema shape for `USERS` and `FUNCTIONS`, but the running application connects through Turso/libSQL environment variables.
- New graph records store complete public Blob URLs in the existing `path_graph` column. Legacy rows containing `imgs/...` paths remain unchanged and are returned as stored; no automatic data migration is performed.
- Graph upload occurs before the database insert, so failed uploads do not create rows with missing or invalid graph URLs. A database failure after upload can leave an unreferenced Blob that may be cleaned up operationally.

## Running tests

```bash
PYTHONPATH=. pytest
```

## Contributing

1. Fork the repository and create a feature branch.
2. Create or update tests for behavior changes.
3. Run the test suite before opening a pull request.
4. Keep changes focused and document any new environment variables or endpoints in this README.

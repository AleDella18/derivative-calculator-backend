# derivative-calculator-backend

Backend API for a derivative calculator application. The service authenticates users, validates mathematical expressions, computes symbolic derivatives, stores previously computed functions in a Turso/libSQL database, and generates PNG plots for derivative results.

## Features

- User signup and signin with hashed passwords and JWT cookies.
- Authenticated derivative computation endpoint.
- Expression validation for invalid characters, parenthesis issues, missing operators, missing function arguments, and division by zero.
- Symbolic differentiation and simplification for supported arithmetic operators and mathematical functions.
- Reuse of cached derivatives already stored in the database.
- PNG graph generation for computed derivatives under the `imgs/` static directory.
- Built-in FastAPI OpenAPI and Swagger UI documentation.

## Architecture overview

The application is a FastAPI service organized around API routers, service-layer derivative logic, repository functions, and a Turso/libSQL database connection manager.

- `app/main.py` creates the FastAPI application, configures CORS, mounts static image files, initializes logging, and opens/closes the database connection during the application lifespan.
- `app/api/endpoints/` exposes authentication and expression endpoints.
- `app/services/` contains parser, differentiator, simplifier, derivative orchestration, and graph generation logic.
- `app/validator/` validates and normalizes incoming expression strings before differentiation.
- `app/repository/` contains database access functions for users, functions, derivatives, and generated graph paths.
- `app/schemas/` defines Pydantic request and response models.

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
├── imgs/                   # Generated and committed derivative graph images served at /imgs
├── tests/                  # Unit and API tests
├── requirements.txt        # Python runtime dependencies
└── README.md               # Project documentation
```

## Prerequisites

- Python 3.11 or newer is recommended.
- A Turso/libSQL database with the expected `USERS` and `FUNCTIONS` tables.
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
| `SECRET_KEY` | No | `;+z8X*(cmbN|#si#` | Secret used to sign and verify JWT authentication cookies. Set this in every non-local environment. |

Example `.env` file:

```env
TURSO_DATABASE_URL=libsql://your-database.turso.io
TURSO_AUTH_TOKEN=your-turso-token
SECRET_KEY=replace-with-a-secure-random-secret
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
| `POST` | `/expression` | Compute or retrieve a derivative and return its graph path. | Yes |

### Static files

Generated derivative plots are saved in `imgs/` and served from:

```text
/imgs/{filename}.png
```

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

Computes and stores the derivative for an expression. This endpoint requires the `auth_token` cookie created by `POST /signin`.

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
  "img_path": "imgs/1.png"
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
python-dotenv
sympy==1.13.3
matplotlib==3.10.8
numpy==2.4.4
```

## Development notes

- The repository currently does not include Docker or Docker Compose configuration.
- The repository currently does not include a Makefile or package-level script runner.
- CORS is configured for the deployed frontend, local frontend development at `http://localhost:3000`, and `http://derivator.duckdns.org`.
- The checked-in `db/db_function.db` file shows the expected local schema shape for `USERS` and `FUNCTIONS`, but the running application connects through Turso/libSQL environment variables.
- API tests use FastAPI's `TestClient`; install `httpx` in the development environment if running those tests directly.

## Running tests

```bash
PYTHONPATH=. pytest
```

## Contributing

1. Fork the repository and create a feature branch.
2. Create or update tests for behavior changes.
3. Run the test suite before opening a pull request.
4. Keep changes focused and document any new environment variables or endpoints in this README.

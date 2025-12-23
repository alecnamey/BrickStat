# BrickStat — Run & Secrets

Quick notes to run the backend with Docker and safely share the `.env` values.

**1) Add your secrets (do not commit)**
- Copy `brickstat-app/backend/.env.example` to `brickstat-app/backend/.env` and fill in your real `REBRICKABLE_API_KEY`.

  macOS / Linux:
  ```bash
  cp brickstat-app/backend/.env.example brickstat-app/backend/.env
  # edit the file and add your key
  ```

  PowerShell (Windows):
  ```powershell
  Copy-Item brickstat-app/backend/.env.example brickstat-app/backend/.env
  # edit the file and add your key
  ```

**2) Run with Docker Compose**
- From the repo root:
  ```bash
  docker compose up --build
  # or detached
  docker compose up -d --build
  ```

**3) Non-interactive lookup at start**
- To run a single set lookup when starting the container:
  ```bash
  SET_NUMBER=75257-1 docker compose up --build
  ```

**4) Development (no venv required)**
- When using Docker the image provides Python and installs `requirements.txt` — your partner does not need to create a virtual environment.

**5) Securely sharing the `.env` values**
- Recommended: share the API key using a password manager (1Password, Bitwarden) or an encrypted channel (Signal). Do NOT send secrets in plaintext email or commit them to the repo.
- For automation, store the secret in CI (GitHub Actions secrets) and inject it at build/run time rather than committing.

**6) If a secret is exposed**
- Rotate the API key at the provider immediately and replace the value in `.env`.

Questions? I can add a `docker-compose.override.yml` for a dev bind-mount workflow or a short GitHub Actions workflow to build images on push (without committing the secret).
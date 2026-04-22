# Local Dev Postgres Setup (Arch / CachyOS)

**Status**: Applied on this machine on 2026-04-21
**Related**: docs/plans/0002-phase-2-postgres-backend.md, docs/adr/0001-pluggable-storage-and-network-access.md

Purpose: capture the minimum, repeatable steps to stand up a Postgres 18 instance on a local Arch/CachyOS box for Phase 2 (`PgMemoryStore`) development, `sqlx prepare`, and manual migration testing. This is a single-operator dev recipe, not a production runbook.

---

## Current state on this machine

- Package: `postgresql` 18.3-2 (pacman). Pulls `postgresql-libs`, `libxslt`.
- Service: `postgresql.service`, enabled + active.
- Listens on: `127.0.0.1:5432` and `[::1]:5432` only (default `listen_addresses = 'localhost'`).
- Data dir: `/var/lib/postgres/data`, owner `postgres:postgres`.
- Auth (`pg_hba.conf`, Arch defaults): `peer` for local socket, `scram-sha-256` for host 127.0.0.1/::1.

### Database + role

- Database: `vestige`, UTF8, owner `vestige`.
- Role: `vestige` with `LOGIN CREATEDB` (no superuser, no replication, no cross-db).
- Schema `public` re-owned to `vestige`, plus default privileges so any future tables / sequences / functions in `public` are fully owned and granted to `vestige`.

Net effect: the `vestige` role can create, alter, drop, and grant freely inside the `vestige` database -- enough for `sqlx::migrate!`, ad-hoc schema work, and the full Phase 2 `MemoryStore` surface. It cannot create extensions (see Phase 2 followups below) and cannot touch other databases.

### Connection

```
postgresql://vestige:<password>@127.0.0.1:5432/vestige
```

Password lives at `~/.vestige_pg_pw`, mode 600, owned by the dev user (no sudo needed to read it). Read with:

```sh
cat ~/.vestige_pg_pw
```

Recommended dev shell export (keep this OUT of the repo; use `.env` + gitignore or a shell rc):

```sh
export DATABASE_URL="postgresql://vestige:$(cat ~/.vestige_pg_pw)@127.0.0.1:5432/vestige"
```

---

## Reproduce from scratch

On a fresh Arch / CachyOS box with passwordless sudo:

```sh
# 1. Install
sudo pacman -S --noconfirm postgresql

# 2. Initialize the cluster (UTF8, scram-sha-256 for host, peer for local)
sudo -iu postgres initdb \
  --locale=C.UTF-8 --encoding=UTF8 \
  -D /var/lib/postgres/data \
  --auth-host=scram-sha-256 --auth-local=peer

# 3. Start + enable
sudo systemctl enable --now postgresql

# 4. Generate a password and stash it in the dev user's home (mode 600)
VESTIGE_PW=$(python3 -c 'import secrets,string; a=string.ascii_letters+string.digits; print("".join(secrets.choice(a) for _ in range(32)))')
umask 077
printf '%s' "$VESTIGE_PW" > ~/.vestige_pg_pw
chmod 600 ~/.vestige_pg_pw

# 5. Create role + database + grants
sudo -u postgres psql -v ON_ERROR_STOP=1 <<SQL
CREATE ROLE vestige WITH LOGIN CREATEDB PASSWORD '${VESTIGE_PW}';
CREATE DATABASE vestige OWNER vestige ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE vestige TO vestige;
SQL

sudo -u postgres psql -d vestige -v ON_ERROR_STOP=1 <<'SQL'
GRANT ALL ON SCHEMA public TO vestige;
ALTER SCHEMA public OWNER TO vestige;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO vestige;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO vestige;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO vestige;
SQL

# 6. Smoke test
PGPASSWORD="$VESTIGE_PW" psql -h 127.0.0.1 -U vestige -d vestige \
  -c 'SELECT current_user, current_database(), version();'
unset VESTIGE_PW
```

---

## Phase 2 followups (before PgMemoryStore works)

The cluster above is bare Postgres. Phase 2 needs `pgvector`:

```sh
# Install the extension package
sudo pacman -S --noconfirm pgvector

# Enable it in the vestige database (must run as postgres; vestige is not superuser)
sudo -u postgres psql -d vestige -c 'CREATE EXTENSION IF NOT EXISTS vector;'
```

Verify:

```sh
PGPASSWORD="$(cat ~/.vestige_pg_pw)" psql -h 127.0.0.1 -U vestige -d vestige \
  -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
```

Notes:

- `pgvector` must be available on the server before `sqlx::migrate!` runs, or the Phase 2 migration that declares typed `Vector` columns will fail.
- Testcontainer-based Phase 2 integration tests use `pgvector/pgvector:pg16` and are independent of this local cluster. This local cluster is for `sqlx prepare`, `cargo run -- migrate --to postgres`, and manual poking.
- `sqlx prepare` needs `DATABASE_URL` pointed at this cluster with `vestige` migrations already applied. Run from `crates/vestige-core/`.

---

## Password rotation

```sh
NEW_PW=$(python3 -c 'import secrets,string; a=string.ascii_letters+string.digits; print("".join(secrets.choice(a) for _ in range(32)))')
umask 077
printf '%s' "$NEW_PW" > ~/.vestige_pg_pw
chmod 600 ~/.vestige_pg_pw
sudo -u postgres psql -v ON_ERROR_STOP=1 \
  -c "ALTER ROLE vestige WITH PASSWORD '${NEW_PW}';"
unset NEW_PW
```

Then re-export `DATABASE_URL` in any live shells.

---

## Teardown

Destroys the cluster and all data in it:

```sh
sudo systemctl disable --now postgresql
sudo pacman -Rns postgresql postgresql-libs
sudo rm -rf /var/lib/postgres
rm -f ~/.vestige_pg_pw
```

---

## Out of scope for this doc

- TLS, client-cert auth, non-localhost access. Phase 3 exposes the Vestige HTTP API over the network, not Postgres directly.
- Backups, PITR, WAL archiving. For dev data: `pg_dump -h 127.0.0.1 -U vestige vestige > vestige.sql`.
- Replication, PgBouncer, tuned `postgresql.conf`. Defaults are fine for Phase 2 development.
- Making this the canonical Vestige backend. By default Vestige still uses SQLite; this cluster exists so the `postgres-backend` feature can be built and tested locally.

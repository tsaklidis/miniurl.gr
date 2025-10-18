To run an Alembic migration, use the following command in your project directory (where alembic.ini is located):

```bash
alembic upgrade head
```

This command applies all pending migrations up to the latest (the "head"). If you want to migrate to a specific revision, use:

```bash
alembic upgrade <revision>
```

Replace <revision> with the revision identifier (e.g., a hash or "base" for the initial state).
Make sure your database connection settings are correct in alembic.ini or your env.py file.

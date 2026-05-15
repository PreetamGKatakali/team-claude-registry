# db-migrate

Generate and run a database migration safely.

## Steps

1. Ask the user what schema change they need (if not already described).

2. Check the existing migration files to understand naming convention and numbering:
   `ls migrations/` or `ls db/migrations/`

3. Generate the migration file following the existing convention.
   - Always include both `up` and `down` (rollback) sections
   - For adding a NOT NULL column, always provide a default or backfill step
   - Never drop a column without checking for active references in code first

4. Show the migration to the user for review before running it.

5. When the user confirms, run it:
   - For Prisma: `npx prisma migrate dev --name <migration-name>`
   - For Knex / raw SQL: `npm run migrate:latest`
   - For Django: `python manage.py migrate`

6. Verify the migration applied: query the schema or run `npx prisma studio`.

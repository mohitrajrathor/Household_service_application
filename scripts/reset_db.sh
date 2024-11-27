#!/bin/bash

# Navigate to the main directory
cd "$(dirname "$0")/.." || exit

# Delete instance/database.db if it exists
if [ -f "instance/database.db" ]; then
  echo "Deleting existing database..."
  rm "instance/database.db"
fi

# Delete the migrations directory if it exists
if [ -d "migrations" ]; then
  echo "Deleting migrations directory..."
  rm -rf "migrations"
fi

# Reinitialize the model
echo "Initializing Flask-Migrate..."
flask db init

# Generate migration scripts
echo "Generating migration scripts..."
flask db migrate -m "Initial migration"

# Apply migrations
echo "Applying migrations..."
flask db upgrade

# Seed the database
if [ -f "seed_data.py" ]; then
  echo "Seeding data..."
  python seed_data.py
else
  echo "Seed data file (seed_data.py) not found!"
fi

echo "Database reset and seed complete."

#! /bin/bash
echo -e "Resetting backend data...\n"
cd backend || { echo "Error: Directory 'backend/' not found"; exit; }

if [[ "$VIRTUAL_ENV" == "" ]]
then
    source .venv/bin/activate || { echo "Error: Unable to activate venv"; exit; }
    rm budget.db
    rm -rf simplefin_app/migrations
    echo -e "Deleted 'budget.db' and 'simplefin_app/migrations', regenerating migrations...\n"
    python manage.py makemigrations simplefin_app || { echo "Error: Unable make migrations for simplefin_app"; exit; }
    python manage.py migrate || { echo "Error: Unable to migrate"; exit; }
    echo -e "\nSuccessfully reset backend data and created migrations"
fi
    # venv automatically deactivates
    exit

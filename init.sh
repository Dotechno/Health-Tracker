# Delete instance directory
rm -rf instance

# Run setup.py
python setup.py

# Run db_filler.py
python db_filler.py
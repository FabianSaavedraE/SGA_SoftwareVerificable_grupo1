import json
from flask import (
    redirect, flash, url_for
)

#Functions that validate the data loading process -----------------------------

def validate_json_file_and_return_processed_file(file):
    
    try:
        data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        flash('Error: File does not follow a valid JSON format', 'error')
        return None
    except Exception as e:
        flash('Error processing file', 'error')
        return None
    
def validate_json_has_required_key(json_data, key):
    if key in json_data:
        return True
    else:
        flash(f'ERROR: Key "{key}" not found in json file', 'error')
        return False
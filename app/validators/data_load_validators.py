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
        flash('Error: El archivo no tiene un formato JSON válido', 'error')
        return None
    except Exception as e:
        flash('Error al procesar el archivo', 'error')
        return None
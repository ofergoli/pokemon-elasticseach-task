from flask import Flask, request
from elastic_search_utils import update_mapping, add_document, search_document, search_with_cache
from validation import is_valid_pokemon_request

app = Flask(__name__)

@app.route('/api', methods=['PUT'])
def create_document():
    if is_valid_pokemon_request(request.json):
        update_mapping(request.json)
        return add_document(request.json)
    return "Invalid Pokemon", 400

@app.route('/api/autocomplete/<term>')
def search(term):
    return search_with_cache(term)

app.run(port=5000)

from constants import VALID_TYPES

def is_valid_pokemon_request(body):
    return body['type'] in VALID_TYPES

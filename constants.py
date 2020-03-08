VALID_TYPES = ["ELECTRIC", "GROUND", "FIRE", "WATER", "WIND", "PSYCHIC", "GRASS"]

index_settings = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "autocomplete_filter"
                    ]
                }
            }
        }
    }
}

index_name = 'netapp'
type_name = 'pokemon'
document_expire_seconds = 5
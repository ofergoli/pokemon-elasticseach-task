from elasticsearch import Elasticsearch
from constants import index_settings, index_name, type_name, document_expire_seconds
from flask import jsonify
import os
import redis
import hashlib
import json

redis_connection = redis.Redis()
es = Elasticsearch()

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_settings)

def create_mapping(value):
    mapping = {
        "properties": {}
    }
    mapping["properties"][value] = {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "standard"
    }
    return mapping

def get_fields_redis():
    field_names = redis_connection.lrange('FIELDS_NAME', 0, -1)
    for idx, value in enumerate(field_names):
        field_names[idx] = field_names[idx].decode('utf-8')
    return field_names

def update_mapping(requestBody):
    field_names = get_fields_redis()
    if field_names is None:
        for value in requestBody.keys():
            redis_connection.lpush('FIELDS_NAME', value)
            es.indices.put_mapping(index=index_name, doc_type=type_name, body=create_mapping(value))
    else:
        for value in requestBody.keys():
            if value not in field_names:
                redis_connection.lpush('FIELDS_NAME', value)
                es.indices.put_mapping(index=index_name, doc_type=type_name, body=create_mapping(value))

def add_document(document):
    res = es.index(index=index_name, doc_type=type_name, body=document)
    return res


def search_document(term):
    field_names = get_fields_redis()
    try:
        field_names.remove('pokadex_id')
    except ValueError:
        pass  #
    results = []
    result = es.search(index=index_name, doc_type=type_name, body={
        "query": {
            "multi_match": {
                "query": term,
                "fields": field_names,
            }
        }
    })
    if result is not None:
        for res in result['hits']['hits']:
            results.append(res['_source'])
        return jsonify(results), results
    return null

def search_with_cache(term):
    redis_cache = redis_connection.get(term)
    if redis_cache is None:
        jsondocument, document = search_document(term)
        redis_connection.set(term, json.dumps(document))
        redis_connection.expire(term, document_expire_seconds)
        return jsondocument
    return redis_cache

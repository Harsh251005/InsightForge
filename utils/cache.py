import json
import os
import hashlib

CACHE_FILE = "cache.json"


def _load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def _save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def _hash_key(query, depth):
    key = f"{query}_{depth}"
    return hashlib.md5(key.encode()).hexdigest()


def get_cached_result(query, depth):
    cache = _load_cache()
    key = _hash_key(query, depth)
    return cache.get(key)


def set_cached_result(query, depth, result):
    cache = _load_cache()
    key = _hash_key(query, depth)
    cache[key] = result
    _save_cache(cache)
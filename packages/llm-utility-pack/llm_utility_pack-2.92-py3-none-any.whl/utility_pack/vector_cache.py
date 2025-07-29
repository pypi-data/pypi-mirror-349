from utility_pack.vector_storage_helper import ShardedLmdbStorage
from collections import OrderedDict
import xxhash

def _hash(key):
    return xxhash.xxh64(key).intdigest()

class VectorCache:
    def __init__(self, path='vector_cache', num_shards=5, max_size=1_000_000):
        self.storage = ShardedLmdbStorage(path, num_shards)
        self.max_size = max_size
        self.lru = OrderedDict()

    def _evict_if_needed(self):
        overflow = len(self.lru) - self.max_size
        if overflow <= 0:
            return
        ids_to_remove = []
        for _ in range(overflow):
            hid, _ = self.lru.popitem(last=False)
            ids_to_remove.append(hid)
        self.storage.delete_data(ids_to_remove)

    def is_cached(self, key):
        hid = _hash(key)
        exists = len(self.storage.get_vectors([hid])) > 0
        if exists:
            # bump recency
            self.lru.pop(hid, None)
            self.lru[hid] = None
        return exists

    def put(self, key, value):
        hid = _hash(key)
        # bump recency
        self.lru.pop(hid, None)
        self.lru[hid] = None

        self.storage.store_vectors([value], [hid])
        self._evict_if_needed()

    def get(self, key):
        hid = _hash(key)
        if not self.is_cached(key):
            return None
        # get_vectors returns a list, so grab [0]
        return self.storage.get_vectors([hid])[0]

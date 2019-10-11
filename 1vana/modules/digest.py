import os
import hashlib

DEFAULT_LOG_HASH_ALGO = 'md5'

class Digest:

    def __init__(self, algo=DEFAULT_LOG_HASH_ALGO, size=0x800):
        
        self.algo   = algo
        self.length = hashlib.new(algo).block_size * 0x800
        self.hash = ""

    def get_hash(self):
        return self.hash

    def file_hash(
        self, filepath
        ):

        h = hashlib.new(self.algo)
        if(os.path.exists(filepath)):
            with open(filepath, 'rb') as f:
                bindata = f.read(self.length)

                while bindata:
                    h.update(bindata)
                    bindata = f.read(self.length)

        self.hash = h.hexdigest()
        return self.hash



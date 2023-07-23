# if you wish to use your sorted list from a1, copy and paste it here
# this is not the best way to do this but the test scripts are not
# designed to pick up an extra file. 

class LinearProbingTS:

	# This is a single record in a chaining hash table.  You can
	# change this in anyway you wish (including not using it at all)
    class Record:
        def _init_(self, key, value):
            self.key = key
            self.value = value

        def if_collide(self):
            return False

    class Tombstone(Record):
        def _init_(self):
            self.key = None
            self.value = None

        def if_collide(self):
            return True
	# You cannot change the function prototypes below.  Other than that
	# how you implement the class is your choice (but it must be a hash
	# table that use chaining for collision resolution)

    def _init_(self, cap=32): # The constructor initializes the LinearProbingTS object with an argument (default is 32).
        self.cap = cap
        self.table = [None] * cap # a list 'table' is created to hold the records
        self.num_items = 0 # number of items is set to 0.

    def insert(self,key, value):
        load_factor = self._find_slot(key)
        if self.table[load_factor] is None or self.table[load_factor].if_collide():
            self.table[load_factor] = self.Record(key, value)
            self.num_items += 1
            if len(self) >= self.cap*0.7: # If a collision occurs or the load factor exceeds 0.7, the table is resized and elements are rehashed.
                  self.restore_size()
            return True
        return False

    def modify(self, key, value): # The modify function changes the value of an existing key in the hash table.
        load_factor = self._find_key(key)
        if load_factor is not None:
            self.table[load_factor].value = value
            return True
        return False

    def remove(self, key): # The remove function removes a key-value pair from the hash table.
        load_factor = self._find_key(key)
        if load_factor is not None:
            self.table[load_factor] = self.Tombstone()
            self.num_items -= 1
            return True
        return False

    def search(self, key): # The search function looks for a key in the hash table and returns its value.
        load_factor = self._find_key(key)
        if load_factor is not None:
            return self.table[load_factor].value
        return None

    def capacity(self): # The capacity function returns the current capacity of the hash table.
        return self.cap

    def _len_(self): # The __len__ function returns the number of items in the hash table.
        return self.num_items

    def _hash(self, key): # The _hash function calculates the hash value for a given key.
        return hash(key) % self.cap

    def _find_slot(self, key):  # The _find_slot function searches for an empty slot for a key using linear probing.
        hash_value = self._hash(key)
        while self.table[hash_value] is not None and self.table[hash_value].key != key:
            hash_value = (hash_value + 1) % self.cap
        return hash_value

    def _find_key(self, key): # The _find_key function finds the index of a key in the hash table.
        load_factor = self._find_slot(key)
        if self.table[load_factor] is not None and not self.table[load_factor].if_collide():
            return load_factor
        return None


    def restore_size(self): # The restore_size function doubles the hash table capacity and rehashes the elements when the load factor exceeds 0.7.
        self.cap *= 2
        prev_table = self.table
        self.num_items = 0
        self.table = [None] * self.cap
        for record in prev_table:
            if record is not None and not record.if_collide():
                self.insert(record.key, record.value)

class LinearProbingNoTS:

	# This is a single record in a chaining hash table.  You can
	# change this in anyway you wish (including not using it at all)
	class Record:
		def _init_(self, key, value):
			self.key = key
			self.value = value



	# You cannot change the function prototypes below.  Other than that
	# how you implement the class is your choice (but it must be a hash
	# table that use linear probing for collision resolution)
	
	def _init_(self, cap=32):
		self.maximum_cap = cap
		self.num_records = 0
		self.table = [None for pos in range(cap)]

	def insert(self,key, value):
		if (self.search(key)!=None):
			return False
		self.num_records+=1
		idx = hash(key)   
		pos = idx % self.maximum_cap 
		while pos < self.maximum_cap*2:
			if self.table[pos%self.maximum_cap ] == None:
				self.table[pos%self.maximum_cap ] = self.Record(key,value)
				break
			pos+=1
		if(len(self) >= self.maximum_cap*0.7):
			fresh_table = [None for idx in range(self.maximum_cap*2)]
			for idx in range(self.maximum_cap):
				fresh_table[idx]=self.table[idx]
			self.table = fresh_table
			self.maximum_cap *= 2
		return True

	def modify(self, key, value):
		idx = hash(key)   
		pos = idx % self.maximum_cap 
		while pos < self.maximum_cap*2:
			if self.table[pos%self.maximum_cap] != None and self.table[pos%self.maximum_cap].key == key:
				self.table[pos%self.maximum_cap].value = value
				return True
			pos+=1
		return False

	def remove(self, key):
		idx = hash(key)   
		pos = idx % self.maximum_cap 
		while pos < self.maximum_cap*2:
			if self.table[pos%self.maximum_cap] != None and self.table[pos%self.maximum_cap].key == key:
				self.table[pos%self.maximum_cap] = None
				self.num_records-=1
				return True
			pos+=1
		return False

	def search(self, key):
		idx = hash(key)   
		pos = idx % self.maximum_cap 
		while pos < self.maximum_cap*2:
			if self.table[pos%self.maximum_cap] != None and self.table[pos%self.maximum_cap].key == key:
				return self.table[pos%self.maximum_cap].value
			pos+=1
		return None

	def capacity(self):
		return self.maximum_cap

	def _len_(self):
		return self.num_records
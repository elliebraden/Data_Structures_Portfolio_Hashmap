# Name: Ellie Braden
# OSU Email: bradebe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap
# Due Date: 6/1/26
# Description: Completion of a HashMap class with a open addressing
#              implementation

from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def __iter__(self):
        """
        Initiates an iterative process
        """
        self._index = 0
        return self

    def __next__(self):
        """
        returns the next occupied array index's obj/value
        """
        element = self._buckets.get_at_index(self._index)
        try:
            #find the next occupied index
            while element is None or element.is_tombstone is True:
                self._index += 1
                element = self._buckets.get_at_index(self._index)

        #no value calculated due to invalid index
        except:
            raise StopIteration

        #valid element - inc index for next __next__ call and return
        self._index = self._index + 1
        return element

    def put(self, key: str, value: object) -> None:
        """
        Inserts a key-val pair into a hash table/map

        param key: key of element to be inserted
        param value: value of element to be inserted, associated with key

        return: nothing, ._size/._buckets changed as needed
        """
        # check load factor, resize if needed
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        #calculate which index to place at
        hash_val = self._hash_function(key)
        cur_index = hash_val % self._capacity

        #initiate variables
        first_tomb = None
        probe_num = 1
        initial_index = cur_index
        cur_pair = self._buckets.get_at_index(cur_index)

        #prope hash table ot find match or open space
        while cur_pair:
            #check if key match - ensure not tombstone
            if cur_pair.key == key and cur_pair.is_tombstone is False:
                cur_pair.value = value
                return
            #check if first tombstone
            elif cur_pair.is_tombstone and first_tomb is None:
                first_tomb = cur_index
            #cal next index and repeat (using quadratic)
            else:
                cur_index = (initial_index + probe_num ** 2) % self._capacity
                probe_num += 1
                cur_pair = self._buckets.get_at_index(cur_index)

        #empty space and no match found
        self._size += 1
        if first_tomb:
            self._buckets.set_at_index(first_tomb, HashEntry(key, value))
        else:
            self._buckets.set_at_index(cur_index, HashEntry(key, value))

    def resize_table(self, new_capacity: int) -> None:
        """
        resizes the hash table

        param new_capacity: new size of table, not yet prime guaranteed

        Return: nothing, ._capacity/._buckets are changed as needed
        """
        if new_capacity < self._size:
            return

        # ensure prime capacity
        # doubled capacity will never be prime but if resizing by user may be prime so don't add + 1
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # initiate new DA
        new_buckets = DynamicArray()
        for index in range(new_capacity):
            new_buckets.append(None)

        # reassign self._buckets
        old_buckets = self._buckets
        self._buckets = new_buckets

        # adjust capacity
        old_capacity = self._capacity
        self._capacity = new_capacity

        #rest size (else will have 2x size after)
        self._size = 0

        #go through old DA and rehash/map
        for index in range(old_capacity):
            this_pair = old_buckets.get_at_index(index)
            if this_pair and this_pair.is_tombstone is False:
                self.put(this_pair.key, this_pair.value)

    def table_load(self) -> float:
        """
        Calculates the load factor of a HashMap

        Return: load factor value
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Finds the associated value of a provided key

        para key: key of target value

        return: value of key if key is present in has table,
                none otherwise
        """
        # calculate which index the key would be at
        hash_val = self._hash_function(key)
        cur_index = hash_val % self._capacity

        #initiate variables
        this_pair = self._buckets.get_at_index(cur_index)
        probe_num = 1
        initial_index = cur_index

        while this_pair:
            # check if key match
            if this_pair.key == key and this_pair.is_tombstone is False:
               return this_pair.value

            #probe to next index
            cur_index = (initial_index + probe_num ** 2) % self._capacity
            probe_num += 1
            this_pair = self._buckets.get_at_index(cur_index)

        #no match found
        return

    def contains_key(self, key: str) -> bool:
        """
        Determines if a key is in a hash table

        param key: target key

        return: True if key exists in hash table, false otherwise
        """
        # calculate which index the key would be at
        hash_val = self._hash_function(key)
        cur_index = hash_val % self._capacity

        #initiate variables
        this_pair = self._buckets.get_at_index(cur_index)
        probe_num = 1
        initial_index = cur_index

        while this_pair:
            # check if key match
            if this_pair.key == key and this_pair.is_tombstone is False:
               return True

            #probe to next index
            cur_index = (initial_index + probe_num ** 2) % self._capacity
            probe_num += 1
            this_pair = self._buckets.get_at_index(cur_index)

        #no match found
        return False

    def remove(self, key: str) -> None:
        """
        removes a key-val pair from the hash table if present

        param key: key of target pair

        Return: nothing, .is_tombstone/._size  changed
        """
        # calculate which index the key would be at
        hash_val = self._hash_function(key)
        cur_index = hash_val % self._capacity

        # initiate variables
        this_pair = self._buckets.get_at_index(cur_index)
        probe_num = 1
        initial_index = cur_index

        while this_pair:
            # check if key match and not already removed
            if this_pair.key == key and this_pair.is_tombstone is False:
                this_pair.is_tombstone = True
                self._size -= 1
                return
            #stop iteration but already removed
            elif this_pair.key == key and this_pair.is_tombstone is True:
                return

            # probe to next index
            cur_index = (initial_index + probe_num ** 2) % self._capacity
            probe_num += 1
            this_pair = self._buckets.get_at_index(cur_index)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of all key-value pairs
        in the hash table
        """
        # initiate variables
        count = 0
        key_val_da = DynamicArray()

        for index in range(self._capacity):
            this_pair = self._buckets.get_at_index(index)
            if this_pair and this_pair.is_tombstone is False:
                key_val_da.append((this_pair.key, this_pair.value))
                count += 1
            #avoid iterating through remaining none once all pairs found
            if count == self._size:
                return key_val_da

    def clear(self) -> None:
        """
        Clears the hash map

        returns: nothing ._buckets/._size are changed
        """
        for index in range(self._capacity):
            self._buckets.set_at_index(index, None)

        self._size = 0

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print('\nPDF - put example 1')
    print('-------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - put example 2')
    print('-------------------')
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - resize example 1')
    print('----------------------')
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print('\nPDF - resize example 2')
    print('----------------------')
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f'Check that the load factor is acceptable after the call to resize_table().\n'
                  f'Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5')

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print('\nPDF - table_load example 1')
    print('--------------------------')
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print('\nPDF - table_load example 2')
    print('--------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 1')
    print('-----------------------------')
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 2')
    print('-----------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - get example 1')
    print('-------------------')
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print('\nPDF - get example 2')
    print('-------------------')
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print('\nPDF - contains_key example 1')
    print('----------------------------')
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print('\nPDF - contains_key example 2')
    print('----------------------------')
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print('\nPDF - remove example 1')
    print('----------------------')
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print('\nPDF - get_keys_and_values example 1')
    print('------------------------')
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print('\nPDF - clear example 1')
    print('---------------------')
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - clear example 2')
    print('---------------------')
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - __iter__(), __next__() example 1')
    print('---------------------')
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print('\nPDF - __iter__(), __next__() example 2')
    print('---------------------')
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

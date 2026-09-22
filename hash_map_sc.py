# Name: Ellie Braden
# OSU Email: bradebe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap
# Due Date: 6/1/26
# Description: Completion of a HashMap class with a chaining implementation


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

    def put(self, key: str, value: object) -> None:
        """
        Inserts a key-val pair into a hash table/map

        param key: key of element to be inserted
        param value: value of element to be inserted, associated with key

        return: nothing, ._size/._buckets changed as needed
        """
        #check load factor, resize if needed
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        #calculate which bucket to place at
        hash_val = self._hash_function(key)
        hash_val = hash_val % self._capacity

        insert_bucket = self._buckets.get_at_index(hash_val)

        #check if key already exists
        dup_key = insert_bucket.contains(key)
        if dup_key:
            dup_key.value = value

        #insert key, no matching key
        else:
            insert_bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        resizes the Hash Table

        param new_capacity: new size of table, not yet prime guaranteed

        Return: nothing, ._capacity/._buckets are changed as needed
        """
        if new_capacity < 1:
            return

        #ensure prime capacity
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        #initiate new DA
        new_buckets = DynamicArray()
        for index in range(new_capacity):
            new_buckets.append(LinkedList())

        # reassign self._buckets
        old_buckets = self._buckets
        self._buckets = new_buckets

        # adjust capacity
        old_capacity = self._capacity
        self._capacity = new_capacity

        #rest size (else will have 2x size after)
        self._size = 0
        #go through each of the old buckets and add to new
        for index in range(old_capacity):
            this_bucket = old_buckets.get_at_index(index)
            if this_bucket.length() > 0:
                for node in this_bucket:
                    self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Calculates the load factor of a HashMap

        Return: load factor value
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the has table
        """
        #check if empty table
        if self._size == 0:
            return self._capacity

        count = 0
        for index in range(self._capacity):
            if self._buckets.get_at_index(index).length() == 0:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Finds the associated value of a provided key

        para key: key of target value

        return: value of key if key is present in has table,
                none otherwise
        """
        #check if empty
        if self._size == 0:
             return

        # calculate which bucket the key would be at
        hash_val = self._hash_function(key)
        hash_val = hash_val % self._capacity

        key_node = self._buckets.get_at_index(hash_val).contains(key)
        if key_node:
            return key_node.value

        #no match found
        return

    def contains_key(self, key: str) -> bool:
        """
        Determines if a key is in a hash table

        param key: target key

        return: True if key exists in hash table, false otherwise
        """
        # check if empty
        if self._size == 0:
            return False

        # calculate which bucket the key would be at
        hash_val = self._hash_function(key)
        hash_val = hash_val % self._capacity

        if self._buckets.get_at_index(hash_val).contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        removes a given key from the has table

        param key: target key to be removed

        Returns: nothing, ._buckets/._size changed if needed
        """
        # check if empty
        if self._size == 0:
            return

        # calculate which bucket the key would be at
        hash_val = self._hash_function(key)
        hash_val = hash_val % self._capacity

        #delete and adjust size
        if self._buckets.get_at_index(hash_val).remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of all key-value pairs
        in the hash table
        """
        #initiate variables
        node_count = 0
        index = 0
        key_val_da = DynamicArray()

        #iterate through each bucket
        while node_count < self._size:
            cur_bucket = self._buckets.get_at_index(index)
            #non-empty bucket, add all node to return arr
            for node in cur_bucket:
                key_val_da.append((node.key, node.value))
                node_count += 1
            index += 1

        return key_val_da

    def clear(self) -> None:
        """
        clears the hash table without changing the capacity
        """
        for index in range(self._capacity):
            self._buckets.set_at_index(index, LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    finds the mode(s) of a provided array

    param da: dynamic array of elements to have mode(s) found

    Returns tuple of an array of value(s) that occur the most, and the amount
     of time occurred in that order
    """
    #initiate variables
    map = HashMap()
    mode_arr = DynamicArray()
    mode_count = 0

    #add vals to hashMap with increase counts/val for repeats
    for index in range(da.length()):
        #get current val of key/element
        element = da.get_at_index(index)
        element_val = map.get(element)
        #inc val of key/element - representing it's count
        if element_val is None:
            element_val = 1
        else:
            element_val += 1
        map.put(element, element_val)

    #get elements and their count from hash map
    key_val_da = map.get_keys_and_values()

    #find mode count
    for index in range(key_val_da.length()):
        # this_tuple = key_val_da.get_at_index(index)
        this_element, this_count = key_val_da.get_at_index(index)
        #same as mode count
        if this_count == mode_count:
            mode_arr.append(this_element)
        #greater than mode count
        elif this_count > mode_count:
            mode_count = this_count
            mode_arr = DynamicArray()
            mode_arr.append(this_element)

    return (mode_arr, mode_count)


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print('\nPDF - find_mode example 1')
    print('-----------------------------')
    da = DynamicArray(['apple', 'apple', 'grape', 'melon', 'peach'])
    mode, frequency = find_mode(da)
    print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}')

    print('\nPDF - find_mode example 2')
    print('-----------------------------')
    test_cases = (
        ['Arch', 'Manjaro', 'Manjaro', 'Mint', 'Mint', 'Mint', 'Ubuntu', 'Ubuntu', 'Ubuntu'],
        ['one', 'two', 'three', 'four', 'five'],
        ['2', '4', '2', '6', '8', '4', '1', '3', '4', '5', '7', '3', '3', '2']
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}\n')

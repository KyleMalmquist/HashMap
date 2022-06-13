# Name: Kyle Malmquist
# OSU Email: Malmquik@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap Implementation
# Due Date: 6/3/2022
# Description: An implementation of a hashmap using open addressing in Python


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
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
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
        Updates the key/value pair in the hash map. If the given key already exists,
        the associated value is replaced by the new value.
        If the load factor is >= 0.5, the table capacity doubles

        param key: the key to be updated
        param value: the value to be updated
        """
        # If the load factor >= 0.5, double the capacity
        if self._size > 0:
            if self.table_load() >= 0.5:
                self.resize_table(self._capacity * 2)

        # get the index
        index = self._hash_function(key) % self._capacity

        # if there is nothing there, insert the new HashEntry
        if self._buckets.get_at_index(index) is None:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1

        # overwrite the value if the key already exists
        elif self._buckets.get_at_index(index).key == key:
            self._buckets.get_at_index(index).value = value
            if self._buckets.get_at_index(index).is_tombstone is True:
                self._buckets.get_at_index(index).is_tombstone = False
                self._size += 1

        # if there is a collision, use quadratic probing to insert the new HashEntry
        else:
            j = 0
            i = index

            # if we run into a tombstone, replace it
            while self._buckets.get_at_index(i) is not None:
                if self._buckets.get_at_index(index).is_tombstone:
                    self._buckets.set_at_index(i, HashEntry(key, value))
                    return

                # overwrite the value if the key already exists
                elif self._buckets.get_at_index(i).key == key:
                    self._buckets.get_at_index(i).value = value
                    return

                else:
                    i = (index + (j ** 2)) % self._capacity
                    j += 1

            self._buckets.set_at_index(i, HashEntry(key, value))
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the table load factor (size / capacity)

        return: the load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets

        return: the number of empty buckets
        """
        count = 0

        # Go through each bucket, and if the bucket is None or a tombstone, increase the count
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            if bucket is None or bucket.is_tombstone:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table

        param new_capacity: the hash tables new capacity
        """
        # if the new capacity is less than one
        # or if the new capacity is less than the current size
        # do nothing
        if new_capacity < 1:
            return
        if new_capacity < self._size:
            return

        # otherwise, create a temporary hash table with the new_capacity
        temp_table = HashMap(new_capacity, self._hash_function)

        # fill the temporary table buckets with the original hash tables data
        # rehashing the data along the way
        for i in range(self._capacity):
            temp_bucket = self._buckets.get_at_index(i)
            if temp_bucket is not None:
                if temp_bucket.is_tombstone is False:
                    temp_table.put(self._buckets.get_at_index(i).key, self._buckets.get_at_index(i).value)

        # overwrite the original hashtable with the temporary hash table
        self._capacity = temp_table._capacity
        self._buckets = temp_table._buckets
        self._size = temp_table._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key

        return: the value associated with the given key
        """
        # get the index
        index = self._hash_function(key) % self._capacity

        if self._buckets.get_at_index(index) is None:
            return None

        # use quadratic probing
        else:
            j = 0
            i = (index + (j ** 2)) % self._capacity

            while self._buckets.get_at_index(i) is not None:
                if self._buckets.get_at_index(i).key == key:
                    if self._buckets.get_at_index(i).is_tombstone is False:
                        return self._buckets.get_at_index(i).value

                j += 1
                i = (index + (j ** 2)) % self._capacity

    def contains_key(self, key: str) -> bool:
        """
        Returns whether or not a key is in the hash map

        return: True if the key is in the hashmap, otherwise False
        """
        if self._size < 1:
            return False

        # get the index
        index = self._hash_function(key) % self._capacity

        # if no value exists return false
        if self._buckets.get_at_index(index) is None:
            return False

        # otherwise, use quadratic probing
        else:
            j = 0
            i = (index + (j ** 2)) % self._capacity

            while self._buckets.get_at_index(i) is not None:
                if self._buckets.get_at_index(i).key == key:
                    if self._buckets.get_at_index(i).is_tombstone is False:
                        return True
                    else:
                        return False

                j += 1
                i = (index + (j ** 2)) % self._capacity

        return False

    def remove(self, key: str) -> None:
        """
        Removes the key and its value if it's in the hashmap

        param key: the key to remove
        """
        # get the index
        index = self._hash_function(key) % self._capacity

        # if no value exists return false
        if self._buckets.get_at_index(index) is None:
            return

        # use quadratic probing
        else:
            j = 0
            i = (index + (j ** 2)) % self._capacity

            while self._buckets.get_at_index(i) is not None:
                if self._buckets.get_at_index(i).key == key:
                    if self._buckets.get_at_index(i).is_tombstone is False:
                        self._buckets.get_at_index(i).is_tombstone = True
                        self._size -= 1
                    return
                j += 1
                i = (index + (j ** 2)) % self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing
        the underlying hash table capacity
        """
        self._size = 0
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(None)

    def get_keys(self) -> DynamicArray:
        """
        Returns all keys stored in the hash map

        return: a dynamic array with all the keys in the hashmap
        """
        ret_arr = DynamicArray()

        # Populate our return array with the keys in the hash table
        for i in range(self._buckets.length()):
            if self._buckets.get_at_index(i) is not None and self._buckets.get_at_index(i).is_tombstone is False:
                ret_arr.append(self._buckets.get_at_index(i).key)

        return ret_arr


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
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

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

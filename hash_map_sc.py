# Name: Kyle Malmquist
# OSU Email: malmquik@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap Implementation
# Due Date: 6/3/2022
# Description: An implementation of a hashmap using separate chaining in Python


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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

        param key: the key to be updated
        param value: the value to be updated
        """
        # get the bucket to modify
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)

        # if the bucket doesn't contain the key
        # insert the key and value, and increase the bucket size by one
        if bucket.contains(key) is None:
            bucket.insert(key, value)
            self._size += 1

        # otherwise, get the node corresponding with the key and overwrite its value
        else:
            node = bucket.contains(key)
            node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        return: the number of empty buckets in the hash table
        """
        count = 0

        # Go through each bucket, and if the bucket is empty (length of 0), increase the count
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the table load factor (size / capacity)

        return: the load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        doesn't change the underlying hash table capacity
        """
        self._size = 0
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table

        param new_capacity: the hash tables new capacity
        """
        # if the new capacity is less than one, do nothing
        if new_capacity < 1:
            return

        # otherwise, create a temporary hash table with the new_capacity
        temp_table = HashMap(new_capacity, self._hash_function)

        # fill the temporary table buckets with the original hash tables data
        # rehashing the data along the way
        for i in range(self._capacity):
            temp_bucket = self._buckets.get_at_index(i)
            for temp_node in temp_bucket:
                temp_table.put(temp_node.key, temp_node.value)

        # overwrite the original hashtable with the temporary hash table
        self._capacity = temp_table._capacity
        self._buckets = temp_table._buckets
        self._size = temp_table._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key

        return: the value associated with the given key
        """
        # get the node associated with the key
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)

        if node is None:
            return None
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns whether or not a key is in the hash map

        return: True if the key is in the hashmap, otherwise False
        """
        # gets the node associated with the key
        index = self._hash_function(key) % self._capacity
        temp_node = self._buckets.get_at_index(index).contains(key)

        if temp_node is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Removes the key and its value if it's in the hashmap

        param key: the key to remove
        """
        index = self._hash_function(key) % self._capacity

        # remove returns True if the key is removed, False otherwise
        result = self._buckets.get_at_index(index).remove(key)

        # decrement the size if True
        if result is True:
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Returns all keys stored in the hash map

        return: a dynamic array with all the keys in the hashmap
        """
        ret_array = DynamicArray()

        # Populate our return array with the keys in the hash table
        for i in range(self._capacity):
            temp_list = self._buckets.get_at_index(i)
            for temp_node in temp_list:
                ret_array.append(temp_node.key)

        return ret_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the most frequently occurring values

    param da: the dynamic array to search
    return: a tuple containing the most frequently occurring values and the number of times they occur
    """
    map = HashMap(da.length() // 3, hash_function_1)

    # add elements of the array to the hash
    # with the values being the number of times the elements appear in the array
    for i in range(da.length()):
        if map.contains_key(da.get_at_index(i)):
            count = map.get((da.get_at_index(i))) + 1
            map.put(da.get_at_index(i), count)
        else:
            count = 1
            map.put(da.get_at_index(i), count)

    ret_arr = DynamicArray()
    max_frequency = 0
    helper_hash = HashMap(da.length() // 3, hash_function_1)

    # if an element has a higher frequency than the elements in the array to return
    # overwrite it and update max frequency
    for i in range(da.length()):
        if map.get(da.get_at_index(i)) > max_frequency:
            ret_arr = DynamicArray()
            ret_arr.append(da.get_at_index(i))
            max_frequency = map.get(da.get_at_index(i))
            helper_hash.put(da.get_at_index(i), 0)

        # otherwise, if it has the same frequency, add it to the array to return
        # helper_hash makes sure we don't add duplicate elements
        elif map.get(da.get_at_index(i)) == max_frequency:
            if helper_hash.contains_key(da.get_at_index(i)) is False:
                ret_arr.append(da.get_at_index(i))
                helper_hash.put(da.get_at_index(i), 0)

    return [ret_arr, max_frequency]

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")

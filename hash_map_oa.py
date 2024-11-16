# Name:Lujia He
# OSU Email:helu@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:6(b)
# Due Date:12-08-2023
# Description:The HashMap class is a dynamic hash map implementation that efficiently stores key-value pairs.
# The put method handles insertion and resizing, ensuring optimal performance.
# Essential functions include resize_table for capacity adjustments, table_load for load factor calculation,
# and empty_buckets for evaluating efficiency. Users can retrieve values with get,
# check key existence with contains_key, and remove entries using remove.
# The get_keys_and_values method returns a DynamicArray of all key-value pairs, while clear resets the hash map.
# Overall, these methods provide a versatile toolset for managing dynamic key-value data in a hash map structure.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
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
        self._index = 0

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

    def put(self, key: str, value: object) -> None:
        """
        Inserts or updates a key-value pair in the hash map.

        :param key: The key to insert or update.
        :param value: The value associated with the key.
        :return: None
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        initial = index
        j = 1
        while True:
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                break
            else:
                if self._buckets[index].key == key:
                    self._buckets[index] = HashEntry(key, value)
                    break
                else:
                    index = (initial + j ** 2) % self._capacity
                    j += 1
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the internal hash map table to the specified capacity.

        :param new_capacity: The new capacity for the hash map table.
        :return: None
        """
        if new_capacity < self._size:
            return
        elif self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        new_buckets = DynamicArray()
        for _ in range(self._capacity):
            new_buckets.append(None)

        arr_key_val = self.get_keys_and_values()
        self._buckets = new_buckets
        self._size = 0
        for i in range(arr_key_val.length()):
            k = arr_key_val[i][0]
            v = arr_key_val[i][1]
            self.put(k, v)
        return

    def table_load(self) -> float:
        """
        Calculates and returns the current load factor of the hash map.

        :return: The load factor as a float.
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Counts and returns the number of empty buckets (null or tombstone) in the hash map.

        :return: The count of empty buckets.
        """
        count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        Retrieves the value associated with the given key.

        :param key: The key to search for.
        :return: The value associated with the key, or None if not found.
        """
        entry = self._get_entry(key)
        if entry:
            return entry.value
        return None

    def _get_entry(self, key: str) -> HashEntry | None:
        """
        Retrieves the hash entry associated with the given key.

        :param key: The key to search for.
        :return: The HashEntry object or None if not found.
        """
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        initial = index
        j = 1
        while self._buckets[index] is not None:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return self._buckets[index]
            else:
                index = (initial + j ** 2) % self._capacity
                j += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the hash map contains the given key.

        :param key: The key to check for.
        :return: True if the key is present, False otherwise.
        """
        entry = self._get_entry(key)
        if entry and not entry.is_tombstone:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key-value pair associated with the given key.

        :param key: The key to remove.
        :return: None
        """
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        initial = index
        j = 1
        while self._buckets[index] is not None:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return
            else:
                index = (initial + j ** 2) % self._capacity
                j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray containing tuples of keys and values in the hash map.

        :return: DynamicArray of (key, value) tuples.
        """
        arr = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                arr.append((self._buckets[i].key, self._buckets[i].value))
        return arr

    def clear(self) -> None:
        """
        Clears the hash map, removing all key-value pairs.

        :return: None
        """
        self.__init__(self._capacity, self._hash_function)

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        while self._index < self._capacity:
            value = self._buckets[self._index]
            if value and not value.is_tombstone:
                self._index += 1
                return value
            self._index += 1
        raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
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

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
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

    print("\nPDF - contains_key example 2")
    print("----------------------------")
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

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
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

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

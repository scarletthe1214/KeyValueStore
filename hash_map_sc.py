# Name:Lujia He
# OSU Email:helu@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:6(a)
# Due Date:12-08-2023
# Description:The HashMap class facilitates dynamic hash map operations, including inserting key-value pairs,
# resizing the table, calculating load factors, counting empty buckets, retrieving values,
# checking key presence, removing pairs, obtaining all key-value pairs, and clearing the map.
# The find_mode function efficiently identifies mode(s)
# and their frequency in a dynamic array using a hash map, returning a tuple with the mode(s) and frequency.


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
        Inserts a key-value pair into the hash map. If the load factor exceeds 1,
        the table is resized to double its current capacity.

        Args:
            key (str): The key to be inserted.
            value (object): The value associated with the key.

        Returns:
            None
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        list = self._buckets[index]
        if not list.contains(key):
            list.insert(key, value)
            self._size += 1
        else:
            for node in list:
                if node.key == key:
                    node.value = value
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map's internal table to the specified capacity.
        Rehashes all existing key-value pairs to fit the new table size.

        Args:
            new_capacity (int): The new capacity for the hash map.

        Returns:
            None
        """
        if new_capacity < 1:
            return
        elif self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        new_buckets = DynamicArray()
        for _ in range(self._capacity):
            new_buckets.append(LinkedList())

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
        Calculates and returns the load factor of the hash map.

        Returns:
            float: The load factor, defined as the ratio of the current size to capacity.
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Counts and returns the number of empty buckets in the hash map.

        Returns:
            int: The count of empty buckets.
        """
        count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Retrieves the value associated with the given key.

        Args:
            key (str): The key to search for.

        Returns:
            object: The value associated with the key, or None if the key is not found.
        """
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        list = self._buckets[index]
        if list.contains(key) is not None:
            return list.contains(key).value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the hash map contains the specified key.

        Args:
            key (str): The key to check for.

        Returns:
            bool: True if the key is present, False otherwise.n
        """
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        list = self._buckets[index]
        return list.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the key and its associated value from the hash map.

        Args:
            key (str): The key to be removed.

        Returns:
            None
        """
        hashcode = self._hash_function(key)
        index = hashcode % self._capacity
        list = self._buckets[index]
        res = list.remove(key)
        if res:
            self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of all key-value pairs in the hash map.

        Returns:
            DynamicArray: A dynamic array containing tuples of key-value pairs.
        """
        arr = DynamicArray()
        for i in range(self._buckets.length()):
            for node in self._buckets[i]:
                arr.append((node.key, node.value))
        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map, resetting it to an empty state.

        Returns:
            None
        """
        self.__init__(self._capacity, self._hash_function)


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the mode(s) in the given dynamic array and returns them along with their frequency.

    Args:
        da (DynamicArray): The dynamic array to find modes in.

    Returns:
        tuple[DynamicArray, int]: A tuple containing a dynamic array of mode(s) and their frequency.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    for i in range (da.length()):
        if not map.contains_key(da[i]):
            map.put(da[i], 1)
        else:
            value = map.get(da[i]) + 1
            map.put(da[i], value)
    cur_max = 0
    cur_arr = DynamicArray()
    arr = map.get_keys_and_values()
    for j in range(arr.length()):
        if arr[j][1] > cur_max:
            cur_max = arr[j][1]
            cur_arr = DynamicArray()
            cur_arr.append(arr[j][0])
        elif arr[j][1] == cur_max:
            cur_arr.append(arr[j][0])
    return cur_arr, cur_max
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

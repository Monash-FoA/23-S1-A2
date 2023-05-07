from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    """
              
    """
    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.hash_tables:ArrayR[tuple[K1,ArrayR[tuple[K2,V]]]] = ArrayR(self.TABLE_SIZES[self.size_index])

        for i in range(len(self.hash_tables)):
            if internal_sizes is None:
                self.internal_sizes = self.TABLE_SIZES[self.size_index]
            else:
                self.internal_sizes = internal_sizes[self.size_index]

            hash_table:ArrayR[tuple[K2,V]] = ArrayR(self.internal_sizes)
            self.hash_tables[i] = (None,hash_table)




    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value



    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """

        hash_value1 = self.hash1(key1)
        #sub_table = self.hash_tables[hash_value1]
        hash_value2 = self.hash2(key2, self.hash_tables[hash_value1][-1])



        for _ in range(self.table_size()):
            if self.hash_tables[hash_value1][0] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    for _ in range(self.internal_sizes):
                        if self.hash_tables[hash_value1][-1][hash_value2] is None:
                            if is_insert:
                                return hash_value1,hash_value2
                            else:
                                raise KeyError(key2)

                else:
                    raise KeyError(key1)

            elif self.hash_tables[hash_value1][0] == key1:

                if is_insert:
                    for _ in range(self.internal_sizes):
                        if self.hash_tables[hash_value1][-1][hash_value2] is None:
                            return hash_value1, hash_value2
                        # if self.hash_tables[hash_value1][-1][hash_value2][0] == key2:
                        # hash_value2 = (hash_value2 + 1) % self.internal_sizes
                        else:
                            hash_value2 = (hash_value2 + 1) % self.internal_sizes
                else:
                    for _ in range(self.internal_sizes):
                        if self.hash_tables[hash_value1][-1][hash_value2] is not None:
                            if self.hash_tables[hash_value1][-1][hash_value2][0] == key2:
                                return hash_value1, hash_value2
                            else:
                                hash_value2 = (hash_value2 + 1) % self.internal_sizes





            else:
                # Taken by something else. Time to linear probe.
                hash_value1 = (hash_value1 + 1) % self.table_size()

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(f"({key1}, {key2}) not found in table")





    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            # Iterate over all top-level keys in the table
            for i in range(self.size):
                if self.table[i] is not None:
                    yield self.table[i][0][0]
        else:
            # Iterate over all keys in the bottom-hash-table for key
            if key not in self:
                return  # Key does not exist in the table
            index = self._hash_func(key)  # Get the index of the top-level key
            for sub_key in self.table[index][1]:
                yield sub_key

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            # Get a list of all top-level keys in the table
            keys_set = []
            for i in range(len(self.hash_tables)):
                if self.hash_tables[i][0] is not None:
                    keys_set.append(self.hash_tables[i][0])
            return keys_set
        else:
            # Get a list of all bottom-level keys for key
            keys_set = []
            for i in range(len(self.hash_tables)):
                if self.hash_tables[i][0] == key:
                    for j in range(len(self.hash_tables[i][-1])):
                        if self.hash_tables[i][-1][j] is not None:
                           keys_set.append(self.hash_tables[i][-1][j][0])
                    return keys_set





    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            values_set = []
            for x in range(len(self.hash_tables)):
                for j in range(len(self.hash_tables[x][-1])):
                    if self.hash_tables[x][-1][j] is not None:
                        values_set.append(self.hash_tables[x][-1][j][-1])
            return values_set

        else:
            values_set = []
            for i in range(len(self.hash_tables)):
                if self.hash_tables[i][0] == key:
                    for j in range(len(self.hash_tables[i][-1])):
                        if self.hash_tables[i][-1][j] is not None:
                            values_set.append(self.hash_tables[i][-1][j][-1])
                    return values_set




    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        index1, index2 = self._linear_probe(key[0], key[-1], False)
        if self.table[index1] is not None and key[1] in self.table[index1]:
            return self.table[index1][key[1]]
        else:
            raise KeyError
        """
        index1, index2 = self._linear_probe(key[0], key[-1], False)
        if self.hash_tables[index1] is not None and key[1] in self.hash_tables[index1]:
            return self.hash_tables[index1][key[1]]
        else:
            raise KeyError

    # setitem was here
    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        """

        index1, index2 = self._linear_probe(key[0],key[1], True)
        #hash_table:ArrayR[tuple[K2, V]] = ArrayR(self.internal_sizes)
        #hash_table[index2] = (key[1], data)
        #if self.hash_tables[index1][-1][index2] == None:
        if self.hash_tables[index1][0] is None:
            self.hash_tables[index1] = (key[0],self.hash_tables[index1][-1])

        self.hash_tables[index1][-1][index2] = (key[1], data)
        #self.hash_tables[index1][-1]


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        empty_no = True
        index1, index2 = self._linear_probe(key[0],key[1], False)
        self.hash_tables[index1][-1][index2] = None
        for _ in range(len(self.hash_tables[index1][-1])):
            if self.hash_tables[index1][-1][index2] is not None:
                empty_no = False
                break

            else:
                index2 = (index2 + 1) % len(self.hash_tables[index1][-1])

        if empty_no:
            self.hash_tables[index1] = (None,self.hash_tables[index1][-1])



    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        new_size_index = self.size_index + 1
        if new_size_index >= len(self.TABLE_SIZES):
            raise IndexError("DoubleKeyTable is too large")
        new_size = self.TABLE_SIZES[new_size_index]

        # Create a new hash table with the larger size
        new_table = DoubleKeyTable(sizes=[new_size], internal_sizes=self.TABLE_SIZES[:self.size_index + 1])

        # Update the hash functions of the new table to match the new size
        new_table.hash1 = self.hash1
        new_table.hash2 = self.hash2

        # Iterate through all the existing items in the current hash table
        for item in self.items():
            # Compute the new hash value based on the updated hash functions of the new table
            key1, key2 = item[0]
            new_hash1 = new_table.hash1(key1)
            new_hash2 = new_table.hash2(key2, new_table.array[new_hash1])

            # Insert the item into the new table using the __setitem__ method
            new_table.__setitem__((key1, key2), item[1])

        # Replace the current hash table with the new table
        self.array = new_table.array
        self.size_index = new_table.size_index

    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.hash_tables)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        count = 0
        for sub_table in self.hash_tables:
            count += len(sub_table)
        return count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

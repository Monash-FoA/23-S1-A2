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

        """
        Doc:
        this init code creates none tuples which will house the k1, and the array storing the tuples of k2,v
        inside the array base on the size given if none is given then
        it will use the given TABLE_SIZES . After that it will iterate through each of the none
        created in the array to make an array on the second part of the tuple and this array contains
        a tuple which will house the k2,v .

        time complexity:
        best case : O(1) as it just initializing the variables
        worst case : O(n*m) where n is the number of hash tables and then the
        m is the size of the internal table hash . This occur as we are simply
        creating a hashtable which house a hashtable



        """
        self.count_low_table = 0
        self.count_top_table = 0
        self.list_internal_sizes = internal_sizes
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.hash_tables:ArrayR[tuple[K1,ArrayR[tuple[K2,V]]]] = ArrayR(self.TABLE_SIZES[self.size_index])
        #self.table_size = len(self.hash_tables)

        for i in range(len(self.hash_tables)):
            if internal_sizes is None:
                self.internal_sizes = self.TABLE_SIZES[self.size_index]
            else:
                self.internal_sizes = internal_sizes[self.size_index]

            hash_table:ArrayR[tuple[K2,V]] = ArrayR(self.internal_sizes)
            hash_table.table_size = len(hash_table)
            hash_table.hash = lambda k: self.hash2(k, hash_table)
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


        Doc:
        for this linear probe first we get the hash value for the key1 and then the
        hash value for the key 2 . after that a for loop is started and using the
        hash value 1 of key 1 to check if it is none at that spot or not . if it is then
        it will  carries on into the key 2 hash value
        and does the same thing as to check if that certain spot is none or not if it is then
        then it will return the hash value index for 1 and 2 .
        Next up is the if the given external table is equalevent to the key one,
        if it is (since te key 1 can store many k2,v in its second part of the tuple) then it
        will go to check if its insert or not if it is it will loop the entire internal table looking
        for an empty spot to place the k2,v if there is then it will return thee index 1 and the index 2
        ,if there isnt then it will update the hashvalue index to continue to loop again to check
        the next slot is empty or not using this formula hash_value2 = (hash_value2 + 1) % self.internal_sizes
        .LAstly for the else , it will also use the hash_value1 = (hash_value1 + 1) % self.table_size
        to move to the next element and start the loop all over again until it reach the end


        time complexity:

        best case : O(1) just putting the keys and values at the none spot on the first
        attempt

        worst case: O(n*m) where the n is the length of the external table and the
        n is the internal table to iterate through the arrays to get the index to
        put the keys and values at



        """

        hash_value1 = self.hash1(key1)
        hash_value2 = self.hash2(key2, self.hash_tables[hash_value1][-1])



        for _ in range(self.table_size):
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

                        else:
                            # Taken by something else. Time to linear probe.
                            hash_value2 = (hash_value2 + 1) % self.internal_sizes
                else:
                    for _ in range(self.internal_sizes):
                        if self.hash_tables[hash_value1][-1][hash_value2] is not None:
                            if self.hash_tables[hash_value1][-1][hash_value2][0] == key2:
                                return hash_value1, hash_value2
                            else:
                                # Taken by something else. Time to linear probe.
                                hash_value2 = (hash_value2 + 1) % self.internal_sizes





            else:
                # Taken by something else. Time to linear probe.
                hash_value1 = (hash_value1 + 1) % self.table_size

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


        Doc:
        this iter keys takes the yield function that yields the key for the hash
        table if the key argument is none then it will iterate the top level keys
        in the table if the key is given and not none then it will iterate through \
        the internal list and yield it and that specific key spot given .

        Time complexity:

        best case:

        worst case:

        """
        if key is None:
            # Iterate over all top-level keys in the table
            for top_keys in self.hash_tables:
                if top_keys[0] is not None:
                    yield top_keys[0]

        # if key is not none:
        else:
            for i in range(len(self.hash_tables)):
                if self.hash_tables[i][0] == key:
                    for j in range(len(self.hash_tables[i][-1])):
                        if self.hash_tables[i][-1][j] is not None:
                            yield self.hash_tables[i][-1][j][0]


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
        if key is None:
            # Iterate over all top-level keys in the table
            for i in range(len(self.hash_tables)):
                for top_keys in self.hash_tables[i][-1]:
                    if top_keys is not None:
                        yield top_keys[-1]

        # if key is not none:

        else:
            # Get a list of all bottom-level keys for key
            for i in range(len(self.hash_tables)):
                if self.hash_tables[i][0] == key:
                    for j in range(len(self.hash_tables[i][-1])):
                        if self.hash_tables[i][-1][j] is not None:
                           yield self.hash_tables[i][-1][j][-1]

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
        if self.hash_tables[index1][0] is None:
            self.hash_tables[index1] = (key[0],self.hash_tables[index1][-1])
            self.count_top_table += 1
        self.hash_tables[index1][-1][index2] = (key[1], data)
        self.count_low_table +=1
        self.external_yes = False
        self.internal_yes = False

        #internal table
        if self.count_low_table > len(self.hash_tables[index1][-1]) / 2:
            self.internal_yes = True
            self.key2_need_resize = self.hash_tables[index1][0]
            self._rehash()
            self.internal_yes = False

        #external table
        if self.count_top_table > len(self.hash_tables) / 2:
            self.external_yes = True
            self.key1_need_resize = self.hash_tables[index1][0]
            self._rehash()
            self.external_yes = False

        #if self.count_top_table > len(self.hash_tables) / 2:
            #self._rehash()


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        empty_no = True
        index1, index2 = self._linear_probe(key[0],key[1], False)
        self.hash_tables[index1][-1][index2] = None
        self.count_low_table -= 1
        for _ in range(len(self.hash_tables[index1][-1])):
            if self.hash_tables[index1][-1][index2] is not None:
                empty_no = False
                break

            else:
                index2 = (index2 + 1) % len(self.hash_tables[index1][-1])

        if empty_no:
            self.hash_tables[index1] = (None,self.hash_tables[index1][-1])
            self.count_top_table -= 1


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """



        #for internal table
        #if self.count_low_table < (self.list_internal_sizes[self.size_index]) / 2 :
        if self.internal_yes:
            self.size_index += 1
            if self.size_index >= len(self.list_internal_sizes):
                self.size_index = 0
                return
            else:
            # if self.size_index < len(self.list_internal_sizes):
                self.internal_sizes = self.list_internal_sizes[self.size_index]
                for i in range(len(self.hash_tables)):
                    if self.hash_tables[i][0] == self.key2_need_resize:
                        old_hash_table_internal = self.hash_tables[i][-1]
                        old_key1 = self.hash_tables[i][0]
                        new_hash_table_internal: ArrayR[tuple[K2, V]] = ArrayR(self.internal_sizes)  # made chg here
                        new_hash_table_internal.table_size = len(new_hash_table_internal)
                        self.hash_tables[i] = (old_key1, new_hash_table_internal)
                        self.count_low_table = 0
                        for item in old_hash_table_internal:
                            if item is not None:
                                key, value = item
                                index1, index2 = self._linear_probe(old_key1, key, True)
                                self.hash_tables[index1][-1][index2] = (key, value)
                                self.count_low_table += 1
                        break

                self.size_index = 0
                return







        # for the top / outer table
        if self.external_yes:
            self.size_index += 1
            if self.size_index >= len(self.TABLE_SIZES):
                self.size_index = 0
                return

        #if self.size_index < len(self.TABLE_SIZES):
            else:
                new_size = self.TABLE_SIZES[self.size_index]
                # for i in range(len(self.hash_tables)):
                old_hash_table_outer = self.hash_tables
                new_hash_table_outer: ArrayR[tuple[K1, ArrayR[tuple[K2, V]]]] = ArrayR(new_size)
                self.hash_tables = new_hash_table_outer
                for j in range(len(self.hash_tables)):
                    hash_table: ArrayR[tuple[K2, V]] = ArrayR(self.internal_sizes)
                    hash_table.table_size = len(hash_table)
                    hash_table.hash = lambda k: self.hash2(k, hash_table)
                    self.hash_tables[j] = (None, hash_table)




                # self.hash_tables.table_size = len(new_hash_table_outer)
                self.count_top_table = 0
                for i in range(len(old_hash_table_outer)):
                    if old_hash_table_outer[i] is not None:
                        #if len(old_hash_table_outer[i][-1]) == self.internal_sizes:
                        for j in range(len(old_hash_table_outer[i][-1])):
                            if old_hash_table_outer[i][-1][j] is not None:
                                key1 = old_hash_table_outer[i][0]
                                key2 = old_hash_table_outer[i][-1][j][0]
                                value = old_hash_table_outer[i][-1][j][-1]
                                index1, index2 = self._linear_probe(key1, key2, True)
                                if self.hash_tables[index1][0] is None:
                                    self.hash_tables[index1] = (key1, self.hash_tables[index1][-1])
                                    self.count_top_table += 1
                                self.hash_tables[index1][-1][index2] = (key2, value)
                                self.count_low_table += 1
                self.size_index = 0

                return










    @property
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
        for i in range(len(self.hash_tables)):
            for j in range(len(self.hash_tables[i][-1])):
                if self.hash_tables[i][-1][j] is not None:
                    count += 1  # len(sub_table)
            break
        return count

        #return len(self.keys())

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

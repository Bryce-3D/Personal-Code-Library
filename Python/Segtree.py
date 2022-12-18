class Segtree:
    '''
    A basic segtree implementation.
    Used to perform a specific associative operation on any 
    contiguous subarray of a fixed number of elements in `O(logn)` 
    time rather than `O(n)`.
    Everything is 0-indexed unless otherwise stated.

    The array of items being queried on will be referred to as 
    the "underlying array".
    `n` is the number of items in the underlying array.
    `T` is the type of the items in the underlying array.

    Implementation uses `None` to pad out the data structure 
    to a perfect binary tree. 

    Raises `IndexError`s to help with debugging.

    Public Methods Summary:
        __init__(self, a, op)
            Creates a segtree with underlying array a and join operation op
        query(self, L, R)
            Result of applying the operation on interval [L:R]
        update(self, ind, val)
            Updates an element of the underlying array and the whole segtree
        get(self, ind)
            Returns specified element of the underlying array
        arr(self)
            Returns a copy of the underlying array
    '''
    
    #Fields
    _n = None      #Number of items in the underlying list
    _op = None     #Join operator; modified to handle `None` inputs
    _seg = None    #Array to store the main segtree
    _span = None   #span[i] = interval [L:R] corresponding to seg[i]
    _l = None      #Length of seg



    def __init__(self, a: list, op: 'function') -> 'Segtree':
        '''
        Initializes a segtree from an array and join operator.

        Time complexity: `O(n)`

        Parameters
        ----------
        `a` : list
            The inputted array
        `op` : function
            Operation to join segments
        
        Returns
        -------
            A segtree initialized from `a` and join operator `op`
        '''
        
        #Initialize other fields
        self.n = len(a)
        #Modify `op` to handle `None` inputs
        def op_none(a,b):
            if a == None and b == None:
                return None
            elif a == None:
                return b
            elif b == None:
                return a
            else:
                return op(a,b)
        self.op = op_none

        #Calculate the length 
        k = 2 ** Segtree._ceil_log_2(self.n)   #Number of leaves (padded)
        self.l = 2*k - 1                      #Number of nodes

        #Initialize `seg`` with `None`s. Unused nodes will remain as `None`
        self.seg = [None for i in range(self.l)]
        #Initialize `span` with [n:n], the empty interval at the end
        self.span = [[self.n,self.n] for i in range(self.l)]

        #Initialize leaves of `seg` and `span`
        for i in range(self.n):
            #Copy `a` into the leaves of `seg`
            self.seg[i + k-1] = a[i]
            #Initilize `span` for the leaves
            self.span[i + k-1] = [i,i+1]
        
        #Initialize non-leaf nodes of `seg` and `span` bottom up
        for i in range(k-2,-1,-1):
            #Run the join operation to fill non-leaf nodes of `seg`
            self.seg[i] = self.op(self.seg[2*i+1], self.seg[2*i+2])
            #Join intervals of children to fill non-leaf nodes of `span`
            self.span[i] = [self.span[2*i+1][0], self.span[2*i+2][1]]



    def query(self, L: int, R: int):
        '''
        Returns the result of applying `op` on the interval `[L:R]` 
        of the underlying array.
        Requires `0 <= L < R <= n`.

        Time complexity: `O(logn)`

        Parameters
        ----------
        `L` : int
            Left end of the queried range (inclusive)
        `R` : int
            Right end of the queried range (exclusive)
        
        Returns
        -------
        The result of applying the join operation on the interval `[L:R]`
        
        Raises
        ------
        IndexError
            When querying an invalid interval
        '''
        
        #Check that [L:R] is a valid interval
        if L < 0 or R > self.n or L >= R:
            msg = f'[L,R] = [{L},{R}] but segtree only has {self.n} elements'
            raise IndexError(msg)
        return self._help_me_query(L, R, 0)
    
    def _help_me_query(self, L: int, R: int, i: int):
        # Helper function for query.
        # Returns the result of applying `op` on the interval `a[L:R]`
        # Has an extra input `i` that represents the index of `seg` and `span` 
        # currently being looked at to help traverse the segtree.
        # [L:R] will always be contained entirely inside self.span[i].

        #If [L:R] is exactly self.span[i], return the value in seg[i]
        L_0 = self.span[i][0]   #Left end of seg[i]'s interval
        R_0 = self.span[i][1]   #Right end of seg[i]'s interval
        if L == L_0 and R == R_0:
            return self.seg[i]
        
        #Check intervals of children of seg[i]
        l = self.span[2*i+1][0]   #Left end of left child
        m = self.span[2*i+1][1]   #Border of left and right child
        r = self.span[2*i+2][1]   #Right end of right child
        
        #If [L:R] is entirely in the left child of span[i]
        if R <= m:
            return self._help_me_query(L, R, 2*i+1)
        #If [L:R] is entirely in the right child of span[i]
        elif L >= m:
            return self._help_me_query(L, R, 2*i+2)
        #If [L:R] hits both the left and right child of span[i]
        else:
            #Ans of part of [L:R] in left subtree
            ans_L = self._help_me_query(L, m, 2*i+1)
            #Ans of part of [L:R] in right subtree
            ans_R = self._help_me_query(m, R, 2*i+2)
            #Join to get the ans
            return self.op(ans_L, ans_R)



    def update(self, ind: int, val) -> None:
        '''
        Updates the element at index `ind` to `val` and updates the 
        segtree accordingly.
        Requires `-n <= ind <= n-1`.
        If `ind < 0`, then it counts from the back similarly to lists.

        Time complexity: `O(logn)`

        Parameters
        ----------
        `ind` : int
            The index being updated
        `val`
            The new value to put in index `ind`

        Raises
        ------
        IndexError
            When `ind` is out of bounds
        '''
        
        #Check that ind is a valid index
        if ind >= self.n or ind < -self.n:
            raise IndexError(f'Getting from index out of range: ind = {ind}')
        #If ind < 0, shift it back up to be positive
        if ind < 0:
            ind += self.n
        
        k = self.l//2       #Number of non-leaf nodes
        i = k + ind         #Index of [ind:ind+1] in seg
        self.seg[i] = val   #Update seg[i]
        while i > 0:        #While not yet at root, go to parent and update
            i = (i-1)//2
            self.seg[i] = self.op(self.seg[2*i+1], self.seg[2*i+2])



    def get(self, ind: int):
        '''
        Returns the item at index `ind` in the underlying array.
        Requires `-n <= ind <= n-1`.
        If `ind < 0`, then it counts from the back similarly to lists.

        Runtime: `O(1)`

        Parameters
        ----------
        ind : int
            The index we want to get

        Returns
        -------
        The element at index `ind` of the underlying array

        Raises
        IndexError
            When an `ind` is out of bounds
        '''
        #Check that ind is a valid index
        if ind >= self.n or ind < -self.n:
            raise IndexError(f'Getting from index out of range: ind = {ind}')
        
        #If ind < 0, shift it back up to be positive
        if ind < 0:
            ind += self.n

        k = self.l//2   #Number of non-leaf nodes
        i = k + ind     #Index of [ind:ind+1] in seg
        return self.seg[i]



    def arr(self):
        '''
        Creates and returns a copy of the underlying array.

        Time complexity: `O(n)`

        Returns
        -------
        A copy of the underlying array
        '''
        k = self.l//2                 #Number of non-leaf nodes
        return self.seg[k:k+self.n]   #Slice non-None part of bottom layer



    @staticmethod
    def _ceil_log_2(n):
        # Utility function to get the value of 
        #     ceil(log_2(n))
        # Used to get the size of the array needed to store the segtree.
        
        ans = 0
        exact = True   #True iff n is an exact power of 2

        #Iterate from LSB to MSB
        while n > 1:
            #If any bit except the MSB is 1, then not exact
            if n%2 == 1:
                exact = False
            #floor_log_2(n) = number of bits - 1
            ans += 1
            n >>= 1
        
        #Add an extra 1 if it is not exact
        if exact:
            return ans
        else:
            return ans+1

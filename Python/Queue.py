class Queue:
    '''
    Initializes a queue.
    Implemented by using 2 stacks.
    Enqueue places elements on top of stack 1.
    Dequeue takes elements from the top of stack 2.
    When an element is dequeued while stack 2 is empty, stack 1 is 
    emptied onto stack 2 in reverse order by popping each element 
    in stack 1 and pushing it into stack 2 until stack 1 is empty.
    '''

    #Instance Attributes
    #_stack_1 - Internal stack 1
    #_stack_2 - Internal stack 2
    #_n       - Number of elements currently in the queue

    def __init__(self):
        '''Initializes an empty Queue'''
        self.stack_1 = []
        self.stack_2 = []
        self.n = 0
    
    def enq(self, k):
        '''Enqueues an element `k` at the back of the queue'''
        self.n += 1
        self.stack_1.append(k)
    
    def deq(self):
        '''
        Dequeues and returns the element at the front of the queue.
        If the queue is empty, it returns `None`.
        '''
        if self.n == 0:
            return None
        
        self.n -= 1
        #If stack 2 is empty
        if len(self.stack_2) == 0:
            #Transfer everything from stack 1 to stack 2
            while len(self.stack_1) != 0:
                next = self.stack_1.pop()
                self.stack_2.append(next)
        #Return the top of stack 2
        return self.stack_2.pop()
    
    def clear(self):
        '''Empties the queue'''
        self.stack_1 = []
        self.stack_2 = []
        self.n = 0
    
    def len(self):
        '''Returns the current length of the queue'''
        return self.n

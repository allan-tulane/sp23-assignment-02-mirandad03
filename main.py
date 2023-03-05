"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))

    def __add__(self, other):
        return BinaryNumber(self.decimal_val + other.decimal_val)

    def __sub__(self, other):
        return BinaryNumber(self.decimal_val - other.decimal_val)
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y

def subquadratic_multiply(x_bin, y_bin):
    
    # pad binary vectors to ensure even length
    x_bin, y_bin = pad(x_bin, y_bin)
    
    # base case: single bit multiplication
    if len(x_bin) == 2:
        return BinaryNumber(int(x_bin[0]) * int(y_bin[0]))
    
    # split input binary vectors in half
    a, b = split_number(x_bin)
    c, d = split_number(y_bin)
    
    # compute products of the halves
    ac = subquadratic_multiply(a, c)
    bd = subquadratic_multiply(b, d)
    
    # compute product of (a+b) and (c+d) using Karatsuba-Ofman recursion
    ab = binary2int(a + b)
    cd = binary2int(c + d)
    ab_cd = subquadratic_multiply(ab.binary_vec, cd.binary_vec)
    ad_bc = ab_cd - ac - bd
    
    # combine products using Karatsuba-Ofman formula
    return ac + bit_shift(BinaryNumber(ad_bc), len(x_bin)//2) + bit_shift(bd, len(x_bin))

def multiply(a, b):
    # Convert both values to binary
    bin_a = Binary(a)
    bin_b = Binary(b)
    
    # Multiply the binary values and convert the result to decimal
    result = Binary(bin_a.binary_val * bin_b.binary_val, decimal=False)
    
    return result

def time_multiply(x, y, f):
    start = time.time()
    result = f(x.binary_vec, y.binary_vec)
    timetaken = (time.time() - start)*1000
    print("Time:", timetaken)
    return timetaken

test_multiply()
x = BinaryNumber(1234)
y = BinaryNumber(5678)
time_multiply(x, y, subquadratic_multiply)
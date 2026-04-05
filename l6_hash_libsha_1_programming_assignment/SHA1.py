"""
    In this program we will program the SHA-1 algorithm.
    Note that this algorithm is no longer a secure hash function.
    However, the SHA-2 algorithms operate in a similar way and
    are considered secure.

    Throughout the program we will work on a binary string.
    The standard way to convert a message to a binary string is to
    first encode the message using UTF-8. We can do this in Python
    by using the encode function. If the m is the message, then
    m.encode() converts m to UTF-8. We can then convert
    this to a binary string in the following way (see the 3rd to last
    line of this code):

    s = ''.join(format(x, 'b').zfill(8) for x in m.encode())

    The variable s now holds a binary string that has length
    that is a multiple of 8.
"""

"""
    The following bitwise functions preform an operation on each
    bit of a binary string. The "and" operator works in the 
    following way: 
        0 and 0 --> 0
        0 and 1 --> 0
        1 and 0 --> 0
        1 and 1 --> 1

    The "xor" below is the exclusive or operator. This acts in the
    same way as it did in the AES algorithm. That is:
        0 xor 0 --> 0
        0 xor 1 --> 1
        1 xor 0 --> 1
        1 xor 1 --> 0

    The compliment operator will take the opposite value of each bit.
    That is 1 --> 0 and 0 --> 1.
"""


def bitwise_and(a, b):
    product = ""
    for i in range(len(a)):
        if (a[i] == b[i]) and a[i] == "1":
            product = product + "1"
        else:
            product = product + "0"
    return product


def bitwise_xor(a, b):
    xor = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            xor = xor + "0"
        else:
            xor = xor + "1"
    return xor


def bitwise_comp(a):
    comp = ""
    for i in range(len(a)):
        if a[i] == "1":
            comp = comp + "0"
        else:
            comp = comp + "1"
    return comp


def ch(x, y, z):
    # Add code here. See the NIST document for details of this function.
    # Function should return a binary string.
    return bitwise_xor(bitwise_and(x, y), bitwise_and(bitwise_comp(x), z))


def parity(x, y, z):
    # Add code here. See the NIST document for details of this function.
    # Function should return a binary string.
    return bitwise_xor(bitwise_xor(x, y), z)


def maj(x, y, z):
    # Add code here. See the NIST document for details of this function.
    # Function should return a binary string.
    return bitwise_xor(bitwise_xor(bitwise_and(x, y), bitwise_and(x, z)), bitwise_and(y, z))


def add(x, y):
    """
        Addition in SHA-1 is done modulo 2^32.
        This method should first convert x and y to integers
        X and Y. Then Z = (X + Y) (mod 2^32).
        The method should then return a 32-bit binary string of Z.
    """
    # Add code here
    X = int(x, 2)
    Y = int(y, 2)
    Z = (X + Y) % (2**32)
    return format(Z, 'b').zfill(32)


# The left_circular_shift functions applies a rotational
# shift by moving each index to the left n indices. The
# furthest left bits get appended to the end.
def left_circular_shift(w, n):
    if n == 0:
        return w
    else:
        temp = w[0]
        w = w[1: len(w)] + temp
        return left_circular_shift(w, n-1)


def padding(message):
    # Each message block must be 512 bits. If the
    # binary string of the message is not a multiple of 512,
    # then it must be padded with extra binary bits.
    # See the NIST document for details of this function.

    # Add code here.
    # Function should return a binary string that has length a multiple of 512.
    l = len(message)
    message += "1"
    k = (448 - (l + 1) % 512) % 512
    message += "0" * k
    message += format(l, 'b').zfill(64)
    return message


# The parse_data function breaks a message into 512 bit blocks.
def parse_data(message):
    if len(message) % 512 != 0:
        message = padding(message)
    data_list = []
    for i in range(0, len(message), 512):
        data_list.append(message[i: i+512])
    return data_list


def f(x, y, z, n):
    # Add code here. See the NIST document for details of this function.
    # Function should return a binary string.
    if 0 <= n <= 19:
        return ch(x, y, z)
    elif 20 <= n <= 39:
        return parity(x, y, z)
    elif 40 <= n <= 59:
        return maj(x, y, z)
    elif 60 <= n <= 79:
        return parity(x, y, z)


def sha1(message):
    message_list = parse_data(message)
    # H and K are lists of initial constants given from the NIST document.
    # Each element of the list below is a hex number converted to a binary string.
    H = [format(0x67452301, "b").zfill(32), format(0xefcdab89, "b").zfill(32),
         format(0x98badcfe, "b").zfill(32), format(0x10325476, "b").zfill(32),
         format(0xc3d2e1f0, "b").zfill(32)]
    K = [format(0x5a827999, "b").zfill(32), format(0x6ed9eba1, "b").zfill(32),
         format(0x8f1bbcdc, "b").zfill(32), format(0xca62c1d6, "b").zfill(32)]

    # Add code below for the SHA-1 algorithm.
    # See the NIST document for details of this algorithm.

    for block in message_list:
        W = []
        for t in range(16):
            W.append(block[t * 32:(t + 1) * 32])
        for t in range(16, 80):
            W.append(left_circular_shift(
                bitwise_xor(bitwise_xor(bitwise_xor(W[t - 3], W[t - 8]), W[t - 14]), W[t - 16]),
                1))

        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]

        for t in range(80):
            if 0 <= t <= 19:
                K_t = K[0]
            elif 20 <= t <= 39:
                K_t = K[1]
            elif 40 <= t <= 59:
                K_t = K[2]
            else:
                K_t = K[3]

            T = add(add(add(add(left_circular_shift(a, 5), f(b, c, d, t)), e), K_t), W[t])
            e = d
            d = c
            c = left_circular_shift(b, 30)
            b = a
            a = T

        H[0] = add(a, H[0])
        H[1] = add(b, H[1])
        H[2] = add(c, H[2])
        H[3] = add(d, H[3])
        H[4] = add(e, H[4])

    return H[0] + H[1] + H[2] + H[3] + H[4]


test_message = "test message"

# Convert to a binary string.
test_binary_string = ''.join(format(x, 'b').zfill(8) for x in test_message.encode())
s = sha1(test_binary_string)
print(hex(int(s, 2)))

# x = base 10 [str], d = set of ordered unique 'digits' [str]
def DecToBaseN(x, d):
    # k = helper, b = result, n = size of set
    k = int(x)
    b = ''
    n = len(d)

    # check if x is within n
    if k < n - 1:
        return d[k]
    # if not, divide and mod by n until x < n
    else:
        while k > n - 1:
            r = k % n
            b = d[r] + b
            k //= n
        if k > 0:
            #b += d[k]
            b = d[k] + b
    return b

# x = base N number as [str], d = set of ordered unique 'digits' [str]
def BaseNToDec(x, d):
    # b = result, n = num digits in x, m = size of set
    b = 0
    n = len(x)
    m = len(d)

    # for sym in x, get base 10 index of sym and multiply by m^i ( 0 < i < n )
    j = 0
    for i in range(n - 1, -1, -1):
        a = int(d.index(x[i]))
        b += ( a * ( m ** j ) )
        j += 1
    return str(b)


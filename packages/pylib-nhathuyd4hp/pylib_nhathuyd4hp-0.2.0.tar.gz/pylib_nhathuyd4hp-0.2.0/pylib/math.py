def sum(*args: int | float) -> int | float:
    sum = 0
    for p in args:
        sum = sum + p
    return sum
def separator(symbol='-', length=50) -> None:
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f'{symbol * length}')
            result = func(*args, **kwargs)
            return result
        return wrapper 
    return decorator

def line_break(symbol1='*', symbol2='*', length=70, second_symbol=True):
    # Prints a line break
    if second_symbol:
        print()
    print(symbol1 * length)
    if second_symbol:
        print(symbol2 * length)
        print()
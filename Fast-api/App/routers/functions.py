
def format_date(date: str) -> str:
    try:
        items = list(date.split('-'))
    except IndexError:
        items = list(date.split('/'))

    new_date = f'{items[2]}-{items[1]}-{items[0]}'
    return new_date



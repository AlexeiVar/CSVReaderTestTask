import csv

import utils


def aggregate(reader: csv.DictReader | list, arg: str) -> dict:
    column, operation = arg.split('=')
    if operation in utils.aggregate_dict:
        try:
            result = utils.aggregate_dict[operation](reader, column)
        except ValueError:
            raise ValueError('aggregate only supports numbers')
    else:
        raise ValueError('aggregate does not accept this operation')
    data = {operation: [result]}
    return data


def where(reader: csv.DictReader | list, arg: str) -> list:
    separators = ['<', '=', '>']
    column = ''
    operation = None
    value = ''
    # Я уверен, что есть метод лучше, но пришел к такому решению
    for symbol in arg:
        if symbol in separators:
            operation = symbol
            continue
        if not operation:
            column += symbol
        else:
            value += symbol
    try:
        value = float(value)
        number = True
    except ValueError:
        number = False
    if operation in utils.where_dict:
        data = utils.where_dict[operation](reader, column, value, number)
    else:
        raise ValueError('where does not accept this operation')
    return data


def order_by(reader: csv.DictReader | list, arg: str) -> list:
    column, operation = arg.split('=')
    unsorted = []
    for line in reader:
        # Насколько я понял без использования pandas нельзя нормально использовать встроенные инструменты
        # для обработки csv файла со смешенными данными, поэтому вручную меняю через try except
        try:
            line[column] = float(line[column])
        except ValueError:
            pass
        unsorted.append(line)
    if operation in utils.order_by_dict:
        data = utils.order_by_dict[operation](unsorted, column)
    else:
        raise ValueError('order-by does not accept this operation')
    return data

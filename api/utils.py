def get_sizes_type_of_number(sizes):
    result = []

    for size in sizes:
        if float(size).is_integer():
            result.append(int(size))
            continue
        result.append(float(size))

    return result

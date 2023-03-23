def to_csvline(lst):
    def to_column(v):
        return '"' + str(v).replace('"', '""') + '"'

    quoted = []
    for v in lst:
        if isinstance(v, str):
            quoted.append(to_column(v))
        else:
            quoted.append(str(v))
    return ",".join(quoted)

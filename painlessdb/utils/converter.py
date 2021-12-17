def datetimeToStr(datetime_obj) -> str:
    attrs = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    dt_value_list = [getattr(datetime_obj, attr) for attr in attrs]
    dt_str_value = "".join(str(x) + '|' for x in dt_value_list)
    return dt_str_value


def singleQuoteToDoubleQuote(data):
    cList = list(data)
    inDouble = False
    inSingle = False
    for i, c in enumerate(cList):
        if c == "'":
            if not inDouble:
                inSingle = not inSingle
                cList[i] = '"'
        elif c == '"':
            inDouble = not inDouble
    doubleQuoted = "".join(cList)
    return doubleQuoted

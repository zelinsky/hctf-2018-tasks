def convert_to_list(text):
    lst = []
    for char in text:
        lst.append(ord(char))
    return lst


def convert_to_string(lst):
    text = ''
    for item in lst:
        text += chr(item)
    return text

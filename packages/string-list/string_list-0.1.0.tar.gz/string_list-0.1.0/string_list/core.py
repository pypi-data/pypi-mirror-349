from typing import Union


def list_from_string(string: str, delim=',', strip=True) -> list:
    if strip:
        return [item.strip() for item in string.split(delim)]
    else:
        return [item for item in string.split(delim)]


def string_from_list(any_iter: Union[list, set], delim=',', quoted=False):
    if any_iter is None:
        return None
    if quoted:
        return delim.join([f"'{i}'" for i in any_iter if i is not None])
    else:
        return delim.join([str(i) for i in any_iter if i is not None])


def list_from_any(input_val: Union[list, str, int], return_items_as_int=False):
    if isinstance(input_val, list):
        input_val_list = input_val
    else:
        input_val_list = list_from_string(str(input_val))
    if return_items_as_int:
        return [int(m) for m in input_val_list]
    else:
        return [str(m) for m in input_val_list]


def case_insensitive_update(keywords_set: set, new_keywords: set):
    assert isinstance(keywords_set, set) and isinstance(new_keywords, set)
    normalized_keywords = {k.lower(): k for k in keywords_set}
    for keyword in new_keywords:
        normalized_keyword = keyword.lower()
        if normalized_keyword not in normalized_keywords:
            normalized_keywords[normalized_keyword] = keyword
        elif keyword.istitle():
            normalized_keywords[normalized_keyword] = keyword
    return set(normalized_keywords.values())


def str_enumerate(input_val: Union[list, str, int], start=0):
    if isinstance(input_val, list):
        input_val_list = input_val
    else:
        input_val_list = list_from_string(str(input_val))
    return {str(k): v for k, v in dict(enumerate(input_val_list, start=start)).items()}

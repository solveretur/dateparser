# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dateparser.search.search import DateSearchWithDetection

_search_with_detection = DateSearchWithDetection()


def search_dates(text, languages=None, settings=None):
    """Find all substrings of the given string which represent date and/or time and parse them.

        :param text:
            A string in a natural language which may contain date and/or time expressions.
        :type text: str|unicode
        :param languages:
            A list of two letters language codes.e.g. ['en', 'es']. If languages are given, it will not attempt
            to detect the language.
        :type languages: list
        :param settings:
               Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
        :type settings: dict


        :return: Returns list of tuples containing pairs:
                 substrings representing date and/or time and corresponding :mod:`datetime.datetime` object.
                 Returns None if no dates that can be parsed are found.
        :rtype: list
        :raises: ValueError - Unknown Language

        >>> search_dates('The first artificial Earth satellite was launched on 4 October 1957.')
        [('on 4 October 1957', datetime.datetime(1957, 10, 4, 0, 0))]

        """
    # TUTAJ ZWRACA WYNIKI
    result = _search_with_detection.search_dates(text=text, languages=languages, settings=settings)
    if result['Dates']:
        return replace_data_in_tuples(result['Dates'])


def replace_for_dmy(my_datetime_object):
    from dateparser.parser import UNDEFINED
    from dateparser.parser import MyDateTime
    if isinstance(my_datetime_object, MyDateTime):
        if my_datetime_object.day is not None and my_datetime_object.month is not None:
            if my_datetime_object.day is not UNDEFINED and my_datetime_object.day is not UNDEFINED:
                if int(my_datetime_object.day) <= 12 and int(my_datetime_object.month) <= 12:
                    tmp = my_datetime_object.day
                    my_datetime_object.day = my_datetime_object.month
                    my_datetime_object.month = tmp
                    return str(my_datetime_object)
    return str(my_datetime_object)


def is_substring_matches_to_replace(substring):
    import regex as re
    pattern = re.compile(r'(?<!\d)\d{1,2}[-|\s|\.|\/]\d{1,2}[-|\s|\.|\/]\d{2,4}(?!\d)')
    re1 = re.findall(pattern, substring)
    if re1:
        return True
    pattern2 = re.compile(r'(?<!\d)\d{1,2}[-|\s|\.|\/]\d{1,2}(?!\d)(?![-|\s|\.|\/])')
    return re.findall(pattern2,substring)


def replace_data_in_tuples(tuple_list):
    return [(k, replace_for_dmy(v)) if is_substring_matches_to_replace(k) else (k, str(v)) for (k, v) in tuple_list]

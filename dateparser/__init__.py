# -*- coding: utf-8 -*-
__version__ = '0.7.0-Improved'

from .date import DateDataParser
from .conf import apply_settings
import dateparser.search as search
from dateparser import my_datefinder as datefinder
import regex as re

_default_parser = DateDataParser()


@apply_settings
def parse(date_string, date_formats=None, languages=None, locales=None, region=None, settings=None):
    """Parse date and time from given date string.

    :param date_string:
        A string representing date and/or time in a recognizably valid format.
    :type date_string: str|unicode

    :param date_formats:
        A list of format strings using directives as given
        `here <https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior>`_.
        The parser applies formats one by one, taking into account the detected languages/locales.
    :type date_formats: list

    :param languages:
        A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
        If locales are not given, languages and region are used to construct locales for translation.
    :type languages: list

    :param locales:
        A list of locale codes, e.g. ['fr-PF', 'qu-EC', 'af-NA'].
        The parser uses locales to translate date string.
    :type locales: list

    :param region:
        A region code, e.g. 'IN', '001', 'NE'.
        If locales are not given, languages and region are used to construct locales for translation.
    :type region: str|unicode

    :param settings:
        Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
    :type settings: dict

    :return: Returns :class:`datetime <datetime.datetime>` representing parsed date if successful, else returns None
    :rtype: :class:`datetime <datetime.datetime>`.
    :raises: ValueError - Unknown Language
    """
    parser = _default_parser

    if any([languages, locales, region, not settings._default]):
        parser = DateDataParser(languages=languages, locales=locales,
                                region=region, settings=settings)

    data = parser.get_date_data(date_string, date_formats)

    if data:
        return data['date_obj']


def find_dates(text):
    substrings = find_dates_substring(text)
    dates = []
    for s, i in substrings:
        substring = s
        if (remove_only_one_digit_substrings(substring)):
            continue
        parsed_date_pl = parse(substring, languages=["pl"])
        parsed_date_en = parse(substring, languages=["en"])
        search_results = search.search_dates(substring, languages=["pl"])
        if parsed_date_en is not None and parsed_date_pl is not None and replace_days_and_months(str(parsed_date_pl)) == str(parsed_date_en) and matches_ymd(str(substring)):
            parsed_date_pl = parsed_date_en
        best_choose = choose_best_parsed(parsed_date_pl, parsed_date_en, search_results)
        if best_choose is None:
            continue
        if isinstance(best_choose, list):
            dates.extend([(findIndexesOfSearched(i, substring, x), x[1]) for x in best_choose])
        else:
            if is_not_valid(substring, best_choose):
                continue
            dates.append((i, best_choose))
    return [(k, str(v)) for k, v in dates]


def remove_duplicates(substring_list):
    used_spans = []
    res = []
    for s in substring_list:
        span = s[1]
        if span not in used_spans:
            used_spans.append(span)
            res.append(s)
    return res


def find_dates_substring(text):
    dates = datefinder.find_dates(text, source=True, index=True)
    return [(k, v) for k, v in dates]


def remove_only_one_digit_substrings(substring):
    pattern = re.compile('^[/\:\-\,\s\_\+\@\.]{0,}[\d{1}][/\:\-\,\s\_\+\@\.]{0,}$')
    return re.match(pattern, substring) is not None


def choose_best_parsed(parsed_pl, parsed_en, search_result):
    if parsed_pl is None and parsed_en is None and search_result is None:
        return None
    if parsed_pl is not None and parsed_en is None and search_result is None:
        return parsed_pl
    if parsed_en is not None and parsed_pl is None and search_result is None:
        return parsed_en
    if search_result is not None and parsed_pl is None and parsed_en is None:
        return search_result
    if parsed_pl is not None and parsed_en is not None and search_result is None:
        if len(str(parsed_pl)) > len(str(parsed_en)):
            return parsed_en
        else:
            return parsed_pl
    if search_result is not None:
        if len(search_result) > 1:
            return search_result
        if len(search_result) == 1:
            from_search_result = search_result[0]
            smallest = from_search_result
            if parsed_pl is not None and len(str(smallest)) > len(str(parsed_pl)):
                smallest = parsed_pl
            if parsed_en is not None and len(str(smallest)) > len(str(parsed_en)):
                smallest = parsed_en
            return smallest
    return None


def findIndexesOfSearched(originalIndex, originalSubstring, searchResult):
    i = originalSubstring.find(searchResult[0])
    return originalIndex[0] + i, originalIndex[0] + i + len(searchResult[0])


def contains_only_fullforms(string):
    from datefinder import DateFinder
    df = DateFinder
    pattern = re.compile(r"(" + df.FULL_MONTHS_POLISH + "|" + df.FULL_MONTHS_ENGLISH + ")", re.IGNORECASE)
    return bool(re.search(pattern, string))


def only_month(date):
    pattern = re.compile(r"Undefined-\d{2}-Undefined")
    return re.match(pattern, date)


def matches_ymd(string):
    from datefinder import DateFinder
    df = DateFinder
    pattern = re.compile(
        r"((\d{4})(" + df.DELIMITERS_PATTERN + ")(0?[0-9]|1[0-2])(" + df.DELIMITERS_PATTERN + ")(0?[0-9]|1[0-2]))",
        re.IGNORECASE)
    return bool(re.search(pattern, string))


def replace_days_and_months(date):
    splitted = date.split('-')
    return splitted[0] + '-' + splitted[2] + '-' + splitted[1]

def isprice_pattern(date):
    PRICE_PATTERN=r"^(-?\d{1,2}\.)(4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9]|00)$"
    return re.match(PRICE_PATTERN, date)


def is_only_numerical(substring):
    ONLY_NUMERICAL_PATTERN=r"^(t\.\s)?\d{1,2}$"
    return re.match(ONLY_NUMERICAL_PATTERN, substring)


def is_not_valid(substring, best_choose):
    if only_month(str(best_choose)) and not contains_only_fullforms(substring):
        return True
    if isprice_pattern(substring):
        return True
    if is_only_numerical(substring):
        return True
    return False




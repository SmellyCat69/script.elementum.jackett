# coding=utf-8
from elementum.provider import log

from src.utils import get_setting, UNKNOWN


#
#
# def get_setting(setting, typ):
#     return typ(
#         {
#             'sort_by': 0,
#
#             'filter_exclude_no_seed': True,
#             'filter_keywords_enabled': False,
#             'keywords_block': '',
#             'keywords_require': '',
#
#             'filter_size_enabled': False,
#             'size_include_unknown': True,
#             'size_min': 0,
#             'size_max': 100,
#             'size_movies_min': 0.5,
#             'size_movies_max': 30,
#             'size_season_min': 0.5,
#             'size_season_max': 10,
#             'size_episode_min': 0,
#             'size_episode_max': 1,
#
#             'filter_include_resolution_enabled': True,
#             'include_resolution_4k': True,
#             'include_resolution_2k': True,
#             'include_resolution_1080p': True,
#             'include_resolution_720p': True,
#             'include_resolution_480p': True,
#             'include_resolution_240p': False,
#             'include_resolution_unknown': False,
#
#             'filter_include_release': True,
#             'include_release_brrip': True,
#             'include_release_webdl': True,
#             'include_release_hdrip': True,
#             'include_release_hdtv': True,
#             'include_release_dvd': True,
#             'include_release_dvdscr': True,
#             'include_release_screener': True,
#             'include_release_3d': False,
#             'include_release_telesync': False,
#             'include_release_cam': False,
#             'include_release_tvrip': True,
#             'include_release_iptvrip': True,
#             'include_release_vhsrip': False,
#             'include_release_trailer': False,
#             'include_release_workprint': False,
#             'include_release_line': False,
#             'include_release_unknown': False,
#         }[setting]
#     )

def keywords(results):
    block_keywords = get_setting('keywords_block').split(",")
    require_keywords = get_setting('keywords_require').split(",")

    for word in block_keywords:
        results = [
            result
            for result in results
            if word in result["name"]
        ]

    for word in require_keywords:
        results = [
            result
            for result in results
            if word not in result["name"]
        ]

    return results


def _should_include_size_result(size, min, max, include_unknown):
    if size == -1:
        return include_unknown

    return min <= size <= max


def size(method, results):
    log.info("hiii", 50*"-")
    include_unknown = get_setting('size_include_' + UNKNOWN, bool)

    if method in ["movie", "season", "episode"]:
        min_size = get_setting('size_' + method + '_min', float)
        max_size = get_setting('size_' + method + '_max', float)
    else:
        min_size = get_setting('size_min', float)
        max_size = get_setting('size_max', float)

    #                        MB     KB      B
    min_size = min_size * (1024 * 1024 * 1024)
    max_size = max_size * (1024 * 1024 * 1024)
    log.info(results[0]["_size_bytes"])

    return [
        result
        for result in results
        if _should_include_size_result(result["_size_bytes"], min_size, max_size, include_unknown)
    ]


def resolution(results):
    filtered = []
    for result in results:
        log.info(f"res {result['name']}: name={result['_resolution']}; id={result['resolution']}")
        if get_setting('include_resolution_' + result["_resolution"], bool):
            filtered.append(result)

    return filtered
    # return [
    #     result
    #     for result in results
    #     if get_setting('include_resolution_' + result["_resolution"], bool)
    # ]


def seed(results):
    return [
        result
        for result in results
        if result["seeds"] > 0
    ]


def release_type(results):
    return [
        result
        for result in results
        if get_setting('include_release_' + result["release_type"], bool)
    ]

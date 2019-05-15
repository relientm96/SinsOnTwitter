"""
utility to get data from database by specifying keywords, state and polarity
"""

import couchdb
from .config import *

couch = couchdb.Server(COUCHDB_URL)
couch.resource.credentials = (COUCHDB_USER, COUCHDB_PW)


index_database = couch[DB_INDEX]
tweet_database = couch[DB_TWEET]
aurin_database = couch[DATABASE_AURIN]
wordlist_database = couch[DATABASE_WORDLIST_RESULT]


def get_tweet_rate(keywords, state, sentiment):
    """
    get the rate of tweets relevant with the keywords
    :param keywords: list of keywords
    :param state: state name
    :param sentiment: maximum sentimental value, in range of (-1, 1)
    :return: rate in percentage
    """
    tweet_id_list = get_tweets_by_words(keywords)

    view = tweet_database.view(get_view_url(state))

    total_tweet_number = view.total_rows

    count = 0
    for tweets_id in tweet_id_list:
        view_result = view[tweets_id]
        if len(view_result.rows) > 0:
            tweet_polarity = view_result.rows[0].value[3]
            if tweet_polarity < sentiment:
                count += 1

    result = float(count / total_tweet_number) * 100
    return result


def get_tweets_by_words(keywords):
    """
    get list of tweets containing one of the words
    :param keywords: list of keywords
    :return: list of tweet ids
    """
    tweet_id_list = []
    view = index_database.view(VIEW_TEXT_INDEX)
    for word in keywords:
        view_result = view[word]
        if len(view_result.rows) > 0:
            item = view_result.rows[0]
            tweet_id_list.extend(item.value)

    return tweet_id_list


def get_view_url(state):
    """
    get couchDB view of each state
    :param state: state name
    :return: view url
    """
    if state == "New South Wales":
        return VIEW_STATE_NSW

    if state == "Queensland":
        return VIEW_STATE_QUEENSLAND

    if state == "South Australia":
        return VIEW_STATE_SA

    if state == "Western Australia":
        return VIEW_STATE_WA

    if state == "Victoria":
        return VIEW_STATE_VIC

    if state == "Tasmania":
        return VIEW_STATE_TASMANIA

    return VIEW_TWEET_INFO


def get_aurin_data(key, state):
    """
    get data from aurin database
    :param key: key in database
    :param state: name of state
    :return: aurin data
    """
    doc = aurin_database.get(key)
    return doc.get(state) * 100


def get_wordlist_data(sin, state):
    """
    get result of the tweet rate containing word of the default word list
    :param sin: sin name
    :param state: state name
    :return: tweet rate
    """
    return wordlist_database[sin][state] * 100

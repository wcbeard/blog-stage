from nb2html import post_todict


def test_post_todict():
    post = """---
layout:     post
title:      Title of post
date:       Today
summary:    My summary
tags:       ipython
extra_key:  extra value
---

Stuff that shouldn't be captured
    """
    shouldbe = {
        'date': 'Today',
        'extra_key': 'extra value', 'layout': 'post',
        'summary': 'My summary', 'tags': 'ipython',
        'title': 'Title of post'
    }
    assert post_todict(post) == shouldbe

    post2 = """---
layout:     post
title:      Title of post
---more text

Stuff that shouldn't be captured
"""
    shouldbe2 = {'layout': 'post', 'title': 'Title of post'}
    assert post_todict(post2) == shouldbe2, 'Delimiting hyphens line need not be succeeded by newline'

    badpost = """---
    layout:     post
    title:      Title of post
    --more text

    Stuff that shouldn't be captured
    """

    assert post_todict(badpost) is None, 'Post should end with 3 hyphens'

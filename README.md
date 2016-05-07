# Note to self

##Dev
    jekyll serve --watch --baseurl ''
## Submodules
Ok, gh-pages broke with my submodules, so I'm doing [yet another repo that collects these](https://github.com/d10genes/notebooks), cloning it locally, and symlinking `ln -s ~/repos/notebooks/subs ~/repos/notebooks/blogistic/_notebooks`

Now do something like this in the new `notebooks` repo:

```
    # git submodule add -b jekyll https://github.com/d10genes/nyt-nlp.git _notebooks/nyt-nlp
    git submodule add https://github.com/d10genes/traffic-atl.git _notebooks/traffic-atl
    cd _notebooks/traffic-atl && git checkout .
```

##New post
Create markdown file in `_posts` directory with following format

```
---
layout:     post
title:      <Title>
date:       2016-M-D
summary:    <Blurb>
tags:       <Tags>
ipynb:      <path to ipynb file>
---
```

##Generate html posts from .md and .ipynb files in blogistic dir

    python nb2html.py -a

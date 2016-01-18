# Note to self

##Dev
    jekyll serve --watch --baseurl ''
## Submodules
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
date:       2015-M-D
summary:    <Blurb>
tags:       <Tags>
ipynb:      <path to ipynb file>
---
```

##Generate html posts from .md and .ipynb files

    python nb2html.py -a

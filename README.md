# pre-condition
- use python 3.6
- use jupyter notebook


### install packages (win)
> pip install requests
> pip install bs4
> pip install selenium
> pip install jupyter 

### install phantomjs & chromedriver (win)
- phantomjs
	- download link : http://phantomjs.org/download.html
	- decompress & add path
- chromedriver
	- download link : https://sites.google.com/a/chromium.org/chromedriver/downloads
	- decompress & move \python\Scripts

### install packages (mac)
```
$ pip install requests
$ pip install bs4
$ pip install selenium
$ brew install phantomjs
```

### crawling_basic.ipython
- https://github.com/radajin/crawling/blob/master/crawling_basic.ipynb
- requests
    - get json data using api

- beautifulsoup
    - Naver search keyword top 10
    - set header

- selenium
    - naver 1st search keyword link title
    - input key & press button
    - into iframe
    - excute script

- xpath

- screenshot
    - screeenshot base64
    - base64 image save and load

### default path 
- mac : "./"
    - setting sample) ./data/images
- win : ""
    - setting sample) data/images


# coding: utf-8

# In[1]:

from selenium import webdriver
import base64, pickle, time, os
from IPython.display import Image
from IPython.display import display
from PIL import Image as pil
from selenium.webdriver.chrome.options import Options


# ### 1. Get Youtube Images

# ##### (1) Get Youtube Driver & Save Element Screen

# In[2]:

def getDriver(youtube_url):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=chrome_options)
#    driver =  webdriver.Chrome()
    driver.get(youtube_url)
    return driver

def saveScreen(driver, filename):
    element = driver.find_element_by_css_selector('#movie_player')
    location = element.location
    size = element.size
    driver.save_screenshot('screenshot.png')
    im = pil.open('screenshot.png')
    
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    # left, top, right, bottom
    im = im.crop((left, top, right, bottom)) 
    im.save(filename) 


# ##### (2) Check Element

# In[3]:

def checkElement(driver, selector):
    result = True
    try:
        driver.find_element_by_css_selector(selector)
    except:
        result = False
    return result


# ##### (3) Skip Ad

# In[4]:

skipAd_selector = ".videoAdUiSkipButton.videoAdUiAction.videoAdUiFixedPaddingSkipButton"
closeAd_selector = ".adDisplay.extra-padding .close-button"

def skipAd(driver):
    if checkElement(driver, skipAd_selector):
        driver.find_element_by_css_selector(skipAd_selector).click()
    
def closeAd(driver):
    if checkElement(driver, closeAd_selector):
        driver.find_element_by_css_selector(closeAd_selector).click()


# ##### (4) Make Directory

# In[5]:

def makeDir(youtube_url):
    dirList = os.listdir("data/images/")
    dirName = youtube_url.split("v=")[1]
    isDir = True
    if dirName not in dirList:
        os.makedirs("data/images/" + dirName)
        isDir = False
    return isDir, dirName


# ### 2. Google Vision API

# In[14]:

# single thread
def vision(filenames):
    url = 'https://cloud.google.com/vision/'

    # open site
    driver =  webdriver.Chrome()
    driver.get(url)

    # enter iframe
    iframe = driver.find_element_by_css_selector("#vision_demo_section iframe")
    driver.switch_to_frame(iframe)
    
    result = []
    
    for filename in filenames:
    
        # file upload
        driver.find_element_by_id("input").send_keys(filename)

        # check done analytics
        delay = 0
        for _ in range(10):
            if driver.find_element_by_css_selector("#results").text != '':
                break
            time.sleep(1)
            delay += 1
        # print("Analytics Delay Time : {} sec".format(delay))
        
        if delay >= 10:
            continue
        
        # check face
        isFace = True
        try:
            driver.find_element_by_css_selector('[data-type="faceAnnotations"]')
        except:
            isFace = False

        face_data_list = []

        if isFace:
            face_list = driver.find_elements_by_css_selector('.face.style-scope.vs-faces')
            for idx, face in enumerate(face_list):
                faceData = {
                    "name":"face " + str(idx+1),
                    "confidence": face.find_element_by_css_selector('.confidence .conf-score.style-scope.vs-faces').text
                }          
                expressions = face.find_elements_by_css_selector('.type-row.style-scope.vs-faces')
                expressionData = {}
                for expression in expressions:
                    name = expression.find_element_by_css_selector('#label').text
                    state = expression.find_element_by_css_selector('#text').text
                    if "Likely" in state or "Possible" in state:
                        state = 1
                    else:
                        state = 0
                    expressionData[name] = state
                faceData["expressions"] = expressionData
                face_data_list.append(faceData)  
                
        result.append(face_data_list)    
        
        # close image
        driver.find_element_by_css_selector("#exit").click()
    driver.close()
    return result


# In[7]:

def saveImages(youtube_url, start_term, image_count, save_term, dirName):
    
    # open driver
    driver = getDriver(youtube_url)

    # skip ad
    time.sleep(6)
    skipAd(driver)

    # save images
    time.sleep(start_term)
    for idx in range(1, image_count+1):
        saveScreen(driver, 'data/images/' + dirName + '/screenshot' + str(idx) + '.png')
        time.sleep(save_term)
        print('saved : screenshot' + str(idx) + '.png')
    # close driver
    driver.close()


# In[8]:

def makeTunmnail(image_count, dirName):
# make image list
    filenames = []
    for idx in range(1, image_count + 1):
        filename = 'C:/script/data/images/' + dirName  + '/screenshot' + str(idx) + '.png'
        filenames.append(filename)

    # make thumnail
    size = (512, 512)
    thumnails = []
    for filename in filenames:
        im = pil.open(filename)
        im.thumbnail(size)
        savename = filename.split("/")
        savename[len(savename)-1] = savename[len(savename)-1].replace(".png","_thumbnail.png")
        savename = "/".join(savename)
        im.save(savename, "png")
        thumnails.append(savename)
        
    return thumnails


# In[9]:

youtube_url = "https://www.youtube.com/watch?v=xyq2T_K6DHg&start=60" # 이미지 생성 youtube URL 

# 도깨비 
# youtube_url = "https://www.youtube.com/watch?v=2kZg7byEYGA"


# In[10]:

get_ipython().run_cell_magic('time', '', 'isDir, dirName = makeDir(youtube_url)\nstart_term = 5 # 20초 후 부터 이미지 생성\nimage_count = 5 # 10개의 이미지 생성\nsave_term = 0.1 # 저장 텀\nsaveImages(youtube_url, start_term, image_count, save_term, dirName)\n\n# make thumnail\nthumnails = makeTunmnail(image_count, dirName)')


# In[11]:

get_ipython().run_cell_magic('time', '', 'result = vision(thumnails)')


# In[16]:

person_count = 0
scene_count = 0
expressions = {'Joy':0, 'Sorrow':0, 'Anger':0, 'Surprise':0, 'Exposed':0, 'Blurred':0, 'Headwear':0}
expression_list = ['Joy', 'Sorrow', 'Anger', 'Surprise', 'Exposed', 'Blurred', 'Headwear']

for data in result:
    scene_count += 1
    person_count += len(data)
    for face in data:
        for expression in expression_list:
            expressions[expression] = expressions[expression] + face['expressions'][expression]
            print(expressions)


# In[13]:

print(scene_count, person_count, expressions)


# In[ ]:




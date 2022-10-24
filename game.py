from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from skimage import transform, color, exposure, io
import skimage
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from io import BytesIO
from PIL import Image
from time import sleep
import base64
import numpy as np
import cv2

class game:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        self.driver.get('https://dino-chrome.com/en')
        self.action_chains = ActionChains(self.driver)
        self.driver.execute_script("Runner.config.ACCELERATION=0")
    '''
    def down(self):
        self.action_chains.key_down(Keys.ARROW_DOWN).perform()
    '''
    def up(self):
        self.action_chains.key_down(Keys.ARROW_UP).perform()
    '''
    def isPaused(self):
        return self.driver.execute_script("return Runner.instance_.paused")
    '''
    def isCrashed(self):
        return self.driver.execute_script("return Runner.instance_.crashed")
    '''
    def isPlaying(self):
        return self.driver.execute_script("return Runner.instance_.isRunning()") and self.driver.execute_script("return Runner.instance_.started")
    '''
    def getScore(self):
        return int(''.join(self.driver.execute_script("return Runner.instance_.distanceMeter.digits")))
    def restart(self):
        self.driver.execute_script('Runner.instance_.restart()')
        sleep(0.25)
    '''
    def stop(self):
        self.driver.execute_script('Runner.instance_.stop()')
    def play(self):
        self.driver.execute_script('Runner.instance_.play()')
    '''
    
    def getScreen(self):
        canvas_details = self.driver.execute_script("return Runner.instance_.canvas.getBoundingClientRect()")
        actual_width = self.driver.execute_script("return Runner.instance_.canvas.width")
        dino_width = self.driver.execute_script("return Runner.instance_.tRex.config.WIDTH")
        xPos = self.driver.execute_script("return Runner.instance_.tRex.xPos")
        frame = self.driver.get_screenshot_as_png()
        frame_img = skimage.io.imread(BytesIO(frame))[:,:,:3]
        frame_img = frame_img[int(canvas_details['y']):int(canvas_details['height']+canvas_details['y']),int(canvas_details['x']+(int(xPos)*(int(canvas_details['width'])/int(actual_width)))):int((canvas_details['width']/2)+canvas_details['x'])]
        frame_img = skimage.color.rgb2gray(frame_img)
        frame_img = skimage.transform.resize(frame_img,(84,100))
        frame_img = skimage.exposure.rescale_intensity(frame_img,out_range=(0,255))
        im = np.uint8(frame_img)
        im = cv2.Canny(im,threshold1=100,threshold2=200)
        im = np.array(im)
        frame_img = im / 255.
        return frame_img
    def close(self):
        self.driver.close()

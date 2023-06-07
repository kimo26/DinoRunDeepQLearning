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
import matplotlib.pyplot as plt
from time import sleep
import base64
import numpy as np
import cv2


class game:
    """
    Class to open the Chrome Dino Game and interact with it
    """
    def __init__(self):
        """
        Initializes the webdriver, navigates to the game page and sets game parameters.
        """
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.driver.set_window_size(700, 700)
        self.driver.get('https://dino-chrome.com/en')
        self.action_chains = ActionChains(self.driver)
        self.driver.execute_script("Runner.instance_.setSpeed(6)")
        self.leading_len = len("data:image/png;base64,")
    def up(self):
        """
        Makes the dinosaur jump by sending an arrow up key event.
        """
        self.action_chains.key_down(Keys.ARROW_UP).perform()

    def isCrashed(self):
        """
        Checks if the dinosaur has crashed into an obstacle.

        Returns:
            bool: True if the dinosaur has crashed, False otherwise.
        """
        return self.driver.execute_script("return Runner.instance_.crashed")

    def getScore(self):
        """
        Gets the current score of the game.

        Returns:
            int: Current score.
        """
        return int(''.join(self.driver.execute_script("return Runner.instance_.distanceMeter.digits")))

    def restart(self):
        """
        Restarts the game by executing the restart function in the game's JavaScript.
        """
        self.driver.execute_script('Runner.instance_.restart()')
        sleep(0.2)

    def getScreen(self):
        """
        Takes a screenshot of the game and processes it to be used as input for a neural network.

        Returns:
            np.array: The processed screenshot.
        """
        canvas = 'document.querySelector("#runner > div > canvas")'
        frame_img = self.driver.execute_script(f'return {canvas}.toDataURL()')
        frame_img = frame_img[self.leading_len:]
        frame_img = np.array(Image.open(BytesIO(base64.b64decode(frame_img))))[:,:,:3]
        frame_img = frame_img[:150,:300]
        frame_img = cv2.cvtColor(frame_img,cv2.COLOR_BGR2GRAY)
        frame_img = np.array(Image.fromarray(frame_img).resize((120,60)))
        frame_img = skimage.exposure.rescale_intensity(frame_img,out_range=(0,255))
        im = np.uint8(frame_img)
        im = cv2.Canny(im,threshold1=100,threshold2=200)
        im = np.array(im)
        frame_img = im / 255.
        return frame_img

    def close(self):
        """
        Closes the webdriver.
        """
        self.driver.close()

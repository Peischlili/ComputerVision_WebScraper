import os
import math
import struct
import numpy as np
from keras.layers import Conv2D
from keras.layers import Input
from keras.layers import BatchNormalization
from keras.layers import LeakyReLU
from keras.layers import ZeroPadding2D
from keras.layers import UpSampling2D
from keras.layers.merge import add, concatenate
from keras.models import Model
from numpy import loadtxt, expand_dims
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import time
import selenium
from selenium import webdriver
from PIL import Image
from time import sleep
import io
import shutil
import requests
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.utils import ChromeType
from selenium.webdriver import ChromeOptions
import torch
from torch import nn
from torch.nn import functional as F
import matplotlib.pyplot as plt
from torchvision import models, transforms, datasets
import faiss
import pandas as pd
import ssl
from flask import Flask, render_template, request, redirect, url_for
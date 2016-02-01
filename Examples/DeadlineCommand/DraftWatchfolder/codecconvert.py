import sys
import os
import datetime
import copy

import Draft
from DraftParamParser import *

expectedTypes = {}
expectedTypes['inFile'] = '<string>'
expectedTypes['outFile'] = '<string>'

params = ParseCommandLine(expectedTypes, sys.argv)
inFile = params['inFile']
outFile = params['outFile']

image = Draft.Image.CreateImage(1, 1)

decoder = Draft.VideoDecoder(inFile)

hasFrames = decoder.DecodeNextFrame(image)

if hasFrames:

    encoder = Draft.VideoEncoder(outFile, codec='H264')

    while hasFrames:

        encoder.EncodeNextFrame(image)

        hasFrames = decoder.DecodeNextFrame(image)

    encoder.FinalizeEncoding()

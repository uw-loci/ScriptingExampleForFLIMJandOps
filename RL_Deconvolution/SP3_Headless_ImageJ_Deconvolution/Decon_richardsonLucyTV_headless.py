#@ OpService ops
#@ IOService io
#@OUTPUT ImgPlus psf
#@OUTPUT ImgPlus deconvolved

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.real import FloatType
from io.scif.img import ImgSaver

# open the image
img = io.open("/test_mt_z_stack.tif")

# convert to float
imgF = ops.convert().float32(img)

# make psf same size as image
psfSize = FinalDimensions([img.dimension(0), img.dimension(1), img.dimension(2)])

# add border in z direction
borderSize=[0,0,psfSize.dimension(2)/2]

# some default values that typically yield good results
riImmersion = float(1.5)
riSample = float(1.4)

# values derived from data
numIterations = int(5)
numericalAperture = float(0.75)
zSpacing = float(800)
wavelength = float(550*1E-9)
xySpacing = float(62.9*1E-9)
zSpacing = float(160*1E-9)
reg_factor = float(0.01)
depth = 0

# generate psf
psf = ops.create().kernelDiffraction(psfSize, numericalAperture, wavelength,
				riSample, riImmersion, xySpacing, zSpacing, depth, FloatType());

# create output image for deconvolv op
deconvolved = ops.create().img(imgF)

# run deconvolve op -- richardsonLucyTV
ops.deconvolve().richardsonLucyTV(deconvolved, imgF, psf, numIterations, reg_factor);

# save the output image
ImgSaver().saveImg("/output_image.tif", deconvolved)

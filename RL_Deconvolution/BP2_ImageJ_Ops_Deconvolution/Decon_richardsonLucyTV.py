#@ OpService ops
#@ UIService ui
#@ ImgPlus img
#@ Integer numIterations(value=30)
#@ Float numericalAperture(value=0.75)
#@ Float wavelength(value=550)
#@ Float riImmersion(value=1.5)
#@ Float riSample(value=1.4)
#@ Float xySpacing(value=110)
#@ Float zSpacing(value=800)
#@OUTPUT ImgPlus psf
#@OUTPUT ImgPlus deconvolved

from net.imglib2 import FinalDimensions
from net.imglib2.type.numeric.real import FloatType

# convert to float
imgF = ops.convert().float32(img)

# make psf same size as image
psfSize = FinalDimensions([img.dimension(0), img.dimension(1), img.dimension(2)])

# add border in z direction
borderSize=[0,0,psfSize.dimension(2)/2]

wavelength=wavelength*1E-9
xySpacing=xySpacing*1E-9
zSpacing=zSpacing*1E-9

# some default values that typically yield good results
riImmersion = 1.5
riSample = 1.4

# values derived from data
xySpacing = 110E-9
zSpacing = 800E-9
depth = 0

# generate psf
psf = ops.create().kernelDiffraction(psfSize, numericalAperture, wavelength,
				riSample, riImmersion, xySpacing, zSpacing, depth, FloatType());

# create output image for deconvolv op
deconvolved = ops.create().img(imgF)
reg_factor = float(0.01)

# run deconvolve op -- richardsonLucyTV
ops.deconvolve().richardsonLucyTV(deconvolved, imgF, psf, numIterations, reg_factor);

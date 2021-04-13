#@ OpService ops
#@ UIService ui
#@ Img img

import net.imagej.ops.Op
import net.imagej.ops.Ops
import net.imagej.ops.convert.RealTypeConverter
import net.imglib2.img.Img
import net.imglib2.type.numeric.RealType
import net.imglib2.type.logic.BitType
import net.imglib2.type.numeric.integer.UnsignedLongType
import net.imglib2.util.Util

// Converts an Img's pixels to UnsignedLongType
Img convertToULong(Img original) {
	// create ULongType image
	Img largeImage = ops.create().img(original, new UnsignedLongType())

	// generate a converter from the original image type to ULongType
	RealType fromType = Util.getTypeFromInterval(original)
	RealType toType = Util.getTypeFromInterval(largeImage)
	RealTypeConverter converter = ops.op(Ops.Convert.NormalizeScale.class, toType, fromType)

	// use the converter to convert original, place output in largeImage
	ops.convert().imageType(largeImage, original, converter)
	return largeImage
}

// Obtains an invert Op (suitable for input and output Imgs)
// using the OpService
Op getSuitableInvertOp(Img output, Img input) {
	Class invert = Ops.Image.Invert.class
	return ops.op(invert, output, input)
}

// Create input images
Img bitTypeInput = ops.threshold().yen(img)
Img largeImage = convertToULong(img)

// Create output images
Img bitTypeOutput = ops.create().img(bitTypeInput, new BitType())
Img uLongTypeOutput = ops.create().img(largeImage, new UnsignedLongType())

// Obtain ops
// NB these calls are identical - only pixel types differ
Op bitTypeOp = getSuitableInvertOp(bitTypeOutput, bitTypeInput)
Op uLongOp = getSuitableInvertOp(uLongTypeOutput, largeImage)

// Describe which Op was provided for each call
println("The Op retrieved for the BitType inversion is: " + bitTypeOp.getClass())
println("The Op retrieved for the UnsignedLongType inversion is: " + uLongOp.getClass())

// Run, display bitType inversion
bitTypeOp.run()
ui.show("bitType (inverted)", bitTypeOutput)
// Run, display uLongType inversion (thresholded for visibility)
uLongOp.run()
ui.show("uLongType (inverted", ops.threshold().yen(uLongTypeOutput))

# @ImageJ ij
# @UIService ui
# @File (label = "Input FLIM Data File", style = "file") sdtFile

img = ij.scifio().datasetIO().open(sdtFile.getAbsolutePath())

import net.imglib2.img.Img
import flimlib.flimj.FitParams
fittingParameters = new FitParams()

fittingParameters.xInc = 0.039 // nanoseconds
fittingParameters.ltAxis = 2 // XY<T> stack

fittingParameters.transMap = img

rldResult = ij.op().run("flim.fitRLD", fittingParameters)

ui.show("FitResults Offset-Amplitude-Tau", rldResult.paramMap)

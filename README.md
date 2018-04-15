# Make sign stills
Estimates sign holds for sign videos and outputs overlay stills of the sign

With this script, it is possible to input videos of individual signs for any sign language (in theory), and it outputs an overlay image of the sign that is representative of the sign movements. 

The analysis is a rather crude way of estimating hold phases in the sign. It makes use of the [OpenCV](https://opencv.org) library for analyzing video frames, the [SciPy](https://www.scipy.org) library for identifying peaks in changes between frames, and the [ImageMagick](https://www.imagemagick.org) library for generating overlay stills.

As a sign video is given to the script, each frame is analyzed and compared pairwise for changes. The first peak (i.e. a lot of changes between frames) is assumed to be the initial transport movement before the sign starts. The script then looks for negative peaks (i.e. small changes ≈ hold phases) and saves these frames as representative phases of the sign. 

The example below shows the sign BEAR in Swedish Sign Language (SSL) from the [Swedish Sign Language Dictionary](http://teckensprakslexikon.su.se) with the changes between frames plotted simultaneously with [Matplotlib](https://matplotlib.org).

![Example](https://github.com/borstell/make_sign_stills/blob/master/bjorn_changes.gif)

With this analysis, two negative peaks are recognized as hold phases: the first one after the inital positive peak (first transport movement) and then the end of the sign. The resulting image still is shown below.

![Still](https://github.com/borstell/make_sign_stills/blob/master/bjorn_still.jpg)

Overall, the script performs fairly well on simplex signs (i.e. no compounds), as can be seen in the image below in which each of five randomly selected signs is illustrated with the manually selected frames found in the [Swedish Sign Language Dictionary](http://teckensprakslexikon.su.se) for the entries (left column) compared to the automatically estimated frames by this model (right column).

![Stacked](https://github.com/borstell/make_sign_stills/blob/master/stack.jpg)

The image overlays are created based on the code in another script of mine: [SSLD-images](https://github.com/borstell/SSLD-images).

Note that the script contains a couple of hard-wired steps that are based on assumptions about the analysis of signs. For instance, the script seems to work best to exclude the second half of the identified negative peaks, as these tend to constitute holds *after* the sign is completed. Also, the lines in the code that identify peaks (using SciPy) contain hardcoded estimates for peak width – these would most likely need to be changed depending on the material being used. For example, the numbers commented out in the code worked better when looking at Sign Language of the Netherlands (NGT) data from the [Global Signbank](https://signbank.science.ru.nl).

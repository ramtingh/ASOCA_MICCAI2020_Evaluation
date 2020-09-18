ASOCA Evaluation

The source code for the evaluation container for ASOCA,

## Predictions can be submitted in either of two formats:

 - NRRD format (Nearly raw raster data, used to store medical images), available on most medical imaging software and programming languages. On python using the pynrrd library is recomendded (https://pypi.org/project/pynrrd/).
 - Compressed Numpy arrays (NPZ format), using numpy.savez_compressed(filename, imagearray).

To submit predictions:

1. Create one file for each case, name each file based on the case number (e.g. 0.nrrd, 1.nrrd,...19.nrrd)
2. We expect exactly 20 predictions to be submitted, wrong number of prediction files or an entirely empty file will result in an error.
3. A value of 0 is assumed to indicate the background and 1 to indicate the vessels.
4. Create a zip archive of all 20 predicitons
5. Go to https://asoca.grand-challenge.org/ -> Create Challenge Submission and upload the archive.

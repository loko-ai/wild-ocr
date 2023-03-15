from pathlib import Path

import matplotlib.pyplot as plt

import keras_ocr

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()
print(type(pipeline))

# Get a set of three example images
p = Path("../data")

for el in p.iterdir():
    print(el)

images = [
    keras_ocr.tools.read(str(url.resolve())) for url in p.iterdir()
]

# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)

# Plot the predictions
fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    print(predictions)
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

plt.show()

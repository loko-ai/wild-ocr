from io import BytesIO

import keras_ocr
from loko_extensions.business.decorators import extract_value_args
from loko_extensions.model.components import Component, save_extensions, Input, Arg
from sanic import Sanic, json as sjson
import numpy as np

app = Sanic("targhe")


class Pipeline:
    def __init__(self):
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            self._pipeline = keras_ocr.pipeline.Pipeline()
        return self._pipeline


extractor = Pipeline()

comp = Component("WildOcr", inputs=[Input(id="image")], args=[
    Arg(name="boxes", type="boolean", value=False, description="Coordinates of the bounding boxes around the text",
        helper="Include bounding boxes")], icon="RiDoorOpenLine")

save_extensions([comp])


@app.route("/", methods=["POST"])
@extract_value_args(file=True)
def extract(file, args):
    if isinstance(file, list):
        file = file[0]
    buffer = BytesIO()
    buffer.write(file.body)
    buffer.seek(0)
    prediction_groups = extractor.pipeline.recognize([keras_ocr.tools.read(buffer)])
    ret = []
    bboxes = args.get("boxes")
    for group in prediction_groups:
        for text, bb in group:
            if bboxes:
                prediction = dict(text=text, bb=bb.tolist())
            else:
                prediction = text
            ret.append(prediction)

    return sjson(ret)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)

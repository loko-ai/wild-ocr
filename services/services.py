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
comp_description="""
### Description

The WildOCR components allows to detect and extract text "in the wild", namely from images taken in real-world, uncontrolled conditions, where the text is presented in diverse and challenging format. 


### Usage & Settings

To use this component you can link a File Reader component to the WildOcr **image** pin and make the flow start. In the WildOCR component, you can decide whether you want only the extracted text as the result or both the text and the corresponding bounding boxes. You can do this, by toggling the **boxes** field. By default, the component will output a stream list of the extracted text. If you toggle the boxes field, the output will consist of a stream of dictionaries, as illustrated in the example below:

```json
{"text":"asamerican",
"bb":[[85.19651794433594,198.86842346191406],[533.275390625,253.9600830078125],[524.9359741210938,321.7872314453125],[76.85710144042969,266.695556640625]]}
{"text":"vintage",
"bb":[[662.2559204101562,275.5168762207031],[903.0850219726562,306.5915832519531],[895.7031860351562,363.8003845214844],[654.8740844726562,332.7256774902344]]}
```

"""
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

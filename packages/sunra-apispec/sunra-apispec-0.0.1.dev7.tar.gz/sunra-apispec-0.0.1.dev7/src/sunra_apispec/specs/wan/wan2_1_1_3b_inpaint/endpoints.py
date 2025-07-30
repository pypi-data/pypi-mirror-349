import os
from base.base_api_service import BaseAPIService, SubmitResponse
from base.output_schema import VideosOutput
from model_mapping import model_mapping
from .input_schema import VideoInpaintInput


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Wan Video Inpaint API",
    description="API for Wan 2.1 1.3B Video Inpainting model",
    version="1.0.0",
    output_schema=VideosOutput,
)

@service.app.post(
    f"/{model_path}/inpaint",
    response_model=SubmitResponse,
    description="Inpaint videos using a mask and text prompt",
)
def inpaint(body: VideoInpaintInput) -> SubmitResponse:
    pass

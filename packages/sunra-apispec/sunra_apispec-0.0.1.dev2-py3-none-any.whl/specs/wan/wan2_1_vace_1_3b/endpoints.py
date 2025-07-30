import os
from base.base_api_service import BaseAPIService, SubmitResponse
from base.output_schema import VideosOutput
from model_mapping import model_mapping
from .input_schema import (
    TextToVideoInput,
    ImageToVideoInput,
    ReferenceImagesToVideoInput,
    VideoToVideoInput,
    InpaintingInput,
)


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Wan VACE API",
    description="API for Wan 2.1 VACE 1.3B model for video creation and editing",
    version="1.0.0",
    output_schema=VideosOutput,
)

@service.app.post(
    f"/{model_path}/text-to-video",
    response_model=SubmitResponse,
    description="Generate videos from text prompts",
)
def text_to_video(body: TextToVideoInput) -> SubmitResponse:
    pass

@service.app.post(
    f"/{model_path}/image-to-video",
    response_model=SubmitResponse,
    description="Generate videos from reference images",
)
def image_to_video(body: ImageToVideoInput) -> SubmitResponse:
    pass

@service.app.post(
    f"/{model_path}/reference-images-to-video",
    response_model=SubmitResponse,
    description="Generate videos from reference images",
)
def reference_images_to_video(body: ReferenceImagesToVideoInput) -> SubmitResponse:
    pass

@service.app.post(
    f"/{model_path}/video-to-video",
    response_model=SubmitResponse,
    description="Edit videos based on text prompts",
)
def video_to_video(body: VideoToVideoInput) -> SubmitResponse:
    pass

@service.app.post(
    f"/{model_path}/inpaint",
    response_model=SubmitResponse,
    description="Inpaint videos using mask and text prompts",
)
def inpaint(body: InpaintingInput) -> SubmitResponse:
    pass 

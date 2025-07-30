import os
from sunra_apispec.base.base_api_service import BaseAPIService, SubmitResponse
from sunra_apispec.base.output_schema import VideoOutput
from sunra_apispec.model_mapping import model_mapping
from .sunra_schema import Text2VideoInput, Image2VideoInput, EffectInput


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Pixverse v4 API",
    description="API for Pixverse v4 video generation model - Quickly generate smooth 5s or 8s videos at 540p, 720p or 1080p.",
    version="1.0.0",
    output_schema=VideoOutput,
)

@service.app.post(
    f"/{model_path}/text-to-video",
    response_model=SubmitResponse,
    description="Generate video from text prompts",
)
def text_to_video(body: Text2VideoInput) -> SubmitResponse:
    pass

@service.app.post(
    f"/{model_path}/image-to-video",
    response_model=SubmitResponse,
    description="Generate video from image",
)
def image_to_video(body: Image2VideoInput) -> SubmitResponse:
    pass

@service.app.post(
    f"/{model_path}/effects",
    response_model=SubmitResponse,
    description="Apply special effects to generate a video",
)
def effects(body: EffectInput) -> SubmitResponse:
    pass

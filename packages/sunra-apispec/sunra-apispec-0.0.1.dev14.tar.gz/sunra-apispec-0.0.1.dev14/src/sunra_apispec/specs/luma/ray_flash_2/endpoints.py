import os
from ....base.base_api_service import BaseAPIService, SubmitResponse
from ....base.output_schema import VideoOutput
from ....model_mapping import model_mapping
from .sunra_schema import Text2VideoInput, Image2VideoInput


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Luma Ray Flash 2 API",
    description="API for Luma Ray Flash 2 video generation model - A faster, more efficient version of Ray 2 that generates high-quality videos from text prompts. Available in 540p and 720p resolutions.",
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
    description="Generate video from start image, with optional end image",
)
def image_to_video(body: Image2VideoInput) -> SubmitResponse:
    pass

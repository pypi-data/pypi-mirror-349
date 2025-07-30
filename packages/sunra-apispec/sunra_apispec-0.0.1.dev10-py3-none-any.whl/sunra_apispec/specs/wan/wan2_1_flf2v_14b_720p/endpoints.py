import os
from base.base_api_service import BaseAPIService, SubmitResponse
from base.output_schema import VideosOutput
from model_mapping import model_mapping
from .sunra_schema import ImageToVideoInput
from .service_providers.fal.adapter import ImageToVideoAdapter as FalImageToVideoAdapter

model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Wan FLF2V API",
    description="API for Wan 2.1 First-Last-Frame to Video 14B 720p model",
    version="1.0.0",
    output_schema=VideosOutput,
)

@service.app.post(
    f"/{model_path}/image-to-video",
    response_model=SubmitResponse,
    description="Generate videos from first and last frame images with a text prompt",
)
def image_to_video(body: ImageToVideoInput) -> SubmitResponse:
    pass


registry_items = {
    f"{model_path}/image-to-video": [
        {
            "service_provider": "fal",
            "adapter": FalImageToVideoAdapter,
        }
    ]
}

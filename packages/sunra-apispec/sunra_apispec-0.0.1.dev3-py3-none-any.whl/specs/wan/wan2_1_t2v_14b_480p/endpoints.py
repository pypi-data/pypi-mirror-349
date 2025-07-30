import os
from base.base_api_service import BaseAPIService, SubmitResponse
from base.output_schema import VideosOutput
from model_mapping import model_mapping
from .input_schema import Text2VideoInput


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Wan Video API",
    description="API for Wan 2.1 14B 480p Text-to-Video generation model",
    version="1.0.0",
    output_schema=VideosOutput,
)

@service.app.post(
    f"/{model_path}/text-to-video",
    response_model=SubmitResponse,
    description="Generate videos from text prompts",
)
def text_to_video(body: Text2VideoInput) -> SubmitResponse:
    pass 
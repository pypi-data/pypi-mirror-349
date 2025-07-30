from ...input_schema import (
    TextToVideoInput,
    ImageToVideoInput,
    ReferenceImagesToVideoInput,
    VideoToVideoInput,
    VideoInpaintingInput,
)
from .schema import ReplicateInput

def get_speed_mode(motion):
    return {
        "consistent": "Lightly Juiced \ud83c\udf4a (more consistent)",
        "fast": "Juiced \ud83d\udd25 (default)",
        "extra_fast": "Extra Juiced \ud83d\udd25 (more speed)"
    }[motion]


def get_size(resolution, aspect_ratio):
    if resolution == "480p":
        if aspect_ratio == "16:9":
            return "832*480"
        elif aspect_ratio == "9:16":
            return "480*832"
        else:
            return "832*480"
    elif resolution == "720p":
        if aspect_ratio == "16:9":
            return "1280*720"
        elif aspect_ratio == "9:16":
            return "720*1280"
        else:
            return "1280*720"
    else:
        return "1280*720"

class Wan2_1_Vace_14bReplicateMapper:    
    
    @staticmethod
    def validate_and_convert_text_to_video_input(data: dict) -> dict:
        # Validate the input data
        input_model = TextToVideoInput.model_validate(data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True) 
    
    @staticmethod
    def validate_and_convert_image_to_video_input(data: dict) -> dict:
        # Validate the input data
        input_model = ImageToVideoInput.model_validate(data)

        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_ref_images=[input_model.start_image],
        )

        return replicate_input.model_dump(exclude_none=True)
    
    @staticmethod
    def validate_and_convert_reference_images_to_video_input(data: dict) -> dict:
        # Validate the input data
        input_model = ReferenceImagesToVideoInput.model_validate(data)
        
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_ref_images=input_model.reference_images,
        )
        
        return replicate_input.model_dump(exclude_none=True)


    @staticmethod
    def validate_and_convert_video_to_video_input(data: dict) -> dict:
        # Validate the input data
        input_model = VideoToVideoInput.model_validate(data)
        
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_video=input_model.video,
        )
        
        return replicate_input.model_dump(exclude_none=True)
    
    @staticmethod
    def validate_and_convert_video_inpainting_input(data: dict) -> dict:
        # Validate the input data
        input_model = VideoInpaintingInput.model_validate(data) 
        
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_video=input_model.video,
            src_mask=input_model.mask,
        )
        
        return replicate_input.model_dump(exclude_none=True)

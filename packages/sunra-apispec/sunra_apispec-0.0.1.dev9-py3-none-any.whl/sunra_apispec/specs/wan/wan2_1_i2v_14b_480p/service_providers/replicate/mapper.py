from ...input_schema import Image2VideoInput
from .schema import ReplicateInput


class Wan2_1_I2V_14b_480PReplicateMapper:
    """Mapper class to convert from Image2VideoInput to Replicate API input format."""
    
    @staticmethod
    def validate_and_convert_image_to_video_input(data: dict) -> dict:
        # Validate the input data
        input_model = Image2VideoInput.model_validate(data)

        # Map fast_mode from "On"/"Off" to Replicate's options
        fast_mode_mapping = {
            "Off": "Balanced",
            "On": "Fast"  # Map "On" to "Fast" as default acceleration level
        }
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            image=input_model.start_image,
            prompt=input_model.prompt,
            max_area=input_model.max_area,
            seed=input_model.seed,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            num_frames=input_model.number_of_frames,
            frames_per_second=input_model.frames_per_second,
            fast_mode=fast_mode_mapping.get(input_model.fast_mode, "Balanced")
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True) 
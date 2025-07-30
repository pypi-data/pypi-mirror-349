from ...input_schema import VideoInpaintInput
from .schema import ReplicateInput


class Wan2_1_1_3B_InpaintReplicateMapper:    
    @staticmethod
    def validate_and_convert_video_inpaint_input(data: dict) -> dict:
        # Validate the input data
        input_model = VideoInpaintInput.model_validate(data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            input_video=input_model.video,
            prompt=input_model.prompt,
            mask_video=input_model.mask,
            seed=input_model.seed,
            strength=input_model.strength,
            expand_mask=input_model.expand_mask,
            guide_scale=input_model.guidance_scale,
            sampling_steps=input_model.number_of_steps,
            frames_per_second=input_model.frames_per_second,
            keep_aspect_ratio=input_model.keep_aspect_ratio,
            inpaint_fixup_steps=input_model.inpaint_fixup_steps,
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True) 

import torch

class LTX_DynamicResolutionSelector:
    
    RESOLUTIONS_720P = {
        "9:16": (704, 1216),
        "16:9": (1216, 704),
        "1:1":  (960, 960),
        "3:4":  (912, 1216),
        "4:3":  (1216, 912)
    }
    
    RESOLUTIONS_512P = {
        "9:16": (384, 672),
        "16:9": (672, 384),
        "1:1":  (512, 512),
        "3:4":  (448, 576),
        "4:3":  (576, 416)
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "resolution_preset": (["720p", "512p"], {"default": "720p"}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_resolution"
    CATEGORY = "LTX Custom Logic"

    def get_resolution(self, image, resolution_preset):
        _ , height, width, _ = image.shape
        
        if resolution_preset == "720p":
            resolution_map = self.RESOLUTIONS_720P
        else: # "512p"
            resolution_map = self.RESOLUTIONS_512P

        if height == 0:
            input_ratio = 1.777
        else:
            input_ratio = width / height
            
        best_match_key = None
        min_diff = float('inf')

        for key, (res_w, res_h) in resolution_map.items():
            supported_ratio = res_w / res_h
            diff = abs(input_ratio - supported_ratio)
            
            if diff < min_diff:
                min_diff = diff
                best_match_key = key
        
        final_width, final_height = resolution_map[best_match_key]
        
        print(f"[DynamicResolution] Preset: {resolution_preset} | Input: {width}x{height} -> Best Match: {best_match_key} -> Output: {final_width}x{final_height}")
        
        return (final_width, final_height)
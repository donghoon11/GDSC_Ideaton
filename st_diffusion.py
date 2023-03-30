import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from PIL import Image

# def image_grid(imgs, rows, cols):
#     assert len(imgs) == rows*cols

#     w, h = imgs[0].size
#     grid = Image.new('RGB', size=(cols*w, rows*h))
#     grid_w, grid_h = grid.size
    
#     for i, img in enumerate(imgs):
#         grid.paste(img, box=(i%cols*w, i//cols*h))
#     return grid

def generate_v1(input_prompt: str, height=512, width=512):
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
    pipe = pipe.to('cuda')

    prompt = input_prompt
    image = pipe(prompt, num_inference_steps=15, height=height, width=width).images[0]
    return image

def generate_v2(input_prompt: str, styler='realistic', height=768, width=768):

    model_id = "stabilityai/stable-diffusion-2"

    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, revision="fp16", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    # styler 예시 : 'realistic', 'story', 'anime', 'concept art'
    prompt = f"{input_prompt}, {styler}" 
    image = pipe(prompt, height=height, width=width).images[0]
    return image

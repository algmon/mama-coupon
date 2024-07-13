import gradio as gr
import torch
from diffusers import StableDiffusion3Pipeline

# Load the model
pipe = StableDiffusion3Pipeline.from_pretrained(
    "stable-diffusion-3-medium-diffusers",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda:1")

def generate_image(prompt, negative_prompt, num_inference_steps, guidance_scale):
    # Generate the image
    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale
    ).images[0]
    return image

# Create the Gradio interface
interface = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(label="正向提示词"),
        gr.Textbox(label="负向提示词", placeholder="Optional"),
        gr.Slider(step=1, minimum=1, maximum=100, value=28, label="推理步数"),
        gr.Slider(minimum=1.0, maximum=20.0, step=0.1, value=7.0, label="Guidance Scale")
    ],
    outputs="image",
    title="Stable Diffusion 3 Image Generator",
    description="Generate images with Stable Diffusion 3. Type a prompt and see the magic!"
)

# Launch the interface
interface.launch(server_name="0.0.0.0", server_port=8912, inbrowser=True, share=False)
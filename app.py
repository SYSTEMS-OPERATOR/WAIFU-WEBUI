"""Gradio web UI for Low Res Waifu Models.

This script launches a simple Gradio interface that accepts an image and
returns the same image as a placeholder for a real upscaling model.
"""

from __future__ import annotations

from PIL import Image
import gradio as gr


def upscale_image(image: Image.Image) -> Image.Image:
    """Return the uploaded image unchanged.

    This function acts as a placeholder for the actual model inference
    that will upscale the provided low resolution waifu image.
    """
    # TODO: Replace this stub with real upscaling logic.
    return image


with gr.Blocks() as demo:
    # Create a simple interface with one image input and output.
    gr.Markdown("## Low Res Waifu Image Upscaler")
    input_image = gr.Image(label="Input Image")
    output_image = gr.Image(label="Upscaled Image")
    upscale_button = gr.Button("Upscale")

    # Connect the button click event to the upscale function.
    upscale_button.click(fn=upscale_image, inputs=input_image, outputs=output_image)


if __name__ == "__main__":
    # Launch the Gradio demo interface when executed as a script.
    demo.launch()

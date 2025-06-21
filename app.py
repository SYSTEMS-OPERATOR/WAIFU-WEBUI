"""Gradio web UI for Low Res Waifu Models. 💖

This script launches a simple Gradio interface that accepts an image and
returns the same image as a placeholder for a real upscaling model.

Example:
    Run ``python app.py`` to start the demo. 🚀
"""

from __future__ import annotations

from PIL import Image
import gradio as gr


def upscale_image(image: Image.Image) -> Image.Image:
    """Upscale the provided image by a factor of two.

    This function performs a basic resize operation as a stand in for a real
    machine learning model that would enhance the low resolution waifu image.
    """
    if image is None:
        return None

    width, height = image.size
    upscale_size = (width * 2, height * 2)
    return image.resize(upscale_size, Image.LANCZOS)


with gr.Blocks() as demo:
    # Create a simple navigational menu using tabs.
    with gr.Tabs() as tabs:
        with gr.TabItem("Home"):
            gr.Markdown(
                "# WAIFU-WEBUI 💖\nChoose an option from the navigation tabs above."
            )

        with gr.TabItem("Upscale"):
            gr.Markdown("## Low Res Waifu Image Upscaler ✨")
            input_image = gr.Image(label="Input Image")
            output_image = gr.Image(label="Upscaled Image")
            upscale_button = gr.Button("Upscale 🖼️")

            # Connect the button click event to the upscale function.
            upscale_button.click(
                fn=upscale_image, inputs=input_image, outputs=output_image
            )

        with gr.TabItem("About"):
            gr.Markdown(
                "This demo uses a placeholder upscaling function. "
                "It simply doubles the image size to illustrate the UI. 🎨"
            )


if __name__ == "__main__":
    # Launch the Gradio demo interface when executed as a script.
    demo.launch()

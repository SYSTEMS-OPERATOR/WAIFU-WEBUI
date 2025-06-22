"""Gradio web UI for creating a simple waifu companion. 💖

The interface provides several tabs that allow you to tweak a persona,
chat with it, build a text dataset from manga pages and upscale images.

Example:
    Run ``python app.py`` to start the demo. 🚀
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Tuple

from PIL import Image
import gradio as gr
import pytesseract

# ------------------------------
# Data storage
# ------------------------------


@dataclass
class Persona:
    """Simple data structure holding persona attributes."""

    name: str = "Waifu"
    age: str = "unknown"
    personality: str = "cheerful"
    catchphrase: str = "Hello!"


# Instantiate the editable persona
persona = Persona()

# Collected dataset lines from text or manga pages
dataset: List[str] = []


def save_dataset() -> str:
    """Save the collected dataset to ``dataset.txt``."""

    with open("dataset.txt", "w", encoding="utf-8") as file:
        for line in dataset:
            file.write(f"{line}\n")
    return "dataset.txt saved"


def load_dataset(file_path: str) -> str:
    """Load lines from a text file into the dataset."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
            dataset.extend(lines)
    except OSError:
        return "Failed to load file"
    return "\n".join(dataset)


def update_persona(
    name: str,
    age: str,
    personality: str,
    catchphrase: str,
) -> str:
    """Update the global persona with the provided values."""

    if name:
        persona.name = name
    if age:
        persona.age = age
    if personality:
        persona.personality = personality
    if catchphrase:
        persona.catchphrase = catchphrase
    return "Persona updated"


def add_text_to_dataset(text: str) -> str:
    """Append provided text to the dataset and return all lines."""

    if text:
        dataset.append(text)
    return "\n".join(dataset)


def add_image_to_dataset(image: Image.Image) -> str:
    """Extract text from an image using OCR and add it to the dataset."""

    if image is not None:
        ocr_text = pytesseract.image_to_string(image)
        lines = [
            line.strip()
            for line in ocr_text.splitlines()
            if line.strip()
        ]
        dataset.extend(lines)
    return "\n".join(dataset)


def generate_reply(_history: List[Tuple[str, str]], message: str) -> str:
    """Generate a simple reply using the dataset or the persona catchphrase."""

    if dataset:
        return random.choice(dataset)
    return persona.catchphrase


def chat(
    history: List[Tuple[str, str]],
    message: str,
) -> List[Tuple[str, str]]:
    """Append the user's message and generated reply to the history."""

    reply = generate_reply(history, message)
    history = history + [(message, reply)]
    return history


def upscale_image(image: Image.Image) -> Image.Image:
    """Upscale the provided image by a factor of two.

    This function performs a basic resize operation as a stand in for a real
    machine learning model that would enhance a low resolution waifu image.
    """
    if image is None:
        return None

    width, height = image.size
    upscale_size = (width * 2, height * 2)
    return image.resize(upscale_size, Image.LANCZOS)


with gr.Blocks() as demo:
    """Build the multi-tabbed web interface."""
    with gr.Tabs() as tabs:
        # ------------------------------
        # Home tab
        # ------------------------------
        with gr.TabItem("Home"):
            gr.Markdown(
                "# WAIFU-WEBUI 💖\n"
                "Choose an option from the navigation tabs above."
            )

        # ------------------------------
        # Persona editing tab
        # ------------------------------
        with gr.TabItem("Persona"):
            gr.Markdown("## Edit Persona Attributes")
            with gr.Row():
                name = gr.Textbox(label="Name", value=persona.name)
                age = gr.Textbox(label="Age", value=persona.age)
            personality = gr.Textbox(
                label="Personality", value=persona.personality
            )
            catchphrase = gr.Textbox(
                label="Catchphrase", value=persona.catchphrase
            )
            update_btn = gr.Button("Update Persona")
            persona_status = gr.Textbox(label="Status", interactive=False)

            update_btn.click(
                update_persona,
                inputs=[name, age, personality, catchphrase],
                outputs=persona_status,
            )

        # ------------------------------
        # Chat tab
        # ------------------------------
        with gr.TabItem("Chat"):
            gr.Markdown("## Talk with your waifu")
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Your message")
            send_btn = gr.Button("Send")

            send_btn.click(chat, inputs=[chatbot, msg], outputs=chatbot)
            msg.submit(chat, inputs=[chatbot, msg], outputs=chatbot)

        # ------------------------------
        # Dataset management tab
        # ------------------------------
        with gr.TabItem("Dataset"):
            gr.Markdown("## Build Dataset from Manga Pages")
            dataset_box = gr.Textbox(
                label="Current Dataset", value="", lines=10, interactive=False
            )
            text_input = gr.Textbox(label="Add Text")
            add_text_btn = gr.Button("Add Text")
            manga_image = gr.Image(label="Add Manga Page")
            add_image_btn = gr.Button("Add Image")
            load_file = gr.File(label="Load Dataset", type="filepath")
            load_btn = gr.Button("Load")
            save_btn = gr.Button("Save")

            add_text_btn.click(
                add_text_to_dataset,
                inputs=text_input,
                outputs=dataset_box,
            )
            add_image_btn.click(
                add_image_to_dataset,
                inputs=manga_image,
                outputs=dataset_box,
            )
            load_btn.click(
                load_dataset,
                inputs=load_file,
                outputs=dataset_box,
            )
            save_btn.click(save_dataset, outputs=dataset_box)

        # ------------------------------
        # Upscale tab
        # ------------------------------
        with gr.TabItem("Upscale"):
            gr.Markdown("## Low Res Waifu Image Upscaler ✨")
            input_image = gr.Image(label="Input Image")
            output_image = gr.Image(label="Upscaled Image")
            upscale_button = gr.Button("Upscale 🖼️")

            upscale_button.click(
                fn=upscale_image, inputs=input_image, outputs=output_image
            )

        # ------------------------------
        # About tab
        # ------------------------------
        with gr.TabItem("About"):
            gr.Markdown(
                "This demo uses a placeholder upscaling function. "
                "It simply doubles the image size to illustrate the UI. 🎨"
            )


if __name__ == "__main__":
    # Launch the Gradio demo interface when executed as a script.
    demo.launch()

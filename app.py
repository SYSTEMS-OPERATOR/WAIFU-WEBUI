"""Gradio web UI for creating a simple waifu companion. 💖

The interface provides several tabs that allow you to tweak a persona,
chat with it, build a text dataset from manga pages and upscale images.

Example:
    Run ``python app.py`` to start the demo. 🚀

This application demonstrates a minimal workflow for building a persona from
manga panels. Users can configure character attributes, extract dialogue text
via OCR and chat with the resulting companion. The upscaling tab from the
original project is retained as a simple example.

"""

from __future__ import annotations

from dataclasses import dataclass
import random
import os
from typing import List, Tuple, Optional

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

# Load existing dataset if present
if os.path.exists("dataset.txt"):
    with open("dataset.txt", "r", encoding="utf-8") as file:
        dataset.extend([line.strip() for line in file if line.strip()])


def save_dataset() -> str:
    """Save the collected dataset to ``dataset.txt``."""

    with open("dataset.txt", "w", encoding="utf-8") as file:
        for line in dataset:
            file.write(f"{line}\n")
    # Return the current dataset so the UI textbox is not replaced by a
    # status message. Previously this function returned the string
    # "dataset.txt saved", which caused the dataset view to be overwritten
    # with that message when pressing the "Save" button.
    return "\n".join(dataset)


def load_dataset(file_path: Optional[str]) -> str:
    """Load lines from a text file into the dataset."""

    if not file_path or not os.path.isfile(file_path):
        return "Failed to load file"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
            dataset.extend(lines)
    except (OSError, TypeError):
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


def reset_persona() -> str:
    """Reset persona attributes to their default values."""

    global persona
    persona = Persona()
    return "Persona reset"


def add_text_to_dataset(text: str) -> str:
    """Append provided text to the dataset and return all lines."""

    if text:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if lines:
            dataset.extend(lines)
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


def clear_dataset() -> str:
    """Remove all dataset entries and delete ``dataset.txt`` if it exists."""

    dataset.clear()
    try:
        os.remove("dataset.txt")
    except OSError:
        pass
    return ""


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






def upscale_image(image: Image.Image) -> Optional[Image.Image]:
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
            reset_btn = gr.Button("Reset Persona")
            persona_status = gr.Textbox(label="Status", interactive=False)

            update_btn.click(
                update_persona,
                inputs=[name, age, personality, catchphrase],
                outputs=persona_status,
            )
            reset_btn.click(
                reset_persona,
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
                label="Current Dataset",
                value="\n".join(dataset),
                lines=10,
                interactive=False,
            )
            text_input = gr.Textbox(label="Add Text")
            add_text_btn = gr.Button("Add Text")
            # Use PIL format so pytesseract can process the image correctly
            manga_image = gr.Image(label="Add Manga Page", type="pil")
            add_image_btn = gr.Button("Add Image")
            load_file = gr.File(label="Load Dataset", type="filepath")
            load_btn = gr.Button("Load")
            save_btn = gr.Button("Save")
            clear_btn = gr.Button("Clear")

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
            clear_btn.click(clear_dataset, outputs=dataset_box)

        # ------------------------------
        # Upscale tab
        # ------------------------------

        with gr.TabItem("Upscale"):
            gr.Markdown("## Low Res Waifu Image Upscaler ✨")
            input_image = gr.Image(label="Input Image", type="pil")
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
                "This demo allows basic creation of a companion persona "
                "from manga pages. OCR and chat responses are simplistic "
                "placeholders for research purposes."
            )


if __name__ == "__main__":
    demo.launch()


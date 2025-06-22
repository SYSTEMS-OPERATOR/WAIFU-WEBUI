"""Gradio interface for creating a waifu companion AI. 💖

This application demonstrates a minimal workflow for building a persona from
manga panels. Users can configure character attributes, extract dialogue text
via OCR and chat with the resulting companion. The upscaling tab from the
original project is retained as a simple example.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import gradio as gr
from PIL import Image
import pytesseract


@dataclass
class WaifuCharacter:
    """Data container describing the waifu persona."""

    name: str = "My Waifu"
    description: str = ""
    avatar: Optional[Image.Image] = None
    dataset: List[str] = field(default_factory=list)

    def add_dialogue(self, text: str) -> None:
        """Split text into lines and extend the dataset."""

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        self.dataset.extend(lines)


# Global character instance used across interface callbacks
WAIFU = WaifuCharacter()


def upscale_image(image: Image.Image) -> Optional[Image.Image]:
    """Upscale the provided image by a factor of two."""

    if image is None:
        return None

    width, height = image.size
    upscale_size = (width * 2, height * 2)
    return image.resize(upscale_size, Image.LANCZOS)


def extract_text(image: Image.Image) -> str:
    """Perform OCR on the provided image using Tesseract."""

    if image is None:
        return ""
    return pytesseract.image_to_string(image)


def update_character(name: str, description: str, avatar: Image.Image) -> str:
    """Update the global character attributes."""

    if name:
        WAIFU.name = name
    WAIFU.description = description
    WAIFU.avatar = avatar
    return f"Character '{WAIFU.name}' updated."


def process_manga_page(image: Image.Image) -> Tuple[str, str]:
    """Extract text from a manga page and store it in the dataset."""

    text = extract_text(image)
    WAIFU.add_dialogue(text)
    size_info = f"Dataset contains {len(WAIFU.dataset)} lines."
    return text, size_info


def generate_reply(user_message: str) -> str:
    """Return a simple response based on collected dialogue lines."""

    if not WAIFU.dataset:
        return "Dataset empty. Please add manga pages first."
    return random.choice(WAIFU.dataset)


def chat(user_message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
    """Append user/AI messages to the chat history."""

    reply = generate_reply(user_message)
    history = history + [(user_message, reply)]
    return history, ""


with gr.Blocks(title="WAIFU-WEBUI") as demo:
    with gr.Tabs() as tabs:
        # Setup tab
        with gr.TabItem("Setup"):
            char_name = gr.Textbox(label="Name", value=WAIFU.name)
            char_desc = gr.Textbox(label="Description")
            char_avatar = gr.Image(label="Avatar", type="pil")
            status = gr.Textbox(label="Status", interactive=False)
            save_btn = gr.Button("Save")

            save_btn.click(
                update_character,
                inputs=[char_name, char_desc, char_avatar],
                outputs=status,
            )

        # Manga OCR tab
        with gr.TabItem("Manga OCR"):
            ocr_input = gr.Image(label="Manga Page", type="pil")
            ocr_text = gr.Textbox(label="Extracted Text")
            dataset_info = gr.Textbox(label="Dataset Info", interactive=False)
            ocr_btn = gr.Button("Add to Dataset")

            ocr_btn.click(
                process_manga_page,
                inputs=ocr_input,
                outputs=[ocr_text, dataset_info],
            )

        # Chat tab
        with gr.TabItem("Chat"):
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(label="Your Message")
            send_btn = gr.Button("Send")

            send_btn.click(
                chat,
                inputs=[user_input, chatbot],
                outputs=[chatbot, user_input],
            )

        # Upscale tab retained from original demo
        with gr.TabItem("Upscale"):
            gr.Markdown("## Low Res Waifu Image Upscaler ✨")
            input_image = gr.Image(label="Input Image", type="pil")
            output_image = gr.Image(label="Upscaled Image")
            upscale_button = gr.Button("Upscale 🖼️")

            upscale_button.click(
                fn=upscale_image, inputs=input_image, outputs=output_image
            )

        # About tab
        with gr.TabItem("About"):
            gr.Markdown(
                "This demo allows basic creation of a companion persona "
                "from manga pages. OCR and chat responses are simplistic "
                "placeholders for research purposes."
            )


if __name__ == "__main__":
    demo.launch()


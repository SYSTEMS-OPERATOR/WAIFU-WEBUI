# WAIFU-WEBUI 🌸✨

A Gradio web UI for managing a waifu companion AI. 🖼️

The interface provides tools to build a custom persona from manga panels,
edit character attributes and chat with the generated companion. Manga
images can be uploaded for text extraction via OCR, which populates a dataset
used for simple dialogue generation.


## Installation 🔧

1. Clone this repository.
2. Install the dependencies with `pip install -r requirements.txt` 🍰

## Manual Install 🛠️

Install the dependencies with:

```bash
pip install pillow gradio pytesseract  # 🔧
```

## Usage 🚀

Run `python app.py` 💻 to start the interface. The application launches a local
Gradio server presenting several tabs:

* **Setup** – configure character attributes and upload an avatar.
* **Manga OCR** – import manga pages and extract dialogue using OCR.
* **Chat** – interact with your waifu using the collected lines.
* **Upscale** – demo image upscaling.
* **About** – project information.

The included OCR and chat logic are simple examples that demonstrate the
workflow for building a personalized companion dataset.

## License 📜

This project is released under the terms of the [Unlicense](LICENSE).

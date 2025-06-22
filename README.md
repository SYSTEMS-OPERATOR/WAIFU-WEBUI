# WAIFU-WEBUI 🌸✨

A Gradio web UI for creating a simple waifu companion.

## Installation 🔧

1. Clone this repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Install Tesseract OCR so manga pages can be processed:

```bash
apt-get update && apt-get install -y tesseract-ocr
```

## Usage 🚀

Run `python app.py` to launch the interface at `http://localhost:7860`.
The UI exposes several tabs:

- **Persona** – edit the waifu's attributes.
- **Chat** – talk with the persona. Replies come from the dataset or the catchphrase.
- **Dataset** – collect text from manga pages or manual input and save it.
- **Upscale** – simple image upscaling (placeholder functionality).
- **About** – details about this demo.

## License 📜

This project is released under the terms of the [Unlicense](LICENSE).

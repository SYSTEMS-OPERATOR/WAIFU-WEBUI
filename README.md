# WAIFU-WEBUI 🌸✨

A Gradio web UI for creating a simple waifu companion. 🖼️

The interface provides tools to build a custom persona from manga panels,
edit character attributes and chat with the generated companion. Manga
images can be uploaded for text extraction via OCR, which populates a dataset
used for simple dialogue generation.


## Installation 🔧

1. Clone this repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Install Tesseract OCR so manga pages can be processed:

```bash
pip install pillow gradio pytesseract  # 🔧
```

## Usage 🚀

Run `python app.py` to launch the interface at `http://localhost:7860`.
The UI exposes several tabs:

- **Persona** – edit the waifu's attributes.
- **Chat** – talk with the persona. Replies come from the dataset or the catchphrase.
- **Dataset** – collect text from manga pages or manual input and save it.
- **Upscale** – simple image upscaling (placeholder functionality).
- **About** – details about this demo.

## Game Flow 🕹️

The diagram below summarizes how the main parts of the application
interact. Each object corresponds to a section of the code in
`app.py` that provides a specific function.

```mermaid
graph TD
    user([User]) --> ui["Gradio Interface"]

    subgraph Persona
        updatePersona["update_persona()"]
        resetPersona["reset_persona()"]
    end

    subgraph Dataset
        addText["add_text_to_dataset()"]
        addImage["add_image_to_dataset()"]
        saveData["save_dataset()"]
        loadData["load_dataset()"]
        clearData["clear_dataset()"]
    end

    subgraph Chat
        chatFn["chat()"]
        genReply["generate_reply()"]
    end

    subgraph Upscale
        upscaleImage["upscale_image()"]
    end

    ui --> Persona
    ui --> Dataset
    ui --> Chat
    ui --> Upscale

    Chat --> genReply
    genReply --> Persona
    genReply --> Dataset
    Dataset --> addImage
    addImage --> ocr["pytesseract OCR"]
```

## Testing 🧪

Run the unit tests with [pytest](https://pytest.org/):

```bash
PYTHONPATH=. pytest -v
```


## License 📜

This project is released under the terms of the [Unlicense](LICENSE).

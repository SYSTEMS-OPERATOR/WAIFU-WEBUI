import os
from unittest import mock
from PIL import Image
import pytest

import app


def setup_function(function):
    # ensure dataset is empty before each test
    app.dataset.clear()
    app.persona = app.Persona()
    # remove dataset.txt if exists
    if os.path.exists("dataset.txt"):
        os.remove("dataset.txt")


def test_update_and_reset_persona():
    msg = app.update_persona("Rei", "17", "quiet", "Hi")
    assert msg == "Persona updated"
    assert app.persona.name == "Rei"
    assert app.persona.age == "17"
    assert app.persona.personality == "quiet"
    assert app.persona.catchphrase == "Hi"

    msg = app.reset_persona()
    assert msg == "Persona reset"
    assert app.persona.name == "Waifu"
    assert app.persona.catchphrase == "Hello!"


def test_dataset_text_and_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    app.dataset.clear()
    app.add_text_to_dataset("hello")
    result = app.save_dataset()
    assert "hello" in result
    assert os.path.exists("dataset.txt")
    loaded = app.load_dataset("dataset.txt")
    assert "hello" in loaded
    cleared = app.clear_dataset()
    assert cleared == ""
    assert not os.path.exists("dataset.txt")
    assert app.dataset == []


def test_add_image_to_dataset(monkeypatch):
    # create dummy image
    img = Image.new("RGB", (10, 10), color="white")
    with mock.patch("pytesseract.image_to_string", return_value="line1\nline2"):
        result = app.add_image_to_dataset(img)
    assert "line1" in result
    assert "line2" in result
    assert "line1" in app.dataset and "line2" in app.dataset


def test_add_text_multiline():
    text = "line1\nline2\n"
    result = app.add_text_to_dataset(text)
    assert result.splitlines() == ["line1", "line2"]
    assert app.dataset == ["line1", "line2"]


def test_generate_reply_and_chat(monkeypatch):
    app.dataset.clear()
    # if dataset empty -> catchphrase
    reply = app.generate_reply([], "hi")
    assert reply == app.persona.catchphrase

    app.dataset.extend(["foo", "bar"])
    reply2 = app.generate_reply([], "hi")
    assert reply2 in app.dataset

    history = []
    history = app.chat(history, "hi")
    assert len(history) == 1
    assert history[0][0] == "hi"
    assert history[0][1] in app.dataset

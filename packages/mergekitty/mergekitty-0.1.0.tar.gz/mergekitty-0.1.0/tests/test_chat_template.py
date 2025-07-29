# Partly Copyright (C) 2025 Arcee AI
# Partly Copyright (C) 2025 Allura-org
from typing import Optional

import pytest
from common import make_picollama, make_tokenizer, run_and_check_merge
from transformers import AutoTokenizer

from mergekitty.config import InputModelDefinition, MergeConfiguration


def check_chat_template(model_path: str, needle: Optional[str] = None):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if needle is None:
        assert not tokenizer.chat_template, "Expected no chat template"
        return
    assert tokenizer.chat_template and needle in tokenizer.chat_template, (
        f"Expected chat template to contain {needle}"
    )


@pytest.fixture(scope="session")
def model_base(tmp_path_factory):
    model_path = make_picollama(tmp_path_factory.mktemp("model_base"), vocab_size=64)
    make_tokenizer(vocab_size=64, added_tokens=[]).save_pretrained(model_path)
    return model_path


@pytest.fixture(scope="session")
def model_b(tmp_path_factory):
    model_path = make_picollama(tmp_path_factory.mktemp("model_b"), vocab_size=64)
    make_tokenizer(vocab_size=64, added_tokens=[]).save_pretrained(model_path)
    return model_path


class TestChatTemplate:
    def test_template_chatml(self, model_base, model_b):
        config = MergeConfiguration(
            merge_method="linear",
            models=[
                InputModelDefinition(model=model_base, parameters={"weight": 0.5}),
                InputModelDefinition(model=model_b, parameters={"weight": 0.5}),
            ],
            base_model=model_base,
            dtype="bfloat16",
            chat_template="chatml",
        )
        run_and_check_merge(
            config,
            validate=lambda p: check_chat_template(p, "<|im_start|>"),
        )

    def test_template_literal_jinja(self, model_base, model_b):
        config = MergeConfiguration(
            merge_method="linear",
            models=[
                InputModelDefinition(model=model_base, parameters={"weight": 0.5}),
                InputModelDefinition(model=model_b, parameters={"weight": 0.5}),
            ],
            base_model=model_base,
            dtype="bfloat16",
            chat_template="{{messages[0]['content']}}",
        )
        run_and_check_merge(
            config,
            validate=lambda p: check_chat_template(p, "{{messages[0]['content']}}"),
        )

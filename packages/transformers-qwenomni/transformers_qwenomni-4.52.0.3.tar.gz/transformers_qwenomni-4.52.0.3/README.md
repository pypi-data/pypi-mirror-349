<!---
Copyright 2020 The HuggingFace Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->



<p align="center">
    <i>This repository is a fork of <a href="https://github.com/huggingface/transformers">https://github.com/huggingface/transformers</a>.</i>

    This library has most recent code of Transformers that supports Qwen 2.5 Omni Model
</p>

Transformers is a library of pretrained text, computer vision, audio, video, and multimodal models for inference and training. Use Transformers to fine-tune models on your data, build inference applications, and for generative AI use cases across multiple modalities.
## Installation

Transformers works with Python 3.9+ [PyTorch](https://pytorch.org/get-started/locally/) 2.1+, [TensorFlow](https://www.tensorflow.org/install/pip) 2.6+, and [Flax](https://flax.readthedocs.io/en/latest/) 0.4.1+.

Create and activate a virtual environment with [venv](https://docs.python.org/3/library/venv.html) or [uv](https://docs.astral.sh/uv/), a fast Rust-based Python package and project manager.

```py
# venv
python -m venv .my-env
source .my-env/bin/activate
# uv
uv venv .my-env
source .my-env/bin/activate
```

Install Transformers in your virtual environment.

```py
# pip
pip install transformers-qwenomni

# uv
uv pip install transformers-qwenomni
```

Install Transformers from source if you want the latest changes in the library or are interested in contributing. However, the *latest* version may not be stable. Feel free to open an [issue](https://github.com/huggingface/transformers/issues) if you encounter an error.

```shell
git clone https://github.com/huggingface/transformers.git
cd transformers

# pip
pip install .[torch]

# uv
uv pip install .[torch]
```

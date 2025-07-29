# mergekitty

`mergekitty` is a toolkit for merging pre-trained language models. `mergekitty` uses an out-of-core approach to perform unreasonably elaborate merges in resource-constrained situations. Merges can be run entirely on CPU or accelerated with as little as 8 GB of VRAM. Many merging algorithms are supported, with more coming as they catch my attention.

## Contents

- [Reasons for the fork](#reasons-for-the-fork)
- [Breaking changes](#breaking-changes)
- [Why Merge Models?](#why-merge-models)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Merge Configuration](#merge-configuration)
  - [Parameter Specification](#parameter-specification)
  - [Tokenizer Configuration](#tokenizer-configuration)
  - [Chat Template Configuration](#chat-template-configuration)
  - [Examples](#examples)
- [Merge Methods](#merge-methods)
- [LoRA extraction](#lora-extraction)
- [Mixture of Experts merging](#mixture-of-experts-merging)
- [Development](#development)
- [Citation](#citation)

## Reasons for the fork

This project is a fork of `mergekit` by Arcee.ai, and originally created by Charles Goddard. This fork was created from the last LGPL licensed commit from the original `mergekit` repository, mainly due to it's anti-community switch to the source-available BSL license (in light of how much work the *community* did to make `mergekit` what it is today).

## Breaking changes

This fork is a work in progress. Here are some of the breaking changes we've made so far:

- ALL SCRIPTS, LIBRARY NAMES, ETC HAVE BEEN RENAMED TO `mergekitty`. THIS ONE IS BIG (but you can just replace `mergekit` with `mergekitty` in your codebase/scripts and it will work)
- legacy tokenizer copying has been removed -- `tokenizer_source` now defaults to `"base"`, which is the same as the legacy functionality
- `bakllama` and `mergekit-legacy` have been removed. if someone can give me a real (not fake) use for them then they will be added back.
- `mergekit-evolve` has been removed. if anyone can give me a real reason why it should remain a wart tacked onto the rest of mergekit instead of an out-of-tree tool that depends on mergekit, I'll reconsider.
- `nuslerp` has been renamed to `slerp` (and the original `slerp` has been removed), and it now supports using the parameter `t` (SLERP behavior) OR tensor parameter `weight` (NuSLERP behavior) to specify the weighting of a given tensor.
- moved from `black` and `isort` to `ruff` for formatting, as well as enabling linting for the whole package.
- moved from `setuptools` to `hatch` for building and distributing the package.

## Why Merge Models?

Model merging is a powerful technique that allows combining the strengths of different models without the computational overhead of ensembling or the need for additional training. By operating directly in the weight space of models, merging can:

- Combine multiple specialized models into a single versatile model
- Transfer capabilities between models without access to training data
- Find optimal trade-offs between different model behaviors
- Improve performance while maintaining inference costs
- Create new capabilities through creative model combinations

Unlike traditional ensembling which requires running multiple models, merged models maintain the same inference cost as a single model while often achieving comparable or superior performance.

## Features

Key features of `mergekitty` include:

- Supports Llama, Mistral, GPT-NeoX, StableLM, and more
- Many [merge methods](#merge-methods)
- GPU or CPU execution
- Lazy loading of tensors for low memory use
- Interpolated gradients for parameter values (inspired by Gryphe's [BlockMerge_Gradient](https://github.com/Gryphe/BlockMerge_Gradient) script)
- Piecewise assembly of language models from layers ("Frankenmerging")
- [Mixture of Experts merging](#mixture-of-experts-merging)
- [LORA extraction](#lora-extraction)

## Installation

`mergekitty` is available on PyPI.

Using `uv` to install in a separate tool environment (recommended):
```sh
uv tool install mergekitty
```

Using `pip`:
```sh
pip install mergekitty
```

From source:
```sh
git clone https://github.com/allura-org/mergekitty.git
cd mergekitty

pip install -e .  # install the package and make scripts available
```

## Usage

The script `mergekitty-yaml` is the main entry point for `mergekitty`. It takes a YAML configuration file and an output path, like so:

```sh
mergekitty-yaml path/to/your/config.yml ./output-model-directory [--cuda] [--lazy-unpickle] [--allow-crimes] [... other options]
```

This will run the merge and write your merged model to `./output-model-directory`.

For more information on the arguments accepted by `mergekitty-yaml` run the command `mergekitty-yaml --help`.

### Uploading to Huggingface

When you have a merged model you're happy with, you may want to share it on the Hugging Face Hub. `mergekitty` generates a `README.md` for your merge with some basic information for a model card. You can edit it to include more details about your merge, like giving it a good name or explaining what it's good at; rewrite it entirely; or use the generated `README.md` as-is. It is also possible to edit your `README.md` online once it has been uploaded to the Hub.

Once you're happy with your model card and merged model, you can upload it to the Hugging Face Hub using the [huggingface_hub](https://huggingface.co/docs/huggingface_hub/index) Python library.

```sh
# log in to huggingface with an access token (must have write permission)
huggingface-cli login
# upload your model
huggingface-cli upload your_hf_username/my-cool-model ./output-model-directory .
```

The [documentation](https://huggingface.co/docs/huggingface_hub/guides/cli#huggingface-cli-upload) for `huggingface_hub` goes into more detail about other options for uploading.

## Merge Configuration

Merge configurations are YAML documents specifying the operations to perform in order to produce your merged model.
Below are the primary elements of a configuration file:

- `merge_method`: Specifies the method to use for merging models. See [Merge Methods](#merge-methods) for a list.
- `slices`: Defines slices of layers from different models to be used. This field is mutually exclusive with `models`.
- `models`: Defines entire models to be used for merging. This field is mutually exclusive with `slices`.
- `base_model`: Specifies the base model used in some merging methods.
- `parameters`: Holds various parameters such as weights and densities, which can also be specified at different levels of the configuration.
- `dtype`: Specifies the data type used for the merging operation.
- `tokenizer` or `tokenizer_source`: Determines how to construct a tokenizer for the merged model.
- `chat_template`: Specifies a chat template for the merged model.

### Parameter Specification

Parameters are flexible and can be set with varying precedence. They can be specified conditionally using tensor name filters, which allows finer control such as differentiating between attention heads and fully connected layers.

Parameters can be specified as:

- **Scalars**: Single floating-point values.
- **Gradients**: List of floating-point values, specifying an interpolated gradient.

The parameters can be set at different levels, with decreasing precedence as follows:

1. `slices.*.sources.parameters` - applying to a specific input slice
2. `slices.*.parameters` - applying to a specific output slice
3. `models.*.parameters` or `input_model_parameters` - applying to any tensors coming from specific input models
4. `parameters` - catchall

### Tokenizer Configuration

The tokenizer behavior can be configured in two ways: using the new `tokenizer` field (recommended) or the legacy `tokenizer_source` field (maintained for backward compatibility). These fields are mutually exclusive - you should use one or the other, not both.

#### Modern Configuration (tokenizer)

The `tokenizer` field provides fine-grained control over vocabulary and embeddings:

```yaml
tokenizer:
  source: "union"  # or "base" or a specific model path
  tokens:          # Optional: configure specific tokens
    <token_name>:
      source: ...  # Specify embedding source
      force: false # Optional: force this embedding for all models
  pad_to_multiple_of: null  # Optional: pad vocabulary size
```

##### Tokenizer Source

The `source` field determines the vocabulary of the output model:

- `union`: Combine vocabularies from all input models (default)
- `base`: Use vocabulary from the base model
- `"path/to/model"`: Use vocabulary from a specific model

##### Token Embedding Handling

When merging models with different vocabularies, `mergekitty` uses smart defaults to handle token embeddings:

- If a token exists in the base model, its embedding is used as the default
- If only one model has the token, that model's embedding is used
- Otherwise, an average of all available embeddings is used

You can override these defaults for specific tokens:

```yaml
tokenizer:
  source: union
  tokens:
    # Use embedding from a specific model
    <|im_start|>:
      source: "path/to/chatml/model"

    # Force a specific embedding for all models
    <|special|>:
      source: "path/to/model"
      force: true

    # Map a token to another model's token embedding
    <|renamed_token|>:
      source:
        kind: "model_token"
        model: "path/to/model"
        token: "<|original_token|>"  # or use token_id: 1234
```

##### Practical Example

Here's how you might preserve both Llama 3 Instruct and ChatML prompt formats when merging models:

```yaml
tokenizer:
  source: union
  tokens:
    # ChatML tokens
    <|im_start|>:
      source: "chatml_model"
    <|im_end|>:
      source: "chatml_model"

    # Llama 3 tokens - force original embeddings
    <|start_header_id|>:
      source: "llama3_model"
      force: true
    <|end_header_id|>:
      source: "llama3_model"
      force: true
    <|eot_id|>:
      source: "llama3_model"
      force: true
```

#### Legacy Configuration (tokenizer_source)

For backward compatibility, the `tokenizer_source` field is still supported:

```yaml
tokenizer_source: "union"  # or "base" or a model path
```

This provides basic tokenizer selection but lacks the fine-grained control of the modern `tokenizer` field.

### Chat Template Configuration

The optional `chat_template` field allows overriding the chat template used for the merged model.

```yaml
chat_template: "auto"  # or a template name or Jinja2 template
```

Options include:

- `"auto"`: Automatically select the most common template among input models
- Built-in templates: `"alpaca"`, `"chatml"`, `"llama3"`, `"mistral"`, `"exaone"`
- A Jinja2 template string for custom formatting

### Examples

Several examples of merge configurations are available in [`examples/`](examples/).

## Merge Methods

A quick overview of the currently supported merge methods:

| Method                                                                                           | `merge_method` value | Multi-Model | Uses base model |
| ------------------------------------------------------------------------------------------------ | -------------------- | ----------- | --------------- |
| Linear ([Model Soups](https://arxiv.org/abs/2203.05482))                                         | `linear`             | ✅          | ❌              |
| SLERP                                                                                            | `slerp`              | ✅*         | ✅              |
| Nearswap                                                                                         | `nearswap`           | ❌          | ✅              |
| [Task Arithmetic](https://arxiv.org/abs/2212.04089)                                              | `task_arithmetic`    | ✅          | ✅              |
| [TIES](https://arxiv.org/abs/2306.01708)                                                         | `ties`               | ✅          | ✅              |
| [DARE](https://arxiv.org/abs/2311.03099) [TIES](https://arxiv.org/abs/2306.01708)                | `dare_ties`          | ✅          | ✅              |
| [DARE](https://arxiv.org/abs/2311.03099) [Task Arithmetic](https://arxiv.org/abs/2212.04089)     | `dare_linear`        | ✅          | ✅              |
| Passthrough                                                                                      | `passthrough`        | ❌          | ❌              |
| [Model Breadcrumbs](https://arxiv.org/abs/2312.06795)                                            | `breadcrumbs`        | ✅          | ✅              |
| [Model Breadcrumbs](https://arxiv.org/abs/2312.06795) + [TIES](https://arxiv.org/abs/2306.01708) | `breadcrumbs_ties`   | ✅          | ✅              |
| [Model Stock](https://arxiv.org/abs/2403.19522)                                                  | `model_stock`        | ✅          | ✅              |
| [DELLA](https://arxiv.org/abs/2406.11617)                                                        | `della`              | ✅          | ✅              |
| [DELLA](https://arxiv.org/abs/2406.11617) [Task Arithmetic](https://arxiv.org/abs/2212.04089)    | `della_linear`       | ✅          | ✅              |
| [SCE](https://arxiv.org/abs/2408.07990)                                                          | `sce`                | ✅          | ✅              |
\* only supports two to three models

### Linear

The classic merge method - a simple weighted average.

Parameters:

- `weight` - relative (or absolute if `normalize=False`) weighting of a given tensor
- `normalize` - if true, the weights of all models contributing to a tensor will be normalized. Default behavior.

### SLERP

Spherically interpolate model parameters with support for both traditional interpolation (`t`) and tensor-specific weighting (`weight`). Works with two models or two task vectors and an optional base model.

Parameters:

One of the following parameters must be specified:

- `t` - interpolation factor. At `t=0` will return `base_model`, at `t=1` will return the other model. if specified, `weight` will be ignored. (only supports one base model and one non-base model)
- `weight` - relative weighting of a given tensor. (supports one base model, and either one or two non-base models)

Additionally, the following parameters are supported:

- `nuslerp_flatten`: set to false to do row-wise/column-wise interpolation instead of treating tensors as vectors
- `nuslerp_row_wise`: SLERP row vectors instead of column vectors

### Nearswap

Interpolates base model with secondary model if similarity is below t. Accepts two models.

Parameters:

- `t` - similarity threshold

### [Task Arithmetic](https://arxiv.org/abs/2212.04089)

Computes "task vectors" for each model by subtracting a base model. Merges the task vectors linearly and adds back the base. Works great for models that were fine tuned from a common ancestor. Also a super useful mental framework for several of the more involved merge methods.

Parameters: same as [Linear](#linear)

### [TIES](https://arxiv.org/abs/2306.01708)

Builds on the task arithmetic framework. Resolves interference between models by sparsifying the task vectors and applying a sign consensus algorithm. Allows you to merge a larger number of models and retain more of their strengths.

Parameters: same as [Linear](#linear), plus:

- `density` - fraction of weights in differences from the base model to retain

### [DARE](https://arxiv.org/abs/2311.03099)

In the same vein as TIES, sparsifies task vectors to reduce interference. Differs in that DARE uses random pruning with a novel rescaling to better match performance of the original models. DARE can be used either with the sign consensus algorithm of TIES (`dare_ties`) or without (`dare_linear`).

Parameters: same as [TIES](#ties) for `dare_ties`, or [Linear](#linear) for `dare_linear`

### Passthrough

`passthrough` is a no-op that simply passes input tensors through unmodified. It is meant to be used for layer-stacking type merges where you have only one input model. Useful for frankenmerging.

### [Model Breadcrumbs](https://arxiv.org/abs/2312.06795)

An extension of task arithmetic that discards both small and extremely large differences from the base model. As with DARE, the Model Breadcrumbs algorithm can be used with (`breadcrumbs_ties`) or without (`breadcrumbs`) the sign consensus algorithm of TIES.

Parameters: same as [Linear](#linear), plus:

- `density` - fraction of weights in differences from the base model to retain
- `gamma` - fraction of largest magnitude differences to remove

Note that `gamma` corresponds with the parameter `β` described in the paper, while `density` is the final density of the sparsified tensors (related to `γ` and `β` by `density = 1 - γ - β`). For good default values, try `density: 0.9` and `gamma: 0.01`.

### [Model Stock](https://arxiv.org/abs/2403.19522)

Uses some neat geometric properties of fine tuned models to compute good weights for linear interpolation. Requires at least three models, including a base model.

Parameters:

- `filter_wise`: if true, weight calculation will be per-row rather than per-tensor. Not recommended.

### [DELLA](https://arxiv.org/abs/2406.11617)

Building upon DARE, DELLA uses adaptive pruning based on parameter magnitudes. DELLA first ranks parameters in each row of delta parameters and assigns drop probabilities inversely proportional to their magnitudes. This allows it to retain more important changes while reducing interference. After pruning, it rescales the remaining parameters similar to [DARE](#dare). DELLA can be used with (`della`) or without (`della_linear`) the sign elect step of TIES

Parameters: same as [Linear](#linear), plus:

- `density` - fraction of weights in differences from the base model to retain
- `epsilon` - maximum change in drop probability based on magnitude. Drop probabilities assigned will range from `density - epsilon` to `density + epsilon`. (When selecting values for `density` and `epsilon`, ensure that the range of probabilities falls within 0 to 1)
- `lambda` - scaling factor for the final merged delta parameters before merging with the base parameters.

### [SCE](https://arxiv.org/abs/2408.07990)

SCE introduces adaptive matrix-level merging weights based on parameter variances. SCE first selects the top-k% elements from each parameter matrix that exhibit high variance across all delta parameters. Following this selection, SCE calculates matrix-level merging weights based on the sum of squares of elements in the delta parameters. Finally, it erases minority elements, a step similar to the sign election process in TIES.

Parameters:

- `select_topk` - fraction of elements with the highest variance in the delta parameters to retain.

## LoRA extraction

`mergekitty` allows extracting PEFT-compatible low-rank approximations of finetuned models.

### Usage

```sh
mergekitty-extract-lora finetuned_model_id_or_path base_model_id_or_path output_path [--no-lazy-unpickle] --rank=desired_rank
```

## Mixture of Experts merging

The `mergekitty-moe` script supports merging multiple dense models into a mixture of experts, either for direct use or for further training. For more details see the [`mergekit-moe` documentation](docs/moe.md).

## Development

`mergekitty` is developed using Hatch and UV. My recommended setup:
```sh
# after installing uv:
uv tool install hatch
hatch test # run tests
hatch run lint # run ruff
hatch run format # run ruff format
hatch run mergekitty-yaml examples/bio-merge.yml ./bio-merge --cuda # run a test merge
```

## Citation

If you find `mergekitty` useful in your research, please consider citing the [original `mergekit` paper](https://aclanthology.org/2024.emnlp-industry.36/):


```bibtex
@inproceedings{goddard-etal-2024-arcees,
    title = "Arcee{'}s {M}erge{K}it: A Toolkit for Merging Large Language Models",
    author = "Goddard, Charles  and
      Siriwardhana, Shamane  and
      Ehghaghi, Malikeh  and
      Meyers, Luke  and
      Karpukhin, Vladimir  and
      Benedict, Brian  and
      McQuade, Mark  and
      Solawetz, Jacob",
    editor = "Dernoncourt, Franck  and
      Preo{\c{t}}iuc-Pietro, Daniel  and
      Shimorina, Anastasia",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track",
    month = nov,
    year = "2024",
    address = "Miami, Florida, US",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-industry.36",
    doi = "10.18653/v1/2024.emnlp-industry.36",
    pages = "477--485",
    abstract = "The rapid growth of open-source language models provides the opportunity to merge model checkpoints, combining their parameters to improve performance and versatility. Advances in transfer learning have led to numerous task-specific models, which model merging can integrate into powerful multitask models without additional training. MergeKit is an open-source library designed to support this process with an efficient and extensible framework suitable for any hardware. It has facilitated the merging of thousands of models, contributing to some of the world{'}s most powerful open-source model checkpoints. The library is accessible at: https://github.com/arcee-ai/mergekit.",
}
```

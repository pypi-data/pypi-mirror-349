
![Banner](https://amirivojdan.io/wp-content/uploads/2025/01/shekar-lib.png)

<p align="center">
    <em>Simplifying Persian NLP for Everyone</em>
</p>

<p align="center">
 <a href="https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml" target="_blank">
 <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml?color=00A693">
</a>
<a href="https://pypi.org/project/shekar" target="_blank">
    <img src="https://img.shields.io/pypi/v/shekar?color=00A693" alt="Package version">
</a>

<a href="https://pypi.org/project/shekar" target="_blank">
    <img src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Famirivojdan%2Fshekar%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&color=00A693" alt="Supported Python versions">
</a>
</p>

Shekar (meaning 'sugar' in Persian) is a Python library for Persian natural language processing, named after the influential satirical story *"فارسی شکر است"* (Persian is Sugar) published in 1921 by Mohammad Ali Jamalzadeh.
The story became a cornerstone of Iran's literary renaissance, advocating for accessible yet eloquent expression.
## Installation

To install the package, you can use **`pip`**. Run the following command:

<!-- termynal -->
```bash
$ pip install shekar
```

## Usage

### Normalization

The **`Normalizer`** is built on top of the **`Pipeline`** class, meaning it inherits all its features, including batch processing, argument decorators, and callability. This makes the Normalizer both powerful and flexible: you can use it directly for comprehensive Persian text normalization.

```python

from shekar import Normalizer
normalizer = Normalizer()

text = "ۿدف ما ػمګ بۀ ێڪډيڱڕ أښټ"
text = normalizer.fit_transform(text) # Output: هدف ما کمک به یکدیگر است
print(text)
```
```shell
هدف ما کمک به یکدیگر است
```

#### Batch Support
You can apply the normalizer to a list of strings to enable batch processing.

```python
texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = normalizer.fit_transform(texts)
# outputs = normalizer(texts) # Normalizer is callable! 
print(outputs)
# ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]
```

#### Normalizer Decorator
Use normalizer decorator to normalize specific arguments.
```python
@normalizer.on_args(["text"])
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
# Output: "تو را من چشم در راهم"
```

## Custom Normalization Pipeline

The **`Pipeline`** class enables you to chain together multiple preprocessing steps into a single, reusable transformation flow. It is particularly useful when you want to apply several text normalization, cleaning, or masking operations in sequence. The **`Pipeline`** is fully compatible with all preprocessors in **`shekar.preprocessing`**.

### Example Pipeline

```python
from shekar import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover

steps = [
    ("removeEmoji", EmojiRemover()),
    ("removePunct", PunctuationRemover()),
]

pipeline = Pipeline(steps= steps)

text = "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!"
output = pipeline.fit_transform(text)
print(output)  # Output: "پرنده‌های  قفسی عادت دارن به بی‌کسی"
```

#### Batch and Decorator Support

Note that **`Pipeline`** objects are **callable**, meaning you can use them like functions to process input data directly.

```python

texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = pipeline(texts)
print(outputs)
# ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]

# Use decorator to apply pipeline on specific arguments
@pipeline.on_args("text")
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
# Output: "تو را من چشم در راهم"
```

## Sentence Tokenization

```python

from shekar.tokenizers import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
tokenizer = SentenceTokenizer()
sentences = tokenizer.tokenize(text)

for sentence in sentences:
    print(sentence)
```

```output
هدف ما کمک به یکدیگر است!
ما می‌توانیم با هم کار کنیم.
```


## WordCloud

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/word_cloud.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/word_cloud.ipynb)

The WordCloud class offers an easy way to create visually rich Persian word clouds. It supports reshaping and right-to-left rendering, Persian fonts, color maps, and custom shape masks for accurate and elegant visualization of word frequencies.

```python
import requests
from collections import Counter

from shekar import WordCloud
from shekar import WordTokenizer
from shekar.preprocessing import (
  HTMLTagRemover,
  PunctuationRemover,
  StopWordRemover,
  NonPersianRemover,
)
preprocessing_pipeline = HTMLTagRemover() | PunctuationRemover() | StopWordRemover() | NonPersianRemover()


url = f"https://ganjoor.net/ferdousi/shahname/siavosh/sh9"
response = requests.get(url)
html_content = response.text
clean_text = preprocessing_pipeline(html_content)

word_tokenizer = WordTokenizer()
tokens = word_tokenizer(clean_text)

counwords = Counter()
for word in tokens:
  counwords[word] += 1

worCloud = WordCloud(
        mask="Iran",
        max_font_size=220,
        min_font_size=5,
        bg_color="white",
        contour_color="black",
        contour_width=5,
        color_map="Greens",
    )

image = worCloud.generate(counwords)
image.show()
```

![](https://raw.githubusercontent.com/amirivojdan/shekar/main/assets/wordcloud_example.png)
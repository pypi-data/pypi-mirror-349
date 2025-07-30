# synapse\_ai\_tools

`synapse_ai_tools` is a Python package developed by **SYNAPSE AI SAS**. It provides utilities for phonetic processing, Mel spectrogram generation, exploratory data analysis (EDA), and interactive deep learning model configuration — especially useful in voice-related AI applications like TTS and voice cloning.

## Installation

```bash
pip install synapse_ai_tools
```

**Requires:** Python > 3.6 and < 3.11
**Recommended versions:**

* `tensorflow==2.10`
* `numpy<2.0`

---

## Modules Overview

### `phonemes` 

Rule-based transformations optimized for Rioplatense Spanish:

* `phoneme(text, punctuation=False)`: Converts Spanish text into a simplified phoneme sequence using context-sensitive linguistic rules (e.g., yeísmo, aspiration, flap /ɾ/, etc.).
* `accent(text, punctuation=False)`: Applies accentuation to each word based on syllabic stress rules.
* `dictionaries(text)`: Returns a phoneme-to-index dictionary and a phoneme frequency dictionary.
* `phoneme_graphs(text, sort=True)`: Displays a bar chart of phoneme frequency distribution.

### `mel_spectrograms` 

* `load_audio_to_mel(file_path, sr=22050, ...)`: Converts an audio file into a Mel spectrogram (in dB scale) using Librosa, with customizable STFT and Mel filter parameters.
* `graph_mel_spectrogram(spectrogram, output_dir='', name='Spectrogram', ...)`: Visualizes and optionally saves the spectrogram image with customizable size, colormap, and layout.

### `eda` 

Utilities for inspecting structured data and feature distributions:

* `nulls(df, column)`: Prints count and percentage of null values in a given column.
* `outliers(df, column, ...)`: Analyzes and visualizes outliers via histograms, boxplots, and summary statistics.
* `heatmap_correlation(df, columns, correlation_type='spearman', ...)`: Displays a correlation heatmap for selected columns.
* `pca_view(df, dimensions=2 or 3, target=None, ...)`: Performs PCA and optionally visualizes it in 2D or 3D, with or without a target variable.

### `ModelConfigurator` 

An interactive Tkinter-based GUI to build deep learning models with the Keras Sequential API:

* Choose problem type: classification or regression
* Define input shape
* Add layers: Dense, Conv1D/2D, Pooling, Dropout, BatchNormalization, LSTM, Bidirectional, Flatten
* Select optimizers, loss functions, metrics
* Export trained model and architecture diagram

**Usage:**

```python
from synapse_ai_tools import ModelConfigurator
ModelConfigurator()
```

**Note:** Due to compatibility, recommended setup:

```bash
pip install tensorflow==2.10 numpy<2.0
```

---

## Use Cases

* Prepare phonetic inputs for voice synthesis or TTS training
* Visualize and debug Mel spectrograms
* Perform quick EDA and dimensionality reduction
* Build deep learning architectures without writing code

---

## Developed by

**SYNAPSE AI SAS**
Advanced solutions in artificial intelligence, speech processing, and applied data science.

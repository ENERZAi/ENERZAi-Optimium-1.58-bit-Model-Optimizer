# ENERZAi Optimium 1.58-bit Model Optimizer

# Qualcomm-containers_optimium_whisper

## 1. Container Functional Overview
The **Qualcomm-containers_optimium_whisper** container is designed to facilitate the deployment and usage of speech to text models powered by our own proprietary inference engine Optimium on edge devices. It provides a pre-configured environment to run high-efficiency AI inference tasks seamlessly.

## 2. Key Features
*   **Architecture:** Built exclusively for **Linux Arm64**.
*   **Runtime:** Includes full support for the **Optimium Runtime**.
*   **Optimization:** Models are specifically optimized for the **Qualcomm QCS6490** chipset.
*   **Language Support:** Supports **English (en)** and **Chinese (zh)**.

## 3. Supported Host Devices
*   Devices based on **Qualcomm QCS6490**.

## 4. Prerequisites
Ensure the following software is installed on the Host OS before deploying:
*   [Docker Engine](https://docs.docker.com/engine/install/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

## 5. Software Components
The container image comes pre-installed with:
*   **Optimium Runtime**
*   **Python 3.10**

## 6. Quick Start Guide

To get started with the container, follow these steps:

### 6.1 Container Build & Run
```bash
docker-compose up -d
```

### 6.2 Access the Container
```bash
docker exec -it containers_optimium_whisper /bin/bash
```

### 6.3 Run Demo
```bash
python demo.py
```

### 6.4 Model Usage
```python
from optimium_whisper.optimium_whisper.util import decode_audio
from optimium_whisper.optimium_whisper.model import OptimiumWhisper

model = OptimiumWhisper(model_path="/models/whisper_advantech_small_en_seqlen_1000") # English fix path
# model = OptimiumWhisper(model_path="/models/whisper_advantech_small_zh_seqlen_1000") # Chinese fix path

audio_data = decode_audio("./Can you recommend three tour sites of Taipei.wav", sampling_rate=16000) # wav to pcm and resampling
sr = 16000
ten_sec = sr * 10
overlap = sr * 2 # 2-second overlap for optimal model performance

chunks = [audio_data[i:i + ten_sec] for i in range(0, len(audio_data), ten_sec - overlap)]
result_text_list = []
for chunk in chunks:
    segments, _ = model.transcribe(chunk, language="en")
    for seg in segments:
        result_text_list.append(seg.text)
transcript = " ".join(result_text_list)
print(transcript)
model.overlap_tokens = [] # Reset if audio is not continuous
```


## 7. Best Practices & Known Limitations
*   **Audio Overlap:** The model is designed to process audio in 10-second units. For continuous audio exceeding 10 seconds, a 2-second overlap is recommended to achieve optimal performance. If the audio segments are not continuous, **model.overlap_tokens** must be reset.
*   **Model Performance:** This model is designed to run exclusively on the CPU.
*   For organizations seeking enhanced real-time capabilities, please contact ENERZAi.

## 8. Performance Benchmarking

The following table compares the performance of **Optimium** against **Fast-Whisper** on the target hardware.

| AI Backend | Model Size | Audio Duration | Threads | Memory (KB) | Encoder Time (ms) | Decoder Time (Tokens / ms per token) | Total Time (ms) | Notes |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Optimium (CPU only)** | Small | 10s | 6 | 160,130 | 1040.23 | 34 / 45.11 | 2746.56 | |
| **Optimium (CPU only)** | Small | 10s | 4 | - | 3067.67 | 34 / 36.33 | 4682.54 | |
| **Optimium (CPU only)** | Small | 10s | Enc: 6<br>Dec: 4 | - | 1051.40 | 34 / 36.33 | 2660.36 | Optimized for 4 performance cores + 4 efficiency cores architecture |
| **Fast-Whisper (CTranslate2)** | Small (INT8) | 10s | 6 | 731,796 | 2386 | 33 / 82.1515 | 5098 |  |

**Table 1.** Performance comparison of AI backends on the target hardware.

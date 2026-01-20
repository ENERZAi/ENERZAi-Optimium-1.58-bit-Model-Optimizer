from optimium_whisper.optimium_whisper.util import decode_audio
from optimium_whisper.optimium_whisper.model import OptimiumWhisper

model = OptimiumWhisper(model_path="/models/whisper_advantech_small_en_seqlen_1000")

audio_data = decode_audio("./Can you recommend three tour sites of Taipei.wav", sampling_rate=16000)
sr = 16000
ten_sec = sr * 10
overlap = sr * 2

chunks = [audio_data[i:i + ten_sec] for i in range(0, len(audio_data), ten_sec - overlap)]
result_text_list = []
for chunk in chunks:
    segments, _ = model.transcribe(chunk, language="en")
    for seg in segments:
        result_text_list.append(seg.text)
transcript = " ".join(result_text_list)
print(transcript)
model.overlap_tokens = []
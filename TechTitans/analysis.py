import os
import numpy as np
import imageio_ffmpeg
import whisper
import subprocess
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import textstat

# Download nltk data
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

# ── Load Whisper ──────────────────────────────
model = whisper.load_model("base")
print("Whisper loaded!")

# ── Find latest wav ───────────────────────────
folder = "recordings"
files = [f for f in os.listdir(folder) if f.endswith(".wav")]
latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(folder, x)))
audio_file = os.path.join(folder, latest_file)
print("Using file:", audio_file)

# ── Decode audio via imageio ffmpeg ──────────
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg_exe,
    "-i", audio_file,
    "-f", "s16le",
    "-ac", "1",
    "-ar", "16000",
    "-"
]
out = subprocess.run(cmd, capture_output=True)
audio_array = np.frombuffer(out.stdout, dtype=np.int16).astype(np.float32) / 32768.0

# ── Transcribe ────────────────────────────────
print("\nTranscribing... (may take a minute)")
result = model.transcribe(audio_array)
text = result["text"].strip()

print("\n" + "="*50)
print("TRANSCRIPTION:")
print("="*50)
print(text)

# ── Evaluate ──────────────────────────────────
words       = word_tokenize(text.lower())
sentences   = sent_tokenize(text)
word_count  = len(words)
sent_count  = len(sentences)

# Duration from audio array
duration_sec = len(audio_array) / 16000
wpm = round((word_count / max(duration_sec, 1)) * 60, 1)

# Filler words
fillers = {"um","uh","like","you know","basically","literally","actually","so","right","okay","hmm","ah","er"}
filler_count = sum(1 for w in words if w in fillers)
filler_ratio = filler_count / max(word_count, 1)

# Scores
readability     = textstat.flesch_reading_ease(text)
clarity_score   = min(10, max(0, round(readability / 10, 1)))
confidence_score= round(max(0, 10 - (filler_ratio * 100)), 1)
avg_sent_len    = round(word_count / max(sent_count, 1), 1)

if 10 <= avg_sent_len <= 25:
    structure_score = 10.0
elif avg_sent_len < 10:
    structure_score = round(avg_sent_len, 1)
else:
    structure_score = round(max(0, 10 - (avg_sent_len - 25) * 0.2), 1)

overall = round((clarity_score * 0.35) + (confidence_score * 0.40) + (structure_score * 0.25), 1)

# ── Feedback ──────────────────────────────────
strengths, weaknesses, improvements = [], [], []

if filler_ratio < 0.05:
    strengths.append("Minimal filler words — speaks confidently")
elif filler_ratio < 0.10:
    weaknesses.append(f"Moderate filler word usage ({round(filler_ratio*100,1)}%)")
    improvements.append("Practice pausing silently instead of using um/uh")
else:
    weaknesses.append(f"High filler word usage ({round(filler_ratio*100,1)}%)")
    improvements.append("Replace fillers with deliberate pauses")

if 120 <= wpm <= 160:
    strengths.append(f"Good speaking pace ({wpm} wpm)")
elif wpm < 100:
    weaknesses.append(f"Speaking too slowly ({wpm} wpm)")
    improvements.append("Aim for 120-160 words per minute")
elif wpm > 180:
    weaknesses.append(f"Speaking too fast ({wpm} wpm)")
    improvements.append("Slow down and breathe between key points")

if clarity_score >= 7:
    strengths.append("Clear and easy to understand language")
else:
    weaknesses.append("Answer readability is low")
    improvements.append("Use shorter sentences and simpler vocabulary")

if structure_score >= 8:
    strengths.append("Well structured sentences")
else:
    weaknesses.append("Sentence structure needs improvement")
    improvements.append("Use STAR method: Situation, Task, Action, Result")

# ── Print Report ──────────────────────────────
print("\n" + "="*50)
print("INTERVIEW FEEDBACK REPORT")
print("="*50)
print(f"Overall Score   : {overall} / 10")
print(f"Clarity         : {clarity_score} / 10")
print(f"Confidence      : {confidence_score} / 10")
print(f"Structure       : {structure_score} / 10")
print(f"\nStats:")
print(f"  Word Count    : {word_count}")
print(f"  Filler Words  : {filler_count} ({round(filler_ratio*100,1)}%)")
print(f"  Speaking Pace : {wpm} wpm")
print(f"  Duration      : {round(duration_sec, 1)}s")
print(f"\nStrengths:")
for s in strengths:   print(f"  ✓ {s}")
print(f"\nWeaknesses:")
for w in weaknesses:  print(f"  ✗ {w}")
print(f"\nImprovements:")
for i in improvements: print(f"  → {i}")
print("="*50)
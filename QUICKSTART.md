# VoiceDoc AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Run Locally (Recommended for Testing)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/VoiceDoc-AI.git
cd VoiceDoc-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the demo
python voicedoc_demo.py

# 4. Select demo mode (1-5)
# Choose option 1 for automated tests
```

### Option 2: Google Colab (Recommended for Full Gemma 4)

1. Open the notebook: `VoiceDoc_Colab.ipynb`
2. Click "Open in Colab"
3. Run cells sequentially
4. Uncomment the Gemma 4 loading cell to use actual model

### Option 3: Kaggle Notebook

1. Create new Kaggle notebook
2. Upload `VoiceDoc_Colab.ipynb`
3. Run with Kaggle GPU

---

## 📊 Demo Modes

### Mode 1: Automated Test Cases
Tests 4 different scenarios (mild, moderate, severe, wound)
```bash
python voicedoc_demo.py
# Select option 1
```

### Mode 2: Interactive Input
Enter your own symptoms and get triage
```bash
python voicedoc_demo.py
# Select option 2
```

### Mode 3: Batch Testing
Run 5 test cases and see summary table
```bash
python voicedoc_demo.py
# Select option 3
```

### Mode 4: ML Engine Deep Dive
See how symptom extraction and risk scoring work
```bash
python voicedoc_demo.py
# Select option 4
```

---

## 🔧 Using the API

### Basic Usage

```python
from voicedoc_core import VoiceDocCore

# Initialize
voicedoc = VoiceDocCore(use_gemma=False)

# Get triage
result = voicedoc.triage_with_function_calling(
    symptoms_text="High fever and cough for 3 days",
    duration_days=3,
    has_fever=True
)

# Access results
print(f"Triage: {result.triage_level}")
print(f"Risk Score: {result.risk_score}/100")
print(f"Confidence: {result.confidence*100:.0f}%")
```

### With Audio Input

```python
# Process audio file
transcription = voicedoc.process_audio_asr(
    audio_path="symptom_recording.wav",
    language="hi"  # Hindi
)

# Get triage from transcription
result = voicedoc.triage_with_function_calling(
    symptoms_text=transcription,
    duration_days=2,
    has_fever=True
)
```

### With Image Analysis

```python
# Analyze medical image
image_analysis = voicedoc.process_image_vision(
    image_path="wound_photo.jpg"
)

# Include in triage
result = voicedoc.triage_with_function_calling(
    symptoms_text="I have a cut on my leg",
    duration_days=1,
    has_fever=False,
    image_analysis=image_analysis
)
```

---

## 📁 Project Structure

```
VoiceDoc-AI/
├── voicedoc_core.py           # Main system (Gemma 4 integration)
├── ml_engine.py               # ML risk scoring
├── voicedoc_demo.py           # Interactive demo
├── VoiceDoc_Colab.ipynb       # Jupyter notebook
├── requirements.txt           # Dependencies
├── KAGGLE_WRITEUP.md          # Competition writeup
├── QUICKSTART.md              # This file
└── README.md                  # Full documentation
```

---

## 🎯 Key Classes

### VoiceDocCore
Main system class
```python
voicedoc = VoiceDocCore(use_gemma=True)  # Use actual Gemma 4
voicedoc = VoiceDocCore(use_gemma=False) # Use mock (for testing)

# Methods
voicedoc.process_audio_asr(audio_path, language)
voicedoc.process_image_vision(image_path)
voicedoc.triage_with_function_calling(symptoms_text, duration_days, has_fever)
voicedoc.format_triage_output(result)
```

### MedicalTriageEngine
ML risk scoring
```python
from ml_engine import MedicalTriageEngine

engine = MedicalTriageEngine()

# Extract symptoms
symptoms = engine.extract_symptoms("I have fever and cough")

# Calculate risk
risk = engine.calculate_risk_score(symptoms, duration_days=2, has_fever=True)

# Get recommendations
recs = engine.get_recommendations(risk['triage_level'], symptoms[0][0])
```

---

## 🧪 Testing

### Run All Tests
```bash
python voicedoc_demo.py
# Select option 5 (Run all demos)
```

### Test ML Engine Only
```python
from ml_engine import MedicalTriageEngine

engine = MedicalTriageEngine()
report = engine.generate_triage_report(
    "High fever and cough",
    duration_days=2,
    has_fever=True
)
print(report)
```

---

## 🚀 Deployment

### Ollama (Raspberry Pi)

```bash
# On Raspberry Pi 5
curl https://ollama.ai/install.sh | sh
ollama pull gemma4-e4b

# Run VoiceDoc server
python voicedoc_ollama_server.py

# Access via local WiFi
# http://raspberrypi.local:8000
```

### LiteRT (Android)

See `android_deployment/` directory for MediaPipe integration.

### Colab (Development)

```python
# In Colab cell
voicedoc = VoiceDocCore(use_gemma=True)
result = voicedoc.triage_with_function_calling(...)
```

---

## 📊 Expected Output

```
🟡 TRIAGE LEVEL: YELLOW
   MODERATE URGENCY - See doctor within 24 hours

Risk Score: 65/100
Confidence: 88%

Primary Symptom: fever
Detected Symptoms: fever, cough, body ache

Home Care Instructions:
  1. Rest and avoid strenuous activity
  2. Stay hydrated
  3. Monitor vital signs (temperature, breathing)
  4. Take prescribed medications as directed

Escalation Guidance: Seek medical attention within 24 hours

Reasoning: Primary symptom: fever | Symptoms persisting for 3 days (elevated risk) | Fever present (increases risk) | Moderate risk - medical attention recommended
```

---

## 🐛 Troubleshooting

### ImportError: No module named 'transformers'
```bash
pip install transformers torch accelerate
```

### CUDA out of memory
- Use `use_gemma=False` for testing
- Or reduce batch size in Colab

### Audio processing error
```bash
pip install librosa soundfile
```

### Image processing error
```bash
pip install Pillow
```

---

## 📝 Next Steps

1. **Test locally** with `python voicedoc_demo.py`
2. **Run in Colab** with `VoiceDoc_Colab.ipynb`
3. **Load Gemma 4** by setting `use_gemma=True`
4. **Deploy on Ollama** for Raspberry Pi
5. **Create video demo** showing real-world usage
6. **Submit to Kaggle** with writeup + code + video

---

## 🤝 Contributing

Found a bug? Have an idea? Open an issue or PR!

---

## 📄 License

Apache 2.0 - Free for commercial use

---

**Questions?** Check the full README.md or open an issue on GitHub.

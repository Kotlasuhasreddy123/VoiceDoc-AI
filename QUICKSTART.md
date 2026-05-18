# VoiceDoc AI — Quick Start Guide

## Get Running in 2 Minutes

### Minimal install (no GPU needed)

```bash
git clone https://github.com/Kotlasuhasreddy123/VoiceDoc-AI.git
cd VoiceDoc-AI
pip install scikit-learn numpy pandas Pillow
python voicedoc_demo.py
```

### Full install (all 7 features)

```bash
pip install -r requirements.txt
python voicedoc_demo.py
```

---

## Demo Modes

When you run `python voicedoc_demo.py` you'll see a menu:

| Option | Mode | What it shows |
|--------|------|---------------|
| 1 | Automated test cases | 4 scenarios run automatically |
| 2 | Interactive input | Type your own symptoms |
| 3 | Batch testing | 5 cases with summary table |
| 4 | ML engine deep dive | Symptom extraction internals |
| 5 | Voice biomarker analysis | Stress / fatigue / mental health |
| 6 | Medical knowledge graph | SNOMED CT, ICD-11, differential diagnosis |
| 7 | Integrated analysis | All 7 features together |
| 8 | Run all demos | Everything in sequence |

**For the video demo → use option 3 then option 7.**

---

## Expected Output (Option 3)

```
Test Case                 Triage     Risk     Confidence
----------------------------------------------------------
Headache                  green      25.0     72%
Fever + Cough             yellow     49.3     65%
Severe Chest Pain         red        96.0     95%
Wound                     red        70.0     95%
Nausea + Vomiting         yellow     49.5     68%
```

---

## API Usage

### Basic triage

```python
from voicedoc_core import VoiceDocCore

voicedoc = VoiceDocCore(use_gemma=False)  # mock mode — no GPU needed

result = voicedoc.triage_with_function_calling(
    symptoms_text="High fever and cough for 3 days",
    duration_days=3,
    has_fever=True
)

print(result.triage_level)   # yellow
print(result.risk_score)     # 49.3
print(result.confidence)     # 0.65
```

### Voice biomarker analysis

```python
result = voicedoc.process_audio_with_biomarkers("patient_voice.wav")
print(result["mental_health_risk"])   # {"risk_level": "moderate", ...}
print(result["detected_conditions"])  # ["stress", "fatigue"]
```

### Clinical context (SNOMED CT)

```python
context = voicedoc.get_clinical_context(["fever", "cough"])
print(context["snomed_codes"])            # ["386661006", "49727002"]
print(context["icd11_codes"])             # ["BA01.0", "AB05.0"]
print(context["differential_diagnoses"])  # top 5 diagnoses with confidence
print(context["urgency_level"])           # yellow
```

### RAG-grounded recommendations

```python
from rag_engine import MedicalRAG

rag = MedicalRAG()
summary = rag.generate_rag_summary(
    ["fever", "cough"],
    {"triage_level": "yellow", "risk_score": 49}
)
for rec in summary["evidence_based_recommendations"]:
    print(f"• {rec['recommendation']}  [{rec['source']}]")
```

### Clinical audit trail

```python
from clinical_decision_support import ClinicalDecisionSupport

cds = ClinicalDecisionSupport()
report = cds.generate_cds_report(
    {"triage_level": "yellow", "risk_score": 49, "confidence": 0.65},
    {
        "patient_id": "P001",
        "symptoms": ["fever", "cough"],
        "fever": True,
        "fever_temperature": 39.2,
        "duration_days": 3
    }
)
print(report["audit_trail"])
```

---

## Triage Levels

| Level | Risk Score | Meaning |
|-------|-----------|---------|
| 🟢 Green | 0–40 | Low risk — home care sufficient |
| 🟡 Yellow | 40–70 | Moderate — see doctor within 24 h |
| 🔴 Red | 70–100 | Emergency — seek immediate care |

---

## Project Files

| File | Purpose |
|------|---------|
| `voicedoc_core.py` | Main system — Gemma 4 + all feature integrations |
| `ml_engine.py` | ML risk scoring (TF-IDF + cosine similarity) |
| `voice_biomarker_analyzer.py` | 22+ acoustic features, mental health signals |
| `medical_knowledge_graph.py` | SNOMED CT, ICD-11, differential diagnosis |
| `rag_engine.py` | Evidence retrieval, grounded recommendations |
| `model_optimization.py` | INT8 quantization, edge deployment |
| `fine_tuning.py` | LoRA / QLoRA fine-tuning |
| `clinical_decision_support.py` | CQL rules, audit trails |
| `voicedoc_demo.py` | Interactive demo (8 modes) |
| `VoiceDoc_Colab.ipynb` | Google Colab notebook |

---

## Troubleshooting

**`ModuleNotFoundError: sklearn`**
```bash
pip install scikit-learn
```

**`ModuleNotFoundError: librosa`** (voice biomarkers)
```bash
pip install librosa soundfile
```

**Gemma 4 not loading**
```python
voicedoc = VoiceDocCore(use_gemma=False)  # use mock mode
```

**CUDA out of memory**
- Use `use_gemma=False` for local testing
- Use Google Colab Pro for full Gemma 4

---

## Deployment

### Ollama — Raspberry Pi (fully offline)
```bash
curl https://ollama.ai/install.sh | sh
ollama pull gemma4:4b
python voicedoc_demo.py
```

### Google Colab
1. Open `VoiceDoc_Colab.ipynb`
2. Runtime → Change runtime type → T4 GPU
3. Run all cells

---

**GitHub:** https://github.com/Kotlasuhasreddy123/VoiceDoc-AI

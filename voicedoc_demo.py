"""
VoiceDoc AI - Interactive Demo
Run this to test the system end-to-end
"""

import json
import sys
import numpy as np
from voicedoc_core import VoiceDocCore


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_triage_result(result):
    """Pretty print triage result"""
    
    color_map = {
        'green': '🟢',
        'yellow': '🟡',
        'red': '🔴'
    }
    
    urgency_map = {
        'green': 'LOW URGENCY - Home care sufficient',
        'yellow': 'MODERATE URGENCY - See doctor within 24 hours',
        'red': 'HIGH URGENCY - Seek immediate medical attention'
    }
    
    print(f"\n{color_map.get(result.triage_level, '⚪')} TRIAGE LEVEL: {result.triage_level.upper()}")
    print(f"   {urgency_map[result.triage_level]}\n")
    
    print(f"Risk Score: {result.risk_score}/100")
    print(f"Confidence: {result.confidence*100:.0f}%\n")
    
    print(f"Primary Symptom: {result.primary_symptom}")
    print(f"Detected Symptoms: {', '.join(result.detected_symptoms)}\n")
    
    print("Home Care Instructions:")
    for i, instruction in enumerate(result.home_care_instructions, 1):
        print(f"  {i}. {instruction}")
    
    print(f"\nEscalation Guidance: {result.escalation_guidance}")
    print(f"\nReasoning: {result.reasoning}")


def demo_mode_1_text_input():
    """Demo 1: Text-based symptom input"""
    print_header("DEMO 1: Text-Based Symptom Input")
    
    voicedoc = VoiceDocCore(use_gemma=False)
    
    test_cases = [
        {
            'name': 'Mild Cold',
            'symptoms': 'I have a slight cough and sore throat',
            'duration': 1,
            'fever': False
        },
        {
            'name': 'Moderate Flu',
            'symptoms': 'High fever, persistent cough, and body ache for 3 days',
            'duration': 3,
            'fever': True
        },
        {
            'name': 'Severe Respiratory',
            'symptoms': 'Severe chest pain and shortness of breath',
            'duration': 1,
            'fever': False
        },
        {
            'name': 'Wound Injury',
            'symptoms': 'Deep cut on my hand with bleeding',
            'duration': 1,
            'fever': False
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test['name']} ---")
        print(f"Input: {test['symptoms']}")
        print(f"Duration: {test['duration']} day(s), Fever: {test['fever']}")
        
        result = voicedoc.triage_with_function_calling(
            symptoms_text=test['symptoms'],
            duration_days=test['duration'],
            has_fever=test['fever']
        )
        
        print_triage_result(result)
        print("\n" + "-"*70)


def demo_mode_2_interactive():
    """Demo 2: Interactive user input"""
    print_header("DEMO 2: Interactive Mode")
    
    voicedoc = VoiceDocCore(use_gemma=False)
    
    print("Welcome to VoiceDoc AI - Medical Triage System")
    print("(Type 'quit' to exit)\n")
    
    while True:
        print("\n" + "="*70)
        symptoms = input("Describe your symptoms: ").strip()
        
        if symptoms.lower() == 'quit':
            print("Thank you for using VoiceDoc AI. Stay healthy!")
            break
        
        if not symptoms:
            print("Please describe your symptoms.")
            continue
        
        # Get additional info
        try:
            duration = int(input("How many days have you had these symptoms? (default: 1): ") or "1")
        except ValueError:
            duration = 1
        
        fever_input = input("Do you have fever? (yes/no, default: no): ").lower()
        has_fever = fever_input in ['yes', 'y', 'true', '1']
        
        print("\nAnalyzing...")
        
        result = voicedoc.triage_with_function_calling(
            symptoms_text=symptoms,
            duration_days=duration,
            has_fever=has_fever
        )
        
        print_triage_result(result)


def demo_mode_3_batch_testing():
    """Demo 3: Batch testing with detailed output"""
    print_header("DEMO 3: Batch Testing with Detailed Output")
    
    voicedoc = VoiceDocCore(use_gemma=False)
    
    test_cases = [
        ('Headache', 'I have a mild headache', 1, False),
        ('Fever + Cough', 'High fever and cough for 2 days', 2, True),
        ('Severe Chest Pain', 'Severe chest pain and difficulty breathing', 1, False),
        ('Wound', 'Deep cut on my leg with bleeding', 1, False),
        ('Nausea + Vomiting', 'Nausea and vomiting for 4 hours', 1, False),
    ]
    
    results_summary = []
    
    for name, symptoms, duration, fever in test_cases:
        print(f"\nTesting: {name}")
        print(f"Symptoms: {symptoms}")
        
        result = voicedoc.triage_with_function_calling(
            symptoms_text=symptoms,
            duration_days=duration,
            has_fever=fever
        )
        
        results_summary.append({
            'test_case': name,
            'triage_level': result.triage_level,
            'risk_score': result.risk_score,
            'confidence': result.confidence
        })
        
        print(f"Result: {result.triage_level.upper()} (Risk: {result.risk_score}/100, Confidence: {result.confidence*100:.0f}%)")
    
    # Print summary table
    print_header("Test Summary")
    print(f"{'Test Case':<25} {'Triage':<10} {'Risk':<8} {'Confidence':<12}")
    print("-" * 55)
    for summary in results_summary:
        print(f"{summary['test_case']:<25} {summary['triage_level']:<10} {summary['risk_score']:<8.1f} {summary['confidence']*100:<11.0f}%")


def demo_mode_4_ml_engine_deep_dive():
    """Demo 4: Deep dive into ML engine"""
    print_header("DEMO 4: ML Engine Deep Dive")
    
    from ml_engine import MedicalTriageEngine
    
    engine = MedicalTriageEngine()
    
    print("Testing symptom extraction and risk scoring...\n")
    
    test_input = "I have high fever, severe cough, and chest pain for 3 days"
    print(f"Input: {test_input}\n")
    
    # Extract symptoms
    symptoms = engine.extract_symptoms(test_input)
    print("Extracted Symptoms (with similarity scores):")
    for symptom, score in symptoms[:5]:
        print(f"  • {symptom}: {score:.2f}")
    
    # Calculate risk
    print("\nRisk Calculation:")
    risk_analysis = engine.calculate_risk_score(symptoms, duration_days=3, has_fever=True)
    print(f"  Base Risk: {engine.symptom_database[symptoms[0][0]]['base_risk']}")
    print(f"  Duration Multiplier: 1.3x (3 days)")
    print(f"  Fever Multiplier: 1.3x")
    print(f"  Multiple Symptoms Multiplier: 1.1x")
    print(f"  Final Risk Score: {risk_analysis['risk_score']}/100")
    print(f"  Triage Level: {risk_analysis['triage_level'].upper()}")
    
    # Get recommendations
    print("\nRecommendations:")
    recommendations = engine.get_recommendations(risk_analysis['triage_level'], symptoms[0][0])
    print(f"  Urgency: {recommendations['urgency']}")
    print(f"  Escalation: {recommendations['escalation']}")
    print("  Home Care:")
    for care in recommendations['home_care']:
        print(f"    • {care}")


def demo_mode_5_voice_biomarkers():
    """Demo 5: Voice biomarker analysis"""
    print_header("DEMO 5: Voice Biomarker Analysis (NEW)")
    
    from voice_biomarker_analyzer import VoiceBiomarkerAnalyzer
    import numpy as np
    
    analyzer = VoiceBiomarkerAnalyzer()
    
    print("Voice Biomarker Analysis - Detecting health signals from voice\n")
    
    # Create sample audio data (simulating different voice conditions)
    sr = 16000
    duration = 1
    
    test_cases = [
        {
            'name': 'Normal Voice',
            'description': 'Healthy person speaking normally',
            'audio_data': np.random.randn(sr * duration) * 0.05
        },
        {
            'name': 'Stressed Voice',
            'description': 'Person under stress (higher pitch variance)',
            'audio_data': np.random.randn(sr * duration) * 0.15
        },
        {
            'name': 'Fatigued Voice',
            'description': 'Person with fatigue (lower energy)',
            'audio_data': np.random.randn(sr * duration) * 0.02
        }
    ]
    
    for test in test_cases:
        print(f"\n--- {test['name']} ---")
        print(f"Description: {test['description']}\n")
        
        # Extract features
        features = analyzer.extract_acoustic_features(test['audio_data'], sr)
        
        print("Key Acoustic Features:")
        print(f"  Pitch Mean: {features['pitch_mean']:.2f} Hz")
        print(f"  Pitch Variance: {features['pitch_variance']:.4f}")
        print(f"  Energy Mean: {features['energy_mean']:.4f}")
        print(f"  Speech Rate: {features['speech_rate']:.0f} words/min")
        print(f"  Jitter: {features['jitter']:.4f}")
        print(f"  Shimmer: {features['shimmer']:.4f}")
        
        # Detect health signals
        signals = analyzer.detect_health_signals(features)
        
        print("\nDetected Health Signals:")
        for signal_name, signal_data in signals.items():
            if isinstance(signal_data, dict) and 'detected' in signal_data:
                status = "✓ DETECTED" if signal_data['detected'] else "✗ Not detected"
                confidence = signal_data.get('confidence', 0)
                print(f"  {signal_name}: {status} (Confidence: {confidence:.0%})")
        
        # Mental health risk
        mental_health = signals.get('mental_health_risk', {})
        print(f"\nMental Health Risk: {mental_health.get('risk_level', 'unknown').upper()}")
        if mental_health.get('detected_conditions'):
            print(f"  Detected Conditions: {', '.join(mental_health['detected_conditions'])}")
        print(f"  Recommendation: {mental_health.get('recommendation', 'N/A')}")


def demo_mode_6_medical_knowledge_graph():
    """Demo 6: Medical knowledge graph"""
    print_header("DEMO 6: Medical Knowledge Graph (NEW)")
    
    from medical_knowledge_graph import MedicalKnowledgeGraph
    
    kg = MedicalKnowledgeGraph()
    
    print("Medical Knowledge Graph - SNOMED CT & ICD-11 Integration\n")
    
    test_cases = [
        {
            'name': 'Respiratory Infection',
            'symptoms': ['fever', 'cough', 'shortness_of_breath']
        },
        {
            'name': 'Gastrointestinal Issue',
            'symptoms': ['nausea', 'vomiting', 'diarrhea']
        },
        {
            'name': 'Neurological Concern',
            'symptoms': ['headache', 'dizziness', 'confusion']
        }
    ]
    
    for test in test_cases:
        print(f"\n--- {test['name']} ---")
        print(f"Symptoms: {', '.join(test['symptoms'])}\n")
        
        # Generate clinical summary
        summary = kg.generate_clinical_summary(test['symptoms'])
        
        print("Clinical Summary:")
        print(f"  Urgency Level: {summary['urgency_level'].upper()}")
        print(f"  SNOMED CT Codes: {', '.join(summary['snomed_codes'])}")
        print(f"  ICD-11 Codes: {', '.join(summary['icd11_codes'])}")
        
        # Differential diagnoses
        print("\nDifferential Diagnoses:")
        for dx in summary['differential_diagnoses'][:3]:
            print(f"  • {dx['diagnosis']}: {dx['confidence']:.0%} confidence")
        
        # Clinical guidelines
        if summary['clinical_guidelines']:
            print("\nApplicable Clinical Guidelines:")
            for guideline in summary['clinical_guidelines'][:3]:
                print(f"  • {guideline}")


def demo_mode_7_integrated_analysis():
    """Demo 7: Integrated analysis with all features"""
    print_header("DEMO 7: Integrated Analysis (NEW)")
    
    voicedoc = VoiceDocCore(use_gemma=False)
    
    print("Integrated Analysis - Combining all VoiceDoc AI features\n")
    
    # Test case
    symptoms_list = ['fever', 'cough', 'chest_pain']
    symptoms_text = "High fever, persistent cough, and chest pain for 3 days"
    
    print(f"Patient Symptoms: {symptoms_text}\n")
    
    # 1. Clinical context from knowledge graph
    print("1. CLINICAL CONTEXT (Medical Knowledge Graph)")
    print("-" * 50)
    clinical_context = voicedoc.get_clinical_context(symptoms_list)
    print(f"Urgency Level: {clinical_context['urgency_level'].upper()}")
    print(f"SNOMED CT Codes: {', '.join(clinical_context['snomed_codes'])}")
    print(f"ICD-11 Codes: {', '.join(clinical_context['icd11_codes'])}")
    print("\nTop Differential Diagnoses:")
    for dx in clinical_context['differential_diagnoses'][:3]:
        print(f"  • {dx['diagnosis']}: {dx['confidence']:.0%}")
    
    # 2. Triage decision
    print("\n2. TRIAGE DECISION (ML Engine + Function Calling)")
    print("-" * 50)
    result = voicedoc.triage_with_function_calling(
        symptoms_text=symptoms_text,
        duration_days=3,
        has_fever=True
    )
    print(f"Triage Level: {result.triage_level.upper()}")
    print(f"Risk Score: {result.risk_score}/100")
    print(f"Confidence: {result.confidence*100:.0f}%")
    print(f"Primary Symptom: {result.primary_symptom}")
    
    # 3. Recommendations
    print("\n3. RECOMMENDATIONS")
    print("-" * 50)
    print("Home Care Instructions:")
    for i, instruction in enumerate(result.home_care_instructions, 1):
        print(f"  {i}. {instruction}")
    print(f"\nEscalation Guidance: {result.escalation_guidance}")
    
    print("\n" + "="*70)
    print("This integrated analysis combines:")
    print("  ✓ Medical knowledge graph (SNOMED CT, ICD-11)")
    print("  ✓ ML-based risk scoring")
    print("  ✓ Gemma 4 function calling")
    print("  ✓ Clinical decision support")
    print("="*70)


def main():
    """Main demo runner"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  VoiceDoc AI - Medical Triage System Demo".center(68) + "║")
    print("║" + "  Powered by Gemma 4 | Offline-First | Multilingual".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\nSelect a demo mode:")
    print("  1. Text-based symptom input (automated test cases)")
    print("  2. Interactive mode (manual input)")
    print("  3. Batch testing with summary")
    print("  4. ML engine deep dive")
    print("  5. Voice biomarker analysis (NEW)")
    print("  6. Medical knowledge graph (NEW)")
    print("  7. Integrated analysis with all features (NEW)")
    print("  8. Run all demos")
    print("  0. Exit")
    
    choice = input("\nEnter your choice (0-8): ").strip()
    
    if choice == '1':
        demo_mode_1_text_input()
    elif choice == '2':
        demo_mode_2_interactive()
    elif choice == '3':
        demo_mode_3_batch_testing()
    elif choice == '4':
        demo_mode_4_ml_engine_deep_dive()
    elif choice == '5':
        demo_mode_5_voice_biomarkers()
    elif choice == '6':
        demo_mode_6_medical_knowledge_graph()
    elif choice == '7':
        demo_mode_7_integrated_analysis()
    elif choice == '8':
        demo_mode_1_text_input()
        demo_mode_3_batch_testing()
        demo_mode_4_ml_engine_deep_dive()
        demo_mode_5_voice_biomarkers()
        demo_mode_6_medical_knowledge_graph()
        demo_mode_7_integrated_analysis()
    elif choice == '0':
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Running demo 1...")
        demo_mode_1_text_input()
    
    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

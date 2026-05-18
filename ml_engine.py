"""
VoiceDoc AI - ML Risk Scoring Engine
Inspired by Project Axiom's TF-IDF + Cosine Similarity approach
Adapted for medical symptom triage
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple

class MedicalTriageEngine:
    """
    ML-powered medical triage system using symptom clustering and risk scoring.
    Similar architecture to Axiom's ML core, but for healthcare.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
        self.symptom_database = self._load_symptom_database()
        self.risk_thresholds = {
            'green': (0, 40),      # Low risk - home care
            'yellow': (40, 70),    # Medium risk - see doctor within 24h
            'red': (70, 100)       # High risk - emergency
        }
        self.fit_vectorizer()
    
    def _load_symptom_database(self) -> Dict:
        """Load symptom → triage mapping database"""
        return {
            # Respiratory
            'fever': {'base_risk': 35, 'category': 'respiratory', 'escalation': 'yellow'},
            'cough': {'base_risk': 30, 'category': 'respiratory', 'escalation': 'yellow'},
            'sore throat': {'base_risk': 25, 'category': 'respiratory', 'escalation': 'green'},
            'shortness of breath': {'base_risk': 75, 'category': 'respiratory', 'escalation': 'red'},
            'chest pain': {'base_risk': 80, 'category': 'respiratory', 'escalation': 'red'},
            
            # Gastrointestinal
            'nausea': {'base_risk': 30, 'category': 'gi', 'escalation': 'yellow'},
            'vomiting': {'base_risk': 45, 'category': 'gi', 'escalation': 'yellow'},
            'diarrhea': {'base_risk': 40, 'category': 'gi', 'escalation': 'yellow'},
            'abdominal pain': {'base_risk': 50, 'category': 'gi', 'escalation': 'yellow'},
            'severe abdominal pain': {'base_risk': 75, 'category': 'gi', 'escalation': 'red'},
            
            # Neurological
            'headache': {'base_risk': 25, 'category': 'neuro', 'escalation': 'green'},
            'severe headache': {'base_risk': 65, 'category': 'neuro', 'escalation': 'yellow'},
            'dizziness': {'base_risk': 40, 'category': 'neuro', 'escalation': 'yellow'},
            'confusion': {'base_risk': 70, 'category': 'neuro', 'escalation': 'red'},
            'loss of consciousness': {'base_risk': 95, 'category': 'neuro', 'escalation': 'red'},
            
            # Skin/Wound
            'rash': {'base_risk': 30, 'category': 'skin', 'escalation': 'yellow'},
            'wound': {'base_risk': 35, 'category': 'skin', 'escalation': 'yellow'},
            'deep wound': {'base_risk': 70, 'category': 'skin', 'escalation': 'red'},
            'burn': {'base_risk': 50, 'category': 'skin', 'escalation': 'yellow'},
            'severe burn': {'base_risk': 85, 'category': 'skin', 'escalation': 'red'},
            
            # General
            'fatigue': {'base_risk': 20, 'category': 'general', 'escalation': 'green'},
            'body ache': {'base_risk': 25, 'category': 'general', 'escalation': 'green'},
            'weakness': {'base_risk': 35, 'category': 'general', 'escalation': 'yellow'},
        }
    
    def fit_vectorizer(self):
        """Fit TF-IDF vectorizer on symptom database"""
        symptoms = list(self.symptom_database.keys())
        self.vectorizer.fit(symptoms)
        self.symptom_vectors = self.vectorizer.transform(symptoms)
    
    def extract_symptoms(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract symptoms from user input using cosine similarity.
        Similar to Axiom's evidence chain matching.
        """
        text_lower = text.lower()

        # Direct keyword override for critical/high-risk symptoms
        # This ensures severe symptoms are never missed by the vectorizer
        critical_keywords = {
            'chest pain': ['chest pain', 'chest ache', 'chest pressure', 'chest tightness'],
            'shortness of breath': ['shortness of breath', 'difficulty breathing',
                                    'hard to breathe', 'cant breathe', "can't breathe",
                                    'trouble breathing', 'breathing difficulty'],
            'loss of consciousness': ['unconscious', 'fainted', 'passed out', 'loss of consciousness'],
            'severe headache': ['severe headache', 'worst headache', 'thunderclap headache'],
            'severe abdominal pain': ['severe abdominal', 'severe stomach', 'severe belly'],
            'deep wound': ['deep cut', 'deep wound', 'deep laceration', 'deep gash'],
            'severe burn': ['severe burn', 'third degree', 'third-degree'],
            'confusion': ['confused', 'confusion', 'disoriented', 'not making sense'],
        }

        forced = []
        for symptom, keywords in critical_keywords.items():
            if any(kw in text_lower for kw in keywords):
                forced.append((symptom, 0.95))

        # Vectorizer-based matching for remaining symptoms
        text_vector = self.vectorizer.transform([text_lower])
        similarities = cosine_similarity(text_vector, self.symptom_vectors)[0]

        symptoms = list(self.symptom_database.keys())
        matched_symptoms = []

        forced_names = {s[0] for s in forced}
        for symptom, similarity in zip(symptoms, similarities):
            if symptom in forced_names:
                continue  # already captured via keyword override
            # Exclude "severe X" / "deep X" variants unless those words appear in input
            if symptom.startswith('severe ') and 'severe' not in text_lower:
                continue
            if symptom.startswith('deep ') and 'deep' not in text_lower:
                continue
            if similarity > 0.35:  # slightly tighter threshold
                matched_symptoms.append((symptom, float(similarity)))

        # Merge: forced symptoms first (highest priority), then vectorizer matches
        matched_symptoms = forced + sorted(matched_symptoms, key=lambda x: x[1], reverse=True)
        return matched_symptoms
    
    def calculate_risk_score(self, symptoms: List[Tuple[str, float]], 
                            duration_days: int = 1, 
                            has_fever: bool = False) -> Dict:
        """
        Calculate overall risk score (0-100) based on symptoms.
        Incorporates duration and fever as multipliers.
        """
        if not symptoms:
            return {
                'risk_score': 0,
                'triage_level': 'green',
                'confidence': 0.0,
                'reasoning': 'No symptoms detected'
            }
        
        # Base risk from primary symptom
        primary_symptom, primary_confidence = symptoms[0]
        base_risk = self.symptom_database[primary_symptom]['base_risk']
        
        # Adjust for duration (longer = higher risk)
        duration_multiplier = min(1.0 + (duration_days - 1) * 0.15, 1.5)
        
        # Adjust for fever (fever + other symptoms = higher risk)
        fever_multiplier = 1.3 if has_fever else 1.0
        
        # Adjust for multiple symptoms (more symptoms = higher risk)
        symptom_multiplier = min(1.0 + (len(symptoms) - 1) * 0.1, 1.4)
        
        # Calculate final risk score
        risk_score = base_risk * duration_multiplier * fever_multiplier * symptom_multiplier
        risk_score = min(risk_score, 100)  # Cap at 100
        
        # Determine triage level — use >= 70 for red so score of 100 is always red
        if risk_score >= 70:
            triage_level = 'red'
        elif risk_score >= 40:
            triage_level = 'yellow'
        else:
            triage_level = 'green'
        
        # Confidence based on primary symptom match
        confidence = primary_confidence
        
        return {
            'risk_score': round(risk_score, 1),
            'triage_level': triage_level,
            'confidence': round(confidence, 2),
            'primary_symptom': primary_symptom,
            'matched_symptoms': [s[0] for s in symptoms[:3]],
            'reasoning': self._generate_reasoning(
                primary_symptom, risk_score, duration_days, has_fever
            )
        }
    
    def _generate_reasoning(self, symptom: str, risk_score: float, 
                           duration_days: int, has_fever: bool) -> str:
        """Generate human-readable reasoning for the risk score"""
        reasons = [f"Primary symptom: {symptom}"]
        
        if duration_days > 3:
            reasons.append(f"Symptoms persisting for {duration_days} days (elevated risk)")
        
        if has_fever:
            reasons.append("Fever present (increases risk)")
        
        if risk_score >= 70:
            reasons.append("High-risk combination detected")
        elif risk_score >= 40:
            reasons.append("Moderate risk - medical attention recommended")
        else:
            reasons.append("Low risk - home care likely sufficient")
        
        return " | ".join(reasons)
    
    def get_recommendations(self, triage_level: str, symptom: str) -> Dict:
        """Get home care and escalation recommendations"""
        recommendations = {
            'green': {
                'home_care': [
                    'Rest and get adequate sleep',
                    'Stay hydrated - drink water regularly',
                    'Monitor symptoms for worsening',
                    'Use over-the-counter pain relief if needed'
                ],
                'escalation': 'Seek medical attention if symptoms worsen or persist beyond 1 week',
                'urgency': 'Non-urgent'
            },
            'yellow': {
                'home_care': [
                    'Rest and avoid strenuous activity',
                    'Stay hydrated',
                    'Monitor vital signs (temperature, breathing)',
                    'Take prescribed medications as directed'
                ],
                'escalation': 'Seek medical attention within 24 hours',
                'urgency': 'Urgent - same day or next day'
            },
            'red': {
                'home_care': [
                    'Do not delay - seek immediate medical attention',
                    'Call emergency services if available',
                    'Keep patient calm and comfortable',
                    'Monitor breathing and consciousness'
                ],
                'escalation': 'EMERGENCY - Seek immediate medical care',
                'urgency': 'CRITICAL - Call emergency services now'
            }
        }
        
        return recommendations.get(triage_level, recommendations['green'])
    
    def generate_triage_report(self, user_input: str, duration_days: int = 1, 
                              has_fever: bool = False, image_analysis: str = None) -> Dict:
        """
        Generate complete triage report.
        This is the main entry point for the system.
        """
        # Extract symptoms
        symptoms = self.extract_symptoms(user_input)
        
        # Calculate risk
        risk_analysis = self.calculate_risk_score(symptoms, duration_days, has_fever)
        
        # Get recommendations
        recommendations = self.get_recommendations(
            risk_analysis['triage_level'], 
            risk_analysis.get('primary_symptom', 'unknown')
        )
        
        # Compile report
        report = {
            'input_analysis': {
                'user_input': user_input,
                'duration_days': duration_days,
                'has_fever': has_fever,
                'image_analysis': image_analysis
            },
            'symptom_extraction': {
                'detected_symptoms': risk_analysis['matched_symptoms'],
                'confidence': risk_analysis['confidence']
            },
            'risk_assessment': {
                'risk_score': risk_analysis['risk_score'],
                'triage_level': risk_analysis['triage_level'],
                'confidence': risk_analysis['confidence'],
                'primary_symptom': risk_analysis.get('primary_symptom', 'unknown'),
                'reasoning': risk_analysis['reasoning']
            },
            'recommendations': recommendations,
            'next_steps': self._get_next_steps(risk_analysis['triage_level'])
        }
        
        return report
    
    def _get_next_steps(self, triage_level: str) -> List[str]:
        """Get specific next steps based on triage level"""
        steps = {
            'green': [
                '1. Follow home care instructions',
                '2. Monitor symptoms daily',
                '3. Seek medical help if symptoms worsen'
            ],
            'yellow': [
                '1. Schedule doctor appointment for today or tomorrow',
                '2. Follow home care instructions',
                '3. Keep emergency contact ready'
            ],
            'red': [
                '1. Call emergency services immediately',
                '2. Go to nearest hospital/clinic',
                '3. Bring this report with you'
            ]
        }
        return steps.get(triage_level, steps['green'])


# Example usage
if __name__ == '__main__':
    engine = MedicalTriageEngine()
    
    # Test case 1: Mild symptoms
    report1 = engine.generate_triage_report(
        "I have a headache and body ache",
        duration_days=1,
        has_fever=False
    )
    print("Test 1 - Mild Symptoms:")
    print(json.dumps(report1, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test case 2: Moderate symptoms
    report2 = engine.generate_triage_report(
        "High fever and persistent cough for 3 days",
        duration_days=3,
        has_fever=True
    )
    print("Test 2 - Moderate Symptoms:")
    print(json.dumps(report2, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test case 3: Severe symptoms
    report3 = engine.generate_triage_report(
        "Severe chest pain and shortness of breath",
        duration_days=1,
        has_fever=False
    )
    print("Test 3 - Severe Symptoms:")
    print(json.dumps(report3, indent=2))

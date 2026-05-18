"""
VoiceDoc AI - Medical Knowledge Graph
SNOMED CT-based medical knowledge representation
Research-based on: SNOMED CT Clinical Decision Support Guide, ICD-11 Mapping
"""

import json
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

@dataclass
class SNOMEDConcept:
    """SNOMED CT concept representation"""
    snomed_id: str
    term: str
    icd11_code: str
    parent_concepts: List[str]
    child_concepts: List[str]
    clinical_guidelines: List[str]
    severity_level: str  # mild, moderate, severe
    urgency: str  # green, yellow, red


class MedicalKnowledgeGraph:
    """
    SNOMED CT-based medical knowledge graph
    Enables clinical decision support with standardized medical terminology
    """
    
    def __init__(self):
        """Initialize medical knowledge graph"""
        self.concepts = {}
        self.relationships = {}
        self.guidelines = {}
        self._initialize_snomed_lite()
    
    def _initialize_snomed_lite(self):
        """Initialize lightweight SNOMED CT subset for common symptoms"""
        
        # Respiratory symptoms
        self.concepts['fever'] = SNOMEDConcept(
            snomed_id='386661006',
            term='Fever',
            icd11_code='BA01.0',
            parent_concepts=['abnormal_vital_sign'],
            child_concepts=['high_fever', 'low_grade_fever'],
            clinical_guidelines=['WHO_fever_management', 'CDC_fever_protocol'],
            severity_level='mild',
            urgency='yellow'
        )
        
        self.concepts['cough'] = SNOMEDConcept(
            snomed_id='49727002',
            term='Cough',
            icd11_code='AB05.0',
            parent_concepts=['respiratory_symptom'],
            child_concepts=['dry_cough', 'productive_cough', 'persistent_cough'],
            clinical_guidelines=['WHO_cough_management', 'respiratory_protocol'],
            severity_level='mild',
            urgency='yellow'
        )
        
        self.concepts['shortness_of_breath'] = SNOMEDConcept(
            snomed_id='25064002',
            term='Shortness of Breath',
            icd11_code='MG30.0',
            parent_concepts=['respiratory_symptom'],
            child_concepts=['mild_dyspnea', 'severe_dyspnea'],
            clinical_guidelines=['emergency_respiratory_protocol'],
            severity_level='severe',
            urgency='red'
        )
        
        self.concepts['chest_pain'] = SNOMEDConcept(
            snomed_id='29857009',
            term='Chest Pain',
            icd11_code='MG30.1',
            parent_concepts=['pain_symptom'],
            child_concepts=['cardiac_chest_pain', 'musculoskeletal_chest_pain'],
            clinical_guidelines=['emergency_cardiac_protocol', 'chest_pain_evaluation'],
            severity_level='severe',
            urgency='red'
        )
        
        # Gastrointestinal symptoms
        self.concepts['nausea'] = SNOMEDConcept(
            snomed_id='422587007',
            term='Nausea',
            icd11_code='DA90.0',
            parent_concepts=['gi_symptom'],
            child_concepts=['nausea_with_vomiting'],
            clinical_guidelines=['gi_symptom_management'],
            severity_level='mild',
            urgency='yellow'
        )
        
        self.concepts['vomiting'] = SNOMEDConcept(
            snomed_id='422400008',
            term='Vomiting',
            icd11_code='DA90.1',
            parent_concepts=['gi_symptom'],
            child_concepts=['projectile_vomiting', 'persistent_vomiting'],
            clinical_guidelines=['dehydration_protocol', 'gi_emergency_protocol'],
            severity_level='moderate',
            urgency='yellow'
        )
        
        self.concepts['diarrhea'] = SNOMEDConcept(
            snomed_id='62315008',
            term='Diarrhea',
            icd11_code='DA93.0',
            parent_concepts=['gi_symptom'],
            child_concepts=['acute_diarrhea', 'chronic_diarrhea', 'bloody_diarrhea'],
            clinical_guidelines=['dehydration_protocol', 'infectious_disease_protocol'],
            severity_level='moderate',
            urgency='yellow'
        )
        
        self.concepts['abdominal_pain'] = SNOMEDConcept(
            snomed_id='21522001',
            term='Abdominal Pain',
            icd11_code='DA89.0',
            parent_concepts=['pain_symptom'],
            child_concepts=['acute_abdomen', 'chronic_abdominal_pain'],
            clinical_guidelines=['acute_abdomen_protocol', 'surgical_emergency_protocol'],
            severity_level='moderate',
            urgency='yellow'
        )
        
        # Neurological symptoms
        self.concepts['headache'] = SNOMEDConcept(
            snomed_id='25064002',
            term='Headache',
            icd11_code='8A80.0',
            parent_concepts=['pain_symptom'],
            child_concepts=['migraine', 'tension_headache', 'cluster_headache'],
            clinical_guidelines=['headache_management', 'migraine_protocol'],
            severity_level='mild',
            urgency='green'
        )
        
        self.concepts['dizziness'] = SNOMEDConcept(
            snomed_id='404640003',
            term='Dizziness',
            icd11_code='8A81.0',
            parent_concepts=['neuro_symptom'],
            child_concepts=['vertigo', 'lightheadedness'],
            clinical_guidelines=['neuro_evaluation_protocol'],
            severity_level='moderate',
            urgency='yellow'
        )
        
        self.concepts['confusion'] = SNOMEDConcept(
            snomed_id='40917007',
            term='Confusion',
            icd11_code='8A80.1',
            parent_concepts=['neuro_symptom'],
            child_concepts=['acute_confusion', 'delirium'],
            clinical_guidelines=['emergency_neuro_protocol', 'mental_status_evaluation'],
            severity_level='severe',
            urgency='red'
        )
        
        # Skin/Wound symptoms
        self.concepts['wound'] = SNOMEDConcept(
            snomed_id='417746004',
            term='Wound',
            icd11_code='NA85.0',
            parent_concepts=['skin_condition'],
            child_concepts=['laceration', 'puncture_wound', 'abrasion'],
            clinical_guidelines=['wound_care_protocol', 'infection_prevention'],
            severity_level='moderate',
            urgency='yellow'
        )
        
        self.concepts['rash'] = SNOMEDConcept(
            snomed_id='271807003',
            term='Rash',
            icd11_code='EA90.0',
            parent_concepts=['skin_condition'],
            child_concepts=['urticaria', 'dermatitis', 'infectious_rash'],
            clinical_guidelines=['dermatology_protocol', 'allergy_protocol'],
            severity_level='mild',
            urgency='yellow'
        )
        
        self.concepts['burn'] = SNOMEDConcept(
            snomed_id='125670008',
            term='Burn',
            icd11_code='NA85.1',
            parent_concepts=['skin_condition'],
            child_concepts=['first_degree_burn', 'second_degree_burn', 'third_degree_burn'],
            clinical_guidelines=['burn_care_protocol', 'emergency_burn_protocol'],
            severity_level='severe',
            urgency='red'
        )
        
        # General symptoms
        self.concepts['fatigue'] = SNOMEDConcept(
            snomed_id='84229001',
            term='Fatigue',
            icd11_code='QE84.0',
            parent_concepts=['general_symptom'],
            child_concepts=['chronic_fatigue'],
            clinical_guidelines=['fatigue_evaluation_protocol'],
            severity_level='mild',
            urgency='green'
        )
        
        self.concepts['body_ache'] = SNOMEDConcept(
            snomed_id='68962001',
            term='Body Ache',
            icd11_code='MG30.0',
            parent_concepts=['pain_symptom'],
            child_concepts=['myalgia', 'arthralgia'],
            clinical_guidelines=['pain_management_protocol'],
            severity_level='mild',
            urgency='green'
        )
        
        self.concepts['weakness'] = SNOMEDConcept(
            snomed_id='13791008',
            term='Weakness',
            icd11_code='MG30.1',
            parent_concepts=['general_symptom'],
            child_concepts=['generalized_weakness', 'localized_weakness'],
            clinical_guidelines=['weakness_evaluation_protocol'],
            severity_level='moderate',
            urgency='yellow'
        )
    
    def get_concept(self, term: str) -> SNOMEDConcept:
        """Get SNOMED concept by term"""
        return self.concepts.get(term.lower().replace(' ', '_'))
    
    def get_symptom_hierarchy(self, symptom: str) -> Dict:
        """
        Get symptom hierarchy (parent and child concepts)
        
        Args:
            symptom: Symptom term
        
        Returns:
            Dictionary with parent and child concepts
        """
        concept = self.get_concept(symptom)
        if not concept:
            return {'error': f'Symptom "{symptom}" not found in knowledge graph'}
        
        return {
            'term': concept.term,
            'snomed_id': concept.snomed_id,
            'icd11_code': concept.icd11_code,
            'parent_concepts': concept.parent_concepts,
            'child_concepts': concept.child_concepts,
            'severity': concept.severity_level,
            'urgency': concept.urgency
        }
    
    def get_differential_diagnosis(self, symptoms: List[str]) -> List[Dict]:
        """
        Get differential diagnoses based on symptoms
        Uses SNOMED CT relationships for more accurate matching
        
        Args:
            symptoms: List of symptom terms
        
        Returns:
            List of potential diagnoses with confidence scores
        """
        diagnoses = []
        
        # Map symptoms to conditions
        symptom_condition_map = {
            'fever': ['influenza', 'common_cold', 'covid_19', 'malaria', 'typhoid'],
            'cough': ['bronchitis', 'pneumonia', 'asthma', 'tuberculosis'],
            'shortness_of_breath': ['pneumonia', 'asthma', 'heart_failure', 'pulmonary_embolism'],
            'chest_pain': ['myocardial_infarction', 'angina', 'pneumonia', 'musculoskeletal_pain'],
            'nausea': ['gastroenteritis', 'food_poisoning', 'migraine', 'pregnancy'],
            'vomiting': ['gastroenteritis', 'food_poisoning', 'appendicitis'],
            'diarrhea': ['gastroenteritis', 'food_poisoning', 'inflammatory_bowel_disease'],
            'abdominal_pain': ['appendicitis', 'gastroenteritis', 'kidney_stones', 'pancreatitis'],
            'headache': ['migraine', 'tension_headache', 'meningitis', 'sinusitis'],
            'dizziness': ['vertigo', 'anemia', 'hypotension', 'inner_ear_infection'],
            'confusion': ['delirium', 'dementia', 'stroke', 'infection'],
            'wound': ['infection_risk', 'tetanus_risk', 'bleeding_risk'],
            'rash': ['allergic_reaction', 'dermatitis', 'measles', 'chickenpox'],
            'burn': ['thermal_injury', 'infection_risk', 'shock_risk'],
        }
        
        # Collect all potential diagnoses
        potential_diagnoses = set()
        for symptom in symptoms:
            symptom_key = symptom.lower().replace(' ', '_')
            if symptom_key in symptom_condition_map:
                potential_diagnoses.update(symptom_condition_map[symptom_key])
        
        # Score diagnoses based on symptom match
        for diagnosis in potential_diagnoses:
            matching_symptoms = 0
            for symptom in symptoms:
                symptom_key = symptom.lower().replace(' ', '_')
                if symptom_key in symptom_condition_map:
                    if diagnosis in symptom_condition_map[symptom_key]:
                        matching_symptoms += 1
            
            confidence = matching_symptoms / len(symptoms) if symptoms else 0
            diagnoses.append({
                'diagnosis': diagnosis,
                'confidence': confidence,
                'matching_symptoms': matching_symptoms,
                'total_symptoms': len(symptoms)
            })
        
        # Sort by confidence
        diagnoses.sort(key=lambda x: x['confidence'], reverse=True)
        return diagnoses[:5]  # Return top 5
    
    def get_clinical_guidelines(self, condition: str) -> List[str]:
        """
        Get evidence-based clinical guidelines for a condition
        
        Args:
            condition: Condition term
        
        Returns:
            List of applicable clinical guidelines
        """
        concept = self.get_concept(condition)
        if concept:
            return concept.clinical_guidelines
        return []
    
    def get_urgency_level(self, symptom: str) -> str:
        """
        Get urgency level for a symptom
        
        Args:
            symptom: Symptom term
        
        Returns:
            Urgency level (green, yellow, red)
        """
        concept = self.get_concept(symptom)
        if concept:
            return concept.urgency
        return 'yellow'  # Default to moderate urgency
    
    def get_severity_level(self, symptom: str) -> str:
        """
        Get severity level for a symptom
        
        Args:
            symptom: Symptom term
        
        Returns:
            Severity level (mild, moderate, severe)
        """
        concept = self.get_concept(symptom)
        if concept:
            return concept.severity_level
        return 'mild'  # Default to mild
    
    def get_icd11_code(self, symptom: str) -> str:
        """
        Get ICD-11 code for a symptom
        
        Args:
            symptom: Symptom term
        
        Returns:
            ICD-11 code
        """
        concept = self.get_concept(symptom)
        if concept:
            return concept.icd11_code
        return 'Unknown'
    
    def get_snomed_id(self, symptom: str) -> str:
        """
        Get SNOMED CT ID for a symptom
        
        Args:
            symptom: Symptom term
        
        Returns:
            SNOMED CT ID
        """
        concept = self.get_concept(symptom)
        if concept:
            return concept.snomed_id
        return 'Unknown'
    
    def generate_clinical_summary(self, symptoms: List[str]) -> Dict:
        """
        Generate clinical summary with SNOMED CT and ICD-11 codes
        
        Args:
            symptoms: List of symptom terms
        
        Returns:
            Clinical summary with standardized codes
        """
        summary = {
            'symptoms': [],
            'differential_diagnoses': [],
            'clinical_guidelines': [],
            'snomed_codes': [],
            'icd11_codes': [],
            'urgency_level': 'green'
        }
        
        max_urgency = 'green'
        urgency_order = {'green': 0, 'yellow': 1, 'red': 2}
        
        for symptom in symptoms:
            concept = self.get_concept(symptom)
            if concept:
                summary['symptoms'].append({
                    'term': concept.term,
                    'snomed_id': concept.snomed_id,
                    'icd11_code': concept.icd11_code,
                    'severity': concept.severity_level,
                    'urgency': concept.urgency
                })
                
                summary['snomed_codes'].append(concept.snomed_id)
                summary['icd11_codes'].append(concept.icd11_code)
                summary['clinical_guidelines'].extend(concept.clinical_guidelines)
                
                # Update max urgency
                if urgency_order.get(concept.urgency, 0) > urgency_order.get(max_urgency, 0):
                    max_urgency = concept.urgency
        
        summary['urgency_level'] = max_urgency
        summary['differential_diagnoses'] = self.get_differential_diagnosis(symptoms)
        summary['clinical_guidelines'] = list(set(summary['clinical_guidelines']))
        
        return summary


# Example usage
if __name__ == '__main__':
    kg = MedicalKnowledgeGraph()
    
    # Test symptom hierarchy
    print("Symptom Hierarchy for 'fever':")
    print(kg.get_symptom_hierarchy('fever'))
    print()
    
    # Test differential diagnosis
    print("Differential Diagnosis for ['fever', 'cough']:")
    diagnoses = kg.get_differential_diagnosis(['fever', 'cough'])
    for dx in diagnoses:
        print(f"  {dx['diagnosis']}: {dx['confidence']:.2%}")
    print()
    
    # Test clinical guidelines
    print("Clinical Guidelines for 'fever':")
    guidelines = kg.get_clinical_guidelines('fever')
    for guideline in guidelines:
        print(f"  - {guideline}")
    print()
    
    # Test clinical summary
    print("Clinical Summary for ['fever', 'cough', 'chest_pain']:")
    summary = kg.generate_clinical_summary(['fever', 'cough', 'chest_pain'])
    print(json.dumps(summary, indent=2))

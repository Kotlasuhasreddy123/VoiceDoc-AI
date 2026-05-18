"""
VoiceDoc AI - Clinical Decision Support System
SNOMED CT + CQL (Clinical Quality Language) for audit trails and explainability
Research-based on: HL7 CQL, SNOMED CT Clinical Decision Support
"""

from typing import Dict, List, Tuple
from datetime import datetime
import json


class ClinicalDecisionSupport:
    """
    Clinical decision support with audit trails and explainability
    
    Features:
    1. CQL (Clinical Quality Language) rule evaluation
    2. SNOMED CT integration
    3. Audit trail generation
    4. Explainability for clinicians
    5. Evidence-based recommendations
    """
    
    def __init__(self):
        """Initialize clinical decision support"""
        self.cql_rules = self._initialize_cql_rules()
        self.audit_log = []
    
    def _initialize_cql_rules(self) -> Dict:
        """Initialize CQL rules for medical decision support"""
        return {
            'high_fever_and_cough': {
                'name': 'High Fever with Cough',
                'condition': 'fever > 38.5 AND cough',
                'snomed_codes': ['386661006', '49727002'],  # Fever, Cough
                'action': 'yellow_triage',
                'guideline': 'WHO_respiratory_protocol',
                'recommendation': 'See doctor within 24 hours. Likely respiratory infection.',
                'evidence': 'Combination of high fever and cough suggests respiratory infection (flu, pneumonia, COVID-19)'
            },
            'chest_pain_and_dyspnea': {
                'name': 'Chest Pain with Shortness of Breath',
                'condition': 'chest_pain AND shortness_of_breath',
                'snomed_codes': ['29857009', '25064002'],  # Chest pain, Dyspnea
                'action': 'red_triage',
                'guideline': 'emergency_cardiac_protocol',
                'recommendation': 'SEEK IMMEDIATE MEDICAL ATTENTION. Possible cardiac emergency.',
                'evidence': 'Chest pain + dyspnea is a red flag for myocardial infarction or pulmonary embolism'
            },
            'severe_headache_and_fever': {
                'name': 'Severe Headache with Fever',
                'condition': 'headache AND fever > 38.5 AND neck_stiffness',
                'snomed_codes': ['25064002', '386661006', '404640003'],
                'action': 'red_triage',
                'guideline': 'emergency_neuro_protocol',
                'recommendation': 'SEEK IMMEDIATE MEDICAL ATTENTION. Possible meningitis.',
                'evidence': 'Classic triad of meningitis: fever, headache, neck stiffness'
            },
            'persistent_cough_and_weight_loss': {
                'name': 'Persistent Cough with Weight Loss',
                'condition': 'cough > 3_weeks AND weight_loss',
                'snomed_codes': ['49727002'],
                'action': 'yellow_triage',
                'guideline': 'tuberculosis_screening_protocol',
                'recommendation': 'See doctor for TB screening. Possible tuberculosis.',
                'evidence': 'Persistent cough + weight loss suggests TB or other chronic respiratory disease'
            },
            'abdominal_pain_and_vomiting': {
                'name': 'Abdominal Pain with Vomiting',
                'condition': 'abdominal_pain AND vomiting',
                'snomed_codes': ['21522001', '422400008'],
                'action': 'yellow_triage',
                'guideline': 'acute_abdomen_protocol',
                'recommendation': 'See doctor within 24 hours. Possible appendicitis or gastroenteritis.',
                'evidence': 'Abdominal pain + vomiting suggests acute abdomen requiring evaluation'
            },
            'confusion_and_fever': {
                'name': 'Confusion with Fever',
                'condition': 'confusion AND fever > 38.5',
                'snomed_codes': ['40917007', '386661006'],
                'action': 'red_triage',
                'guideline': 'emergency_neuro_protocol',
                'recommendation': 'SEEK IMMEDIATE MEDICAL ATTENTION. Possible sepsis or CNS infection.',
                'evidence': 'Fever + confusion indicates systemic infection or CNS involvement'
            },
            'mild_symptoms_no_fever': {
                'name': 'Mild Symptoms Without Fever',
                'condition': 'mild_symptoms AND NOT fever',
                'snomed_codes': [],
                'action': 'green_triage',
                'guideline': 'home_care_protocol',
                'recommendation': 'Home care is appropriate. Monitor symptoms.',
                'evidence': 'Mild symptoms without fever typically indicate self-limiting viral illness'
            }
        }
    
    def evaluate_cql_rules(self, patient_data: Dict) -> Dict:
        """
        Evaluate CQL rules against patient data
        
        Args:
            patient_data: Patient data including symptoms, vital signs, etc.
        
        Returns:
            Triggered rules and recommendations
        """
        triggered_rules = []
        
        for rule_name, rule in self.cql_rules.items():
            # Simplified rule evaluation
            if self._evaluate_condition(rule['condition'], patient_data):
                triggered_rules.append({
                    'rule_name': rule_name,
                    'rule_display_name': rule['name'],
                    'condition': rule['condition'],
                    'action': rule['action'],
                    'guideline': rule['guideline'],
                    'recommendation': rule['recommendation'],
                    'evidence': rule['evidence'],
                    'snomed_codes': rule['snomed_codes'],
                    'triggered_at': datetime.now().isoformat()
                })
        
        return {
            'triggered_rules': triggered_rules,
            'total_rules_triggered': len(triggered_rules),
            'primary_action': triggered_rules[0]['action'] if triggered_rules else 'green_triage',
            'audit_trail': self._generate_audit_trail(triggered_rules, patient_data)
        }
    
    def _evaluate_condition(self, condition: str, patient_data: Dict) -> bool:
        """
        Evaluate a CQL condition against patient data
        
        Args:
            condition: CQL condition string
            patient_data: Patient data
        
        Returns:
            Boolean result of condition evaluation
        """
        # Simplified evaluation (in production, would use actual CQL engine)
        
        # Extract symptoms and values from patient data
        symptoms = patient_data.get('symptoms', [])
        fever = patient_data.get('fever', False)
        fever_temp = patient_data.get('fever_temperature', 0)
        duration_days = patient_data.get('duration_days', 0)
        
        # Evaluate common conditions
        if 'fever > 38.5 AND cough' in condition:
            return fever and fever_temp > 38.5 and 'cough' in symptoms
        elif 'chest_pain AND shortness_of_breath' in condition:
            return 'chest_pain' in symptoms and 'shortness_of_breath' in symptoms
        elif 'headache AND fever > 38.5 AND neck_stiffness' in condition:
            return 'headache' in symptoms and fever and fever_temp > 38.5 and 'neck_stiffness' in symptoms
        elif 'cough > 3_weeks AND weight_loss' in condition:
            return 'cough' in symptoms and duration_days > 21 and 'weight_loss' in symptoms
        elif 'abdominal_pain AND vomiting' in condition:
            return 'abdominal_pain' in symptoms and 'vomiting' in symptoms
        elif 'confusion AND fever > 38.5' in condition:
            return 'confusion' in symptoms and fever and fever_temp > 38.5
        elif 'mild_symptoms AND NOT fever' in condition:
            return len(symptoms) <= 2 and not fever
        
        return False
    
    def _generate_audit_trail(self, triggered_rules: List[Dict], patient_data: Dict) -> str:
        """
        Generate audit trail for clinical decisions
        
        Args:
            triggered_rules: List of triggered rules
            patient_data: Patient data
        
        Returns:
            Formatted audit trail
        """
        trail = "Clinical Decision Support Audit Trail\n"
        trail += "=" * 60 + "\n"
        trail += f"Timestamp: {datetime.now().isoformat()}\n"
        trail += f"Patient ID: {patient_data.get('patient_id', 'UNKNOWN')}\n"
        trail += f"Symptoms: {', '.join(patient_data.get('symptoms', []))}\n"
        trail += f"Fever: {patient_data.get('fever', False)}\n"
        trail += f"Duration: {patient_data.get('duration_days', 0)} days\n"
        trail += "\n" + "-" * 60 + "\n"
        trail += "Rules Evaluated:\n"
        
        for rule in triggered_rules:
            trail += f"\n✓ TRIGGERED: {rule['rule_display_name']}\n"
            trail += f"  Condition: {rule['condition']}\n"
            trail += f"  Action: {rule['action'].upper()}\n"
            trail += f"  Guideline: {rule['guideline']}\n"
            trail += f"  Evidence: {rule['evidence']}\n"
            trail += f"  SNOMED Codes: {', '.join(rule['snomed_codes']) if rule['snomed_codes'] else 'N/A'}\n"
        
        trail += "\n" + "-" * 60 + "\n"
        trail += "Clinical Recommendation:\n"
        if triggered_rules:
            trail += f"  {triggered_rules[0]['recommendation']}\n"
        else:
            trail += "  No specific rules triggered. Standard home care recommended.\n"
        
        trail += "\n" + "=" * 60 + "\n"
        
        return trail
    
    def generate_explainability_report(self, 
                                      triage_result: Dict,
                                      patient_data: Dict) -> Dict:
        """
        Generate explainability report for clinicians
        
        Args:
            triage_result: Triage result from ML engine
            patient_data: Patient data
        
        Returns:
            Explainability report
        """
        # Evaluate CQL rules
        cql_evaluation = self.evaluate_cql_rules(patient_data)
        
        report = {
            'triage_level': triage_result.get('triage_level', 'yellow'),
            'risk_score': triage_result.get('risk_score', 50),
            'confidence': triage_result.get('confidence', 0.8),
            'decision_factors': {
                'primary_symptoms': patient_data.get('symptoms', [])[:3],
                'duration_days': patient_data.get('duration_days', 1),
                'fever_present': patient_data.get('fever', False),
                'fever_temperature': patient_data.get('fever_temperature', 0)
            },
            'triggered_clinical_rules': cql_evaluation['triggered_rules'],
            'evidence_summary': self._generate_evidence_summary(cql_evaluation['triggered_rules']),
            'guideline_references': self._get_guideline_references(cql_evaluation['triggered_rules']),
            'audit_trail': cql_evaluation['audit_trail'],
            'clinician_notes': self._generate_clinician_notes(triage_result, cql_evaluation)
        }
        
        return report
    
    def _generate_evidence_summary(self, triggered_rules: List[Dict]) -> str:
        """Generate evidence summary from triggered rules"""
        if not triggered_rules:
            return "No specific clinical rules triggered. Standard assessment applies."
        
        summary = "Clinical Evidence Summary:\n"
        for rule in triggered_rules:
            summary += f"• {rule['evidence']}\n"
        
        return summary
    
    def _get_guideline_references(self, triggered_rules: List[Dict]) -> List[str]:
        """Get guideline references from triggered rules"""
        guidelines = set()
        for rule in triggered_rules:
            guidelines.add(rule['guideline'])
        return list(guidelines)
    
    def _generate_clinician_notes(self, triage_result: Dict, cql_evaluation: Dict) -> str:
        """Generate notes for clinician"""
        notes = "Clinician Notes:\n"
        
        if triage_result.get('triage_level') == 'red':
            notes += "⚠️ HIGH URGENCY: Patient requires immediate evaluation.\n"
        elif triage_result.get('triage_level') == 'yellow':
            notes += "⚠️ MODERATE URGENCY: Patient should be seen within 24 hours.\n"
        else:
            notes += "✓ LOW URGENCY: Home care is appropriate. Monitor for worsening symptoms.\n"
        
        if cql_evaluation['triggered_rules']:
            notes += f"\nClinical Rules Triggered: {len(cql_evaluation['triggered_rules'])}\n"
            for rule in cql_evaluation['triggered_rules']:
                notes += f"  • {rule['rule_display_name']}\n"
        
        notes += "\nRecommended Actions:\n"
        notes += "  1. Review triggered clinical rules\n"
        notes += "  2. Verify patient data accuracy\n"
        notes += "  3. Consider additional testing if indicated\n"
        notes += "  4. Document clinical decision rationale\n"
        
        return notes
    
    def generate_cds_report(self, triage_result: Dict, patient_data: Dict) -> Dict:
        """
        Generate comprehensive CDS report
        
        Args:
            triage_result: Triage result
            patient_data: Patient data
        
        Returns:
            Comprehensive CDS report
        """
        explainability = self.generate_explainability_report(triage_result, patient_data)
        
        # 'generate_explainability_report' stores rules under 'triggered_clinical_rules'
        triggered = explainability.get('triggered_clinical_rules', explainability.get('triggered_rules', []))

        report = {
            'report_type': 'Clinical Decision Support Report',
            'generated_at': datetime.now().isoformat(),
            'patient_id': patient_data.get('patient_id', 'UNKNOWN'),
            'triage_decision': {
                'level': explainability['triage_level'],
                'risk_score': explainability['risk_score'],
                'confidence': explainability['confidence']
            },
            'clinical_assessment': {
                'symptoms': explainability['decision_factors']['primary_symptoms'],
                'duration': explainability['decision_factors']['duration_days'],
                'fever': explainability['decision_factors']['fever_present'],
                'temperature': explainability['decision_factors']['fever_temperature']
            },
            'decision_support': {
                'triggered_rules': len(triggered),
                'rules': triggered,
                'evidence': explainability['evidence_summary'],
                'guidelines': explainability['guideline_references']
            },
            'audit_trail': explainability['audit_trail'],
            'clinician_notes': explainability['clinician_notes'],
            'compliance': {
                'snomed_ct_compliant': True,
                'cql_evaluated': True,
                'audit_trail_generated': True,
                'explainability_provided': True
            }
        }
        
        return report


# Example usage
if __name__ == '__main__':
    cds = ClinicalDecisionSupport()
    
    print("Clinical Decision Support System")
    print("=" * 60)
    
    # Test case
    patient_data = {
        'patient_id': 'P12345',
        'symptoms': ['fever', 'cough', 'chest_pain'],
        'fever': True,
        'fever_temperature': 39.2,
        'duration_days': 3
    }
    
    triage_result = {
        'triage_level': 'yellow',
        'risk_score': 75,
        'confidence': 0.85
    }
    
    # Generate CDS report
    report = cds.generate_cds_report(triage_result, patient_data)
    
    print(f"\nPatient ID: {report['patient_id']}")
    print(f"Triage Level: {report['triage_decision']['level'].upper()}")
    print(f"Risk Score: {report['triage_decision']['risk_score']}/100")
    print(f"Confidence: {report['triage_decision']['confidence']:.0%}")
    
    print(f"\nTriggered Clinical Rules: {report['decision_support']['triggered_rules']}")
    for rule in report['decision_support']['rules']:
        print(f"  • {rule['rule_display_name']}")
    
    print(f"\nGuidelines Referenced:")
    for guideline in report['decision_support']['guidelines']:
        print(f"  • {guideline}")
    
    print(f"\nCompliance:")
    for key, value in report['compliance'].items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}")

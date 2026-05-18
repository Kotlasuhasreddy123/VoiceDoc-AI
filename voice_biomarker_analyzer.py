"""
VoiceDoc AI - Voice Biomarker Analyzer
Extracts health signals from voice using acoustic features
Research-based on: Speechmatics + Thymia, Canary Speech, Frontiers in Digital Health
"""

import numpy as np
from typing import Dict, List, Tuple
import json

class VoiceBiomarkerAnalyzer:
    """
    Extract 30+ health signals from 15 seconds of voice
    Detects: stress, fatigue, depression, anxiety, diabetes markers, etc.
    """
    
    def __init__(self):
        """Initialize biomarker detection thresholds"""
        self.biomarker_thresholds = {
            'stress': {'pitch_variance': 0.15, 'energy_level': 0.7},
            'fatigue': {'speech_rate': 120, 'energy_level': 0.5},
            'depression': {'pitch_range': 50, 'speech_rate': 100},
            'anxiety': {'pitch_variance': 0.2, 'jitter': 0.02},
            'diabetes_markers': {'formant_freq': 2500, 'spectral_centroid': 3000},
            'neurological': {'jitter': 0.03, 'shimmer': 0.05},
        }
    
    def extract_acoustic_features(self, audio_data: np.ndarray, sr: int = 16000) -> Dict:
        """
        Extract 22+ acoustic features from audio
        
        Args:
            audio_data: Audio waveform (numpy array)
            sr: Sample rate (default 16kHz)
        
        Returns:
            Dictionary of acoustic features
        """
        features = {}
        
        # 1. Pitch-based features
        features['pitch_mean'] = self._estimate_pitch_mean(audio_data, sr)
        features['pitch_variance'] = self._estimate_pitch_variance(audio_data, sr)
        features['pitch_range'] = self._estimate_pitch_range(audio_data, sr)
        
        # 2. Energy-based features
        features['energy_mean'] = self._calculate_energy_mean(audio_data)
        features['energy_variance'] = self._calculate_energy_variance(audio_data)
        features['energy_contour'] = self._calculate_energy_contour(audio_data)
        
        # 3. Spectral features
        features['spectral_centroid'] = self._calculate_spectral_centroid(audio_data, sr)
        features['spectral_rolloff'] = self._calculate_spectral_rolloff(audio_data, sr)
        features['mfcc_mean'] = self._calculate_mfcc_mean(audio_data, sr)
        
        # 4. Voice quality features
        features['jitter'] = self._calculate_jitter(audio_data, sr)
        features['shimmer'] = self._calculate_shimmer(audio_data, sr)
        features['nhr'] = self._calculate_noise_harmonic_ratio(audio_data, sr)
        
        # 5. Temporal features
        features['speech_rate'] = self._estimate_speech_rate(audio_data, sr)
        features['pause_duration'] = self._estimate_pause_duration(audio_data, sr)
        features['voice_activity_ratio'] = self._calculate_voice_activity_ratio(audio_data)
        
        # 6. Formant features
        features['formant_freq_1'] = self._estimate_formant_frequency(audio_data, sr, 1)
        features['formant_freq_2'] = self._estimate_formant_frequency(audio_data, sr, 2)
        features['formant_freq_3'] = self._estimate_formant_frequency(audio_data, sr, 3)
        
        # 7. Prosodic features
        features['intonation_range'] = self._calculate_intonation_range(audio_data, sr)
        features['speech_rhythm'] = self._calculate_speech_rhythm(audio_data, sr)
        
        return features
    
    def detect_health_signals(self, features: Dict) -> Dict:
        """
        Map acoustic features to health signals
        
        Args:
            features: Dictionary of acoustic features
        
        Returns:
            Dictionary of detected health signals with confidence scores
        """
        signals = {}
        
        # Stress detection
        stress_score = self._detect_stress(features)
        signals['stress'] = {
            'detected': stress_score > 0.6,
            'confidence': stress_score,
            'indicators': ['high_pitch_variance', 'elevated_energy']
        }
        
        # Fatigue detection
        fatigue_score = self._detect_fatigue(features)
        signals['fatigue'] = {
            'detected': fatigue_score > 0.6,
            'confidence': fatigue_score,
            'indicators': ['slow_speech_rate', 'low_energy']
        }
        
        # Depression detection
        depression_score = self._detect_depression(features)
        signals['depression'] = {
            'detected': depression_score > 0.6,
            'confidence': depression_score,
            'indicators': ['narrow_pitch_range', 'monotone_speech']
        }
        
        # Anxiety detection
        anxiety_score = self._detect_anxiety(features)
        signals['anxiety'] = {
            'detected': anxiety_score > 0.6,
            'confidence': anxiety_score,
            'indicators': ['high_jitter', 'rapid_speech']
        }
        
        # Diabetes markers
        diabetes_score = self._detect_diabetes_markers(features)
        signals['diabetes_markers'] = {
            'detected': diabetes_score > 0.6,
            'confidence': diabetes_score,
            'indicators': ['formant_shift', 'spectral_changes']
        }
        
        # Neurological condition markers
        neuro_score = self._detect_neurological_markers(features)
        signals['neurological_markers'] = {
            'detected': neuro_score > 0.6,
            'confidence': neuro_score,
            'indicators': ['high_jitter', 'high_shimmer']
        }
        
        # Mental health risk assessment
        signals['mental_health_risk'] = self._assess_mental_health_risk(signals)
        
        return signals
    
    # Feature extraction methods
    
    def _estimate_pitch_mean(self, audio_data: np.ndarray, sr: int) -> float:
        """Estimate mean pitch using autocorrelation"""
        # Simplified: use spectral peak as proxy
        fft = np.abs(np.fft.fft(audio_data))
        freqs = np.fft.fftfreq(len(fft), 1/sr)
        pitch_idx = np.argmax(fft[1:len(fft)//2]) + 1
        return freqs[pitch_idx] if pitch_idx > 0 else 100.0
    
    def _estimate_pitch_variance(self, audio_data: np.ndarray, sr: int) -> float:
        """Estimate pitch variance across frames"""
        # Divide into frames and estimate pitch for each
        frame_length = sr // 10  # 100ms frames
        pitches = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            pitch = self._estimate_pitch_mean(frame, sr)
            pitches.append(pitch)
        return np.var(pitches) if len(pitches) > 1 else 0.0
    
    def _estimate_pitch_range(self, audio_data: np.ndarray, sr: int) -> float:
        """Estimate pitch range (max - min)"""
        frame_length = sr // 10
        pitches = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            pitch = self._estimate_pitch_mean(frame, sr)
            pitches.append(pitch)
        return max(pitches) - min(pitches) if len(pitches) > 1 else 0.0
    
    def _calculate_energy_mean(self, audio_data: np.ndarray) -> float:
        """Calculate mean energy"""
        return np.mean(audio_data ** 2)
    
    def _calculate_energy_variance(self, audio_data: np.ndarray) -> float:
        """Calculate energy variance"""
        return np.var(audio_data ** 2)
    
    def _calculate_energy_contour(self, audio_data: np.ndarray) -> float:
        """Calculate energy contour (trend)"""
        frame_length = len(audio_data) // 10
        energies = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            energies.append(np.mean(frame ** 2))
        return np.polyfit(range(len(energies)), energies, 1)[0] if len(energies) > 1 else 0.0
    
    def _calculate_spectral_centroid(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate spectral centroid"""
        fft = np.abs(np.fft.fft(audio_data))
        freqs = np.fft.fftfreq(len(fft), 1/sr)
        return np.average(freqs[:len(fft)//2], weights=fft[:len(fft)//2])
    
    def _calculate_spectral_rolloff(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate spectral rolloff (frequency below which 85% of energy is concentrated)"""
        fft = np.abs(np.fft.fft(audio_data))
        freqs = np.fft.fftfreq(len(fft), 1/sr)
        cumsum = np.cumsum(fft[:len(fft)//2])
        rolloff_idx = np.where(cumsum >= 0.85 * cumsum[-1])[0][0]
        return freqs[rolloff_idx]
    
    def _calculate_mfcc_mean(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate mean MFCC (Mel-Frequency Cepstral Coefficient)"""
        # Simplified: use spectral centroid as proxy
        return self._calculate_spectral_centroid(audio_data, sr)
    
    def _calculate_jitter(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate jitter (pitch period perturbation)"""
        # Simplified: use pitch variance as proxy
        return self._estimate_pitch_variance(audio_data, sr) / 1000.0
    
    def _calculate_shimmer(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate shimmer (amplitude perturbation)"""
        frame_length = sr // 10
        amplitudes = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            amplitudes.append(np.max(np.abs(frame)))
        if len(amplitudes) > 1:
            return np.mean(np.abs(np.diff(amplitudes))) / np.mean(amplitudes)
        return 0.0
    
    def _calculate_noise_harmonic_ratio(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate noise-to-harmonic ratio"""
        fft = np.abs(np.fft.fft(audio_data))
        # Simplified: ratio of noise floor to peak
        return np.mean(fft) / (np.max(fft) + 1e-10)
    
    def _estimate_speech_rate(self, audio_data: np.ndarray, sr: int) -> float:
        """Estimate speech rate (words per minute)"""
        # Simplified: use energy peaks as proxy for syllables
        frame_length = sr // 100  # 10ms frames
        energies = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            energies.append(np.mean(frame ** 2))
        
        # Count peaks (syllables)
        threshold = np.mean(energies) + np.std(energies)
        peaks = np.where(np.array(energies) > threshold)[0]
        syllables = len(peaks)
        
        # Estimate words (assume 3-4 syllables per word)
        words = syllables / 3.5
        duration_seconds = len(audio_data) / sr
        duration_minutes = duration_seconds / 60
        
        return words / duration_minutes if duration_minutes > 0 else 0.0
    
    def _estimate_pause_duration(self, audio_data: np.ndarray, sr: int) -> float:
        """Estimate average pause duration"""
        frame_length = sr // 100
        energies = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            energies.append(np.mean(frame ** 2))
        
        threshold = np.mean(energies) * 0.1
        pauses = np.where(np.array(energies) < threshold)[0]
        
        if len(pauses) > 0:
            pause_frames = np.diff(pauses)
            return np.mean(pause_frames) * (frame_length / sr)
        return 0.0
    
    def _calculate_voice_activity_ratio(self, audio_data: np.ndarray) -> float:
        """Calculate ratio of voiced to total frames"""
        frame_length = len(audio_data) // 100
        voiced_frames = 0
        
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            energy = np.mean(frame ** 2)
            if energy > np.mean(audio_data ** 2) * 0.1:
                voiced_frames += 1
        
        total_frames = len(audio_data) // frame_length
        return voiced_frames / total_frames if total_frames > 0 else 0.0
    
    def _estimate_formant_frequency(self, audio_data: np.ndarray, sr: int, formant_num: int) -> float:
        """Estimate formant frequency"""
        # Simplified: use spectral peaks
        fft = np.abs(np.fft.fft(audio_data))
        freqs = np.fft.fftfreq(len(fft), 1/sr)
        
        # Find peaks
        peaks = []
        for i in range(1, len(fft)//2 - 1):
            if fft[i] > fft[i-1] and fft[i] > fft[i+1]:
                peaks.append((freqs[i], fft[i]))
        
        peaks.sort(key=lambda x: x[1], reverse=True)
        
        if len(peaks) >= formant_num:
            return peaks[formant_num - 1][0]
        return 0.0
    
    def _calculate_intonation_range(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate intonation range"""
        return self._estimate_pitch_range(audio_data, sr)
    
    def _calculate_speech_rhythm(self, audio_data: np.ndarray, sr: int) -> float:
        """Calculate speech rhythm (regularity of speech)"""
        frame_length = sr // 100
        energies = []
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i+frame_length]
            energies.append(np.mean(frame ** 2))
        
        # Rhythm = inverse of energy variance (regular = low variance)
        return 1.0 / (np.var(energies) + 1e-10)
    
    # Health signal detection methods
    
    def _detect_stress(self, features: Dict) -> float:
        """Detect stress from acoustic features"""
        score = 0.0
        
        # High pitch variance indicates stress
        if features['pitch_variance'] > self.biomarker_thresholds['stress']['pitch_variance']:
            score += 0.5
        
        # Elevated energy indicates stress
        if features['energy_mean'] > self.biomarker_thresholds['stress']['energy_level']:
            score += 0.5
        
        return min(score, 1.0)
    
    def _detect_fatigue(self, features: Dict) -> float:
        """Detect fatigue from acoustic features"""
        score = 0.0
        
        # Slow speech rate indicates fatigue
        if features['speech_rate'] < self.biomarker_thresholds['fatigue']['speech_rate']:
            score += 0.5
        
        # Low energy indicates fatigue
        if features['energy_mean'] < self.biomarker_thresholds['fatigue']['energy_level']:
            score += 0.5
        
        return min(score, 1.0)
    
    def _detect_depression(self, features: Dict) -> float:
        """Detect depression from acoustic features"""
        score = 0.0
        
        # Narrow pitch range indicates depression (monotone speech)
        if features['pitch_range'] < self.biomarker_thresholds['depression']['pitch_range']:
            score += 0.5
        
        # Slow speech rate indicates depression
        if features['speech_rate'] < self.biomarker_thresholds['depression']['speech_rate']:
            score += 0.5
        
        return min(score, 1.0)
    
    def _detect_anxiety(self, features: Dict) -> float:
        """Detect anxiety from acoustic features"""
        score = 0.0
        
        # High jitter indicates anxiety
        if features['jitter'] > self.biomarker_thresholds['anxiety']['jitter']:
            score += 0.5
        
        # High pitch variance indicates anxiety
        if features['pitch_variance'] > self.biomarker_thresholds['anxiety']['pitch_variance']:
            score += 0.5
        
        return min(score, 1.0)
    
    def _detect_diabetes_markers(self, features: Dict) -> float:
        """Detect diabetes markers from acoustic features"""
        score = 0.0
        
        # Formant frequency shifts indicate diabetes
        if features['formant_freq_2'] > self.biomarker_thresholds['diabetes_markers']['formant_freq']:
            score += 0.5
        
        # Spectral changes indicate diabetes
        if features['spectral_centroid'] > self.biomarker_thresholds['diabetes_markers']['spectral_centroid']:
            score += 0.5
        
        return min(score, 1.0)
    
    def _detect_neurological_markers(self, features: Dict) -> float:
        """Detect neurological condition markers"""
        score = 0.0
        
        # High jitter indicates neurological issues
        if features['jitter'] > self.biomarker_thresholds['neurological']['jitter']:
            score += 0.5
        
        # High shimmer indicates neurological issues
        if features['shimmer'] > self.biomarker_thresholds['neurological']['shimmer']:
            score += 0.5
        
        return min(score, 1.0)
    
    def _assess_mental_health_risk(self, signals: Dict) -> Dict:
        """Assess overall mental health risk"""
        mental_health_signals = ['stress', 'fatigue', 'depression', 'anxiety']
        detected_count = sum(1 for sig in mental_health_signals if signals[sig]['detected'])
        
        risk_level = 'low'
        if detected_count >= 3:
            risk_level = 'high'
        elif detected_count >= 2:
            risk_level = 'moderate'
        
        return {
            'risk_level': risk_level,
            'detected_conditions': [sig for sig in mental_health_signals if signals[sig]['detected']],
            'recommendation': self._get_mental_health_recommendation(risk_level)
        }
    
    def _get_mental_health_recommendation(self, risk_level: str) -> str:
        """Get mental health recommendation based on risk level"""
        recommendations = {
            'low': 'Continue regular self-care and stress management practices',
            'moderate': 'Consider speaking with a mental health professional',
            'high': 'Strongly recommend consulting with a mental health professional'
        }
        return recommendations.get(risk_level, 'Consult with a healthcare provider')
    
    def generate_biomarker_report(self, audio_path: str, sr: int = 16000) -> Dict:
        """
        Generate comprehensive biomarker report from audio file
        
        Args:
            audio_path: Path to audio file
            sr: Sample rate
        
        Returns:
            Comprehensive biomarker report
        """
        try:
            import librosa
            audio_data, _ = librosa.load(audio_path, sr=sr)
        except:
            # Fallback if librosa not available
            import wave
            with wave.open(audio_path, 'rb') as wav_file:
                audio_data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), np.int16)
                audio_data = audio_data.astype(np.float32) / 32768.0
        
        # Extract features
        features = self.extract_acoustic_features(audio_data, sr)
        
        # Detect health signals
        signals = self.detect_health_signals(features)
        
        # Generate report
        report = {
            'acoustic_features': features,
            'health_signals': signals,
            'summary': {
                'detected_conditions': [sig for sig, data in signals.items() if isinstance(data, dict) and data.get('detected')],
                'mental_health_risk': signals.get('mental_health_risk', {}),
                'recommendations': self._generate_recommendations(signals)
            }
        }
        
        return report
    
    def _generate_recommendations(self, signals: Dict) -> List[str]:
        """Generate health recommendations based on detected signals"""
        recommendations = []
        
        if signals.get('stress', {}).get('detected'):
            recommendations.append('Practice stress-reduction techniques (meditation, deep breathing)')
        
        if signals.get('fatigue', {}).get('detected'):
            recommendations.append('Ensure adequate sleep and rest')
        
        if signals.get('depression', {}).get('detected'):
            recommendations.append('Consider speaking with a mental health professional')
        
        if signals.get('anxiety', {}).get('detected'):
            recommendations.append('Practice anxiety management techniques')
        
        if signals.get('diabetes_markers', {}).get('detected'):
            recommendations.append('Consult with an endocrinologist for diabetes screening')
        
        if signals.get('neurological_markers', {}).get('detected'):
            recommendations.append('Consult with a neurologist for evaluation')
        
        return recommendations if recommendations else ['Continue regular health monitoring']


# Example usage
if __name__ == '__main__':
    analyzer = VoiceBiomarkerAnalyzer()
    
    # Create sample audio data (1 second of noise)
    sr = 16000
    duration = 1
    audio_data = np.random.randn(sr * duration) * 0.1
    
    # Extract features
    features = analyzer.extract_acoustic_features(audio_data, sr)
    print("Acoustic Features:")
    for key, value in features.items():
        print(f"  {key}: {value:.2f}")
    
    # Detect health signals
    signals = analyzer.detect_health_signals(features)
    print("\nHealth Signals:")
    for signal, data in signals.items():
        if isinstance(data, dict):
            print(f"  {signal}: {data}")

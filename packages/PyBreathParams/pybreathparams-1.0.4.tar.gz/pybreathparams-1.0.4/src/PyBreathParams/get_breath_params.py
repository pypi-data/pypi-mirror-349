import joblib
import librosa
import numpy as np
import json
import importlib.resources as pkg_resources

import PyBreathParams

with pkg_resources.files(PyBreathParams).joinpath("model_ie.joblib").open("rb") as f:
    model_ie = joblib.load(f)

with pkg_resources.files(PyBreathParams).joinpath("model_ar.joblib").open("rb") as f:
    model_ar = joblib.load(f)

SR = 16_000               # Target sampling rate
WIN_LENGTH = 0.025        # 25 ms windows
HOP_LENGTH = 0.010        # 10 ms hop
N_MFCC = 20               # Number of MFCC coefficients used

IE = 0
AR = 1


def extract_features(wav_path: str) -> np.ndarray:
    """Load a WAV file and return time—averaged MFCC and delta features."""
    y, sr = librosa.load(wav_path, sr=SR, mono=True)
    # Pad / trim to at least 0.5 s so very short clips still work
    if len(y) < 0.5 * SR:
        y = np.pad(y, (0, int(0.5 * SR) - len(y)))
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=N_MFCC,
        hop_length=int(HOP_LENGTH * sr),
        n_fft=int(WIN_LENGTH * sr),
    )
    delta = librosa.feature.delta(mfcc)
    feat = np.concatenate([mfcc, delta], axis=0)
    # Average over time frames → shape (2 × N_MFCC,)
    return feat.mean(axis=1)

def predict(mode, wav_path):
    if mode == IE:
        clf = model_ie
    elif mode == AR:
        clf = model_ar
    feat = extract_features(wav_path)
    prob = clf.predict_proba(feat.reshape(1, -1))[0]
    if mode == IE:
        label = "inhale" if prob[0] > prob[1] else "exhale"
        print(json.dumps({"label": label, "probabilities": {"inhale": prob[0], "exhale": prob[1]}}))
    elif mode == AR:
        label = "active" if prob[0] > prob[1] else "resting"
        print(json.dumps({"label": label, "probabilities": {"active": prob[0], "resting": prob[1]}}))
    
    return label
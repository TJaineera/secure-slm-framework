# slm-security (scaffold)

Lightweight scaffold to build SLM safety pipeline: sanitization, prompt-injection detection, and adversarial fuzz harness + CI tests.

## Quick start (local)
1. create venv & activate
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. run tests
   ```bash
   pytest -q
   ```

3. optional: run TextAttack fuzz harness (install textattack first)
   ```bash
   # pip install textattack
   python -m fuzz.fuzz_harness
   ```

## What to extend next
- Replace simple regex detector with a trained classifier (export model to detectors/model.joblib and update detectors/prompt_injection_detector.py to call it).
- Add dataset provenance checks and signed dataset registry.
- Add integration tests that run the entire runtime flow (sanitize → detect → compose prompt → SLM generate → output filter).
- Add CI policies to fail if dataset snapshot missing or new dependencies added without approval.

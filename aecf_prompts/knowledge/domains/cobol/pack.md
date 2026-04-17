# COBOL (legacy)

- Preserve copybook contracts, job control assumptions, and transaction boundaries unless explicitly redesigned.
- Prefer strangler or adapter strategies around stable legacy seams instead of broad rewrites.
- Make integration boundaries explicit when exposing legacy capabilities to modern services.
- Validate batch side effects, dataset naming, and scheduling implications before refactors.
- Add regression evidence around financial, operational, or compliance-critical flows.
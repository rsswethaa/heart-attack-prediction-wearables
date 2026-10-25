# Architecture

```mermaid
sequenceDiagram
  participant D as Wearable/Data Source
  participant P as Preprocessor
  participant M as Risk Model
  participant U as User Interface
  D->>P: heart rate, HRV, sleep, activity
  P->>P: validate + engineer features
  P->>M: model-ready vector
  M-->>U: educational risk score + band
```

A production research version could replace the deterministic baseline with a validated classifier trained on appropriately consented clinical/wearable datasets, with calibration and external validation.

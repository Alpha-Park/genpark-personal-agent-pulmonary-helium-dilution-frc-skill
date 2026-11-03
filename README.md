# Pulmonary Closed-Circuit Helium Dilution FRC Personal Agent Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard%20JSON--RPC-orange.svg)]()
[![Production Ready](https://img.shields.io/badge/status-production--ready-green.svg)]()

Deterministic, zero-mock personal agent micro-skill for calculating Functional Residual Capacity (FRC), Total Lung Capacity (TLC), Residual Volume (RV), and RV/TLC ratio using closed-circuit helium dilution gas physics.

## Architecture

```mermaid
flowchart TD
    A[Initial Circuit C1 He & V_spiro] --> B[Closed Rebreathing & Equilibrium]
    B --> C[Equilibrated Concentration C2]
    C --> D[FRC Mass Balance Calculation]
    D --> E[TLC & RV Stratification]
    E --> F[Air Trapping vs Hyperinflation Alert]
```

## Quickstart

```python
from client import HeliumDilutionFRCClient

client = HeliumDilutionFRCClient()
result = client.evaluate_frc_volumes(
    c1_initial_he_fraction=0.10,
    c2_equilibrated_he_fraction=0.0667,
    spirometer_circuit_volume_l=5.0,
    inspiratory_capacity_l=3.0,
    expiratory_reserve_volume_l=1.0
)
print(result)
```

## License

Apache-2.0

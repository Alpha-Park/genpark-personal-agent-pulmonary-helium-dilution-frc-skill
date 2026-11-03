---
name: genpark-personal-agent-pulmonary-helium-dilution-frc-skill
version: 1.0.0
description: Calculates Pulmonary Functional Residual Capacity (FRC), Total Lung Capacity (TLC), Residual Volume (RV), and RV/TLC ratio using closed-circuit helium dilution equilibrium.
authors:
  - GenPark Ecosystem
tags:
  - personal-agent
  - pulmonary
  - frc
  - tlc
  - helium-dilution
  - lung-volumes
  - zero-dependency
---

# Pulmonary Closed-Circuit Helium Dilution FRC Skill

## Mathematical Formulation

The equilibrium conservation of helium mass in a closed rebreathing circuit yields:

$$C_1 \times V_{\text{spirometer}} = C_2 \times (V_{\text{spirometer}} + \text{FRC})$$

Solving for $\text{FRC}$:

$$\text{FRC} = V_{\text{spirometer}} \times \left(\frac{C_1 - C_2}{C_2}\right) - V_{\text{deadspace}}$$

Total lung capacity and residual volume:

$$\text{TLC} = \text{FRC} + \text{IC}$$
$$\text{RV} = \text{FRC} - \text{ERV}$$
$$\text{RV/TLC} (\%) = \left(\frac{\text{RV}}{\text{TLC}}\right) \times 100$$

## Clinical Interpretation
- **Normal**: $\text{RV/TLC} \in [20\%, 35\%]$
- **Isolated Air Trapping**: $\text{RV/TLC} > 35\%$ with preserved $\text{TLC}$
- **Pulmonary Hyperinflation**: $\text{TLC} > 120\%$ predicted and $\text{RV/TLC} > 35\%$ (typical of emphysema/severe COPD)
- **Restrictive Ventilatory Defect**: $\text{TLC} < 80\%$ predicted (interstitial lung disease, fibrosis)

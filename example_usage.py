"""
Example usage of Pulmonary Helium Dilution FRC & Lung Volumes Skill.
Demonstrates normal static lung volumes vs emphysema hyperinflation and gas trapping.
"""

import json
from client import HeliumDilutionFRCClient


def main():
    print("=== Testing Pulmonary Helium Dilution FRC Skill ===")
    client = HeliumDilutionFRCClient()

    # 1. Normal adult subject (C1=10%, C2=6.67%, V_spiro=5.0L -> FRC ~ 2.4L, TLC ~ 5.4L, RV/TLC ~ 26%)
    res_normal = client.evaluate_frc_volumes(
        c1_initial_he_fraction=0.10,
        c2_equilibrated_he_fraction=0.0667,
        spirometer_circuit_volume_l=5.0,
        inspiratory_capacity_l=3.0,
        expiratory_reserve_volume_l=1.0,
        predicted_tlc_l=5.5,
        predicted_frc_l=2.5,
        predicted_rv_l=1.5
    )
    print("\n[Case 1: Normal Static Lung Volumes]")
    print(json.dumps(res_normal, indent=2))

    # 2. Severe emphysematous COPD patient (C1=10%, C2=5.0%, V_spiro=5.0L -> FRC ~ 4.9L, IC=2.5L -> TLC ~ 7.4L > 130% pred, RV/TLC ~ 55%)
    res_hyperinflated = client.evaluate_frc_volumes(
        c1_initial_he_fraction=0.10,
        c2_equilibrated_he_fraction=0.050,
        spirometer_circuit_volume_l=5.0,
        inspiratory_capacity_l=2.6,
        expiratory_reserve_volume_l=0.8,
        predicted_tlc_l=5.5,
        predicted_frc_l=2.5,
        predicted_rv_l=1.5
    )
    print("\n[Case 2: Severe Emphysema / Pulmonary Hyperinflation]")
    print(json.dumps(res_hyperinflated, indent=2))

    # Assertions
    assert res_normal["indices"]["rv_tlc_ratio_pct"] < 35.0
    assert "Normal" in res_normal["interpretation"]["classification"]
    assert res_hyperinflated["indices"]["rv_tlc_ratio_pct"] > 45.0
    assert "Hyperinflation" in res_hyperinflated["interpretation"]["classification"]
    print("\n[SUCCESS] Helium Dilution FRC tests passed!")


if __name__ == "__main__":
    main()

"""
Pulmonary Closed-Circuit Helium Dilution FRC & Lung Volumes Client.
Zero-mock pure Python standard library implementation.
Calculates Functional Residual Capacity (FRC), Total Lung Capacity (TLC),
Residual Volume (RV), and RV/TLC ratio using helium equilibrium dilution mechanics.
"""

import math
from typing import Dict, Any, Optional


class HeliumDilutionFRCClient:
    """
    Evaluates pulmonary volumes and gas trapping via closed-circuit helium dilution:
    C1 * V_spiro = C2 * (V_spiro + FRC)
    FRC = V_spiro * (C1 - C2) / C2 - V_deadspace
    TLC = FRC + IC (Inspiratory Capacity)
    RV = FRC - ERV (Expiratory Reserve Volume)
    RV_TLC_ratio = (RV / TLC) * 100
    """

    def __init__(self):
        pass

    def evaluate_frc_volumes(
        self,
        c1_initial_he_fraction: float,
        c2_equilibrated_he_fraction: float,
        spirometer_circuit_volume_l: float,
        inspiratory_capacity_l: float,
        expiratory_reserve_volume_l: float,
        apparatus_deadspace_l: Optional[float] = 0.10,
        predicted_tlc_l: Optional[float] = 6.0,
        predicted_frc_l: Optional[float] = 3.0,
        predicted_rv_l: Optional[float] = 1.5,
    ) -> Dict[str, Any]:
        """
        Calculates static lung volumes via helium dilution.
        c1_initial_he_fraction: initial helium concentration (e.g. 0.10 = 10% He)
        c2_equilibrated_he_fraction: equilibrated helium concentration (e.g. 0.065 = 6.5% He)
        spirometer_circuit_volume_l: volume of gas in rebreathing circuit (L)
        inspiratory_capacity_l: IC from spirometry (L)
        expiratory_reserve_volume_l: ERV from spirometry (L)
        apparatus_deadspace_l: mouthpiece, valve, filter deadspace (default 0.10 L)
        """
        if c1_initial_he_fraction <= 0 or c2_equilibrated_he_fraction <= 0:
            raise ValueError("Helium fractions must be positive.")
        if c2_equilibrated_he_fraction >= c1_initial_he_fraction:
            raise ValueError("Equilibrated He fraction C2 must be strictly less than initial C1 due to dilution into lung gas.")
        if spirometer_circuit_volume_l <= 0 or inspiratory_capacity_l <= 0 or expiratory_reserve_volume_l <= 0:
            raise ValueError("Spirometric volumes must be strictly positive.")

        # FRC calculation (Liters)
        raw_frc = spirometer_circuit_volume_l * ((c1_initial_he_fraction - c2_equilibrated_he_fraction) / c2_equilibrated_he_fraction)
        frc = max(0.2, raw_frc - apparatus_deadspace_l)

        # TLC and RV calculations
        tlc = frc + inspiratory_capacity_l
        rv = max(0.1, frc - expiratory_reserve_volume_l)

        rv_tlc_ratio_pct = (rv / tlc) * 100.0

        # Percentage of predicted
        frc_pct_pred = (frc / predicted_frc_l) * 100.0 if predicted_frc_l else None
        tlc_pct_pred = (tlc / predicted_tlc_l) * 100.0 if predicted_tlc_l else None
        rv_pct_pred = (rv / predicted_rv_l) * 100.0 if predicted_rv_l else None

        # Clinical interpretation:
        # Normal RV/TLC: 20.0% - 35.0%
        # Air Trapping: RV/TLC > 35.0% with TLC within normal limits (80 - 120%)
        # Pulmonary Hyperinflation: TLC > 120% of predicted and RV/TLC > 35.0% (emphysema / COPD)
        # Restrictive Ventilatory Defect: TLC < 80% of predicted (interstitial lung disease / chest wall disorder)
        if tlc_pct_pred and tlc_pct_pred < 80.0:
            classification = "Restrictive Ventilatory Defect"
            severity = "Reduced total lung capacity consistent with parenchymal or chest wall restriction."
        elif tlc_pct_pred and tlc_pct_pred > 120.0 and rv_tlc_ratio_pct > 35.0:
            classification = "Pulmonary Hyperinflation & Severe Air Trapping"
            severity = "Markedly elevated total lung volume and residual volume typical of severe emphysema or chronic obstruction."
        elif rv_tlc_ratio_pct > 35.0:
            classification = "Isolated Air Trapping"
            severity = "Premature small airway closure with elevated residual gas volume but preserved total lung capacity."
        elif rv_tlc_ratio_pct < 20.0:
            classification = "Low Residual Volume Ratio"
            severity = "Subnormal residual volume fraction, seen in super-normal athletic capacity or mild chest restriction."
        else:
            classification = "Normal Static Lung Volumes"
            severity = "Physiological balance between lung elastic recoil and chest wall expansibility."

        return {
            "status": "success",
            "volumes_liters": {
                "functional_residual_capacity_frc": round(frc, 2),
                "total_lung_capacity_tlc": round(tlc, 2),
                "residual_volume_rv": round(rv, 2),
                "inspiratory_capacity_ic": round(inspiratory_capacity_l, 2),
                "expiratory_reserve_volume_erv": round(expiratory_reserve_volume_l, 2)
            },
            "indices": {
                "rv_tlc_ratio_pct": round(rv_tlc_ratio_pct, 1),
                "tlc_pct_predicted": round(tlc_pct_pred, 1) if tlc_pct_pred else None,
                "frc_pct_predicted": round(frc_pct_pred, 1) if frc_pct_pred else None,
                "rv_pct_predicted": round(rv_pct_pred, 1) if rv_pct_pred else None
            },
            "interpretation": {
                "classification": classification,
                "clinical_finding": severity
            }
        }

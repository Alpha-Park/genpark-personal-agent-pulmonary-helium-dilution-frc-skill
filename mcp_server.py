"""
MCP Server for Pulmonary Closed-Circuit Helium Dilution FRC Skill.
Provides standard Model Context Protocol JSON-RPC tool endpoints.
"""

import sys
import json
from client import HeliumDilutionFRCClient


def main():
    client = HeliumDilutionFRCClient()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "evaluate_frc_volumes",
                            "description": "Calculates Pulmonary Functional Residual Capacity (FRC), Total Lung Capacity (TLC), Residual Volume (RV), and RV/TLC ratio using closed-circuit helium dilution equilibrium.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "c1_initial_he_fraction": {
                                        "type": "number",
                                        "description": "Initial helium fraction in closed spirometer circuit (e.g. 0.10 for 10% He)."
                                    },
                                    "c2_equilibrated_he_fraction": {
                                        "type": "number",
                                        "description": "Equilibrated helium fraction after rebreathing (e.g. 0.065 for 6.5% He)."
                                    },
                                    "spirometer_circuit_volume_l": {
                                        "type": "number",
                                        "description": "Total volume of gas in spirometer circuit (Leters)."
                                    },
                                    "inspiratory_capacity_l": {
                                        "type": "number",
                                        "description": "Measured Inspiratory Capacity IC from spirometer maneuver (Liters)."
                                    },
                                    "expiratory_reserve_volume_l": {
                                        "type": "number",
                                        "description": "Measured Expiratory Reserve Volume ERV from spirometer maneuver (Liters)."
                                    },
                                    "apparatus_deadspace_l": {
                                        "type": "number",
                                        "description": "Mouthpiece, valve, and filter deadspace volume in Liters (default: 0.10 L)."
                                    },
                                    "predicted_tlc_l": {
                                        "type": "number",
                                        "description": "Predicted normal TLC based on demographics (Liters, optional)."
                                    },
                                    "predicted_frc_l": {
                                        "type": "number",
                                        "description": "Predicted normal FRC based on demographics (Liters, optional)."
                                    },
                                    "predicted_rv_l": {
                                        "type": "number",
                                        "description": "Predicted normal RV based on demographics (Liters, optional)."
                                    }
                                },
                                "required": [
                                    "c1_initial_he_fraction",
                                    "c2_equilibrated_he_fraction",
                                    "spirometer_circuit_volume_l",
                                    "inspiratory_capacity_l",
                                    "expiratory_reserve_volume_l"
                                ]
                            }
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "evaluate_frc_volumes":
                try:
                    out = client.evaluate_frc_volumes(**args)
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(out, indent=2)}]
                        }
                    }
                except Exception as e:
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "isError": True,
                        "error": {"code": -32000, "message": str(e)}
                    }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()

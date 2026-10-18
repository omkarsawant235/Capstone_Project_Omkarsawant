import os
import json

def generate_scr_narrative_offline(
    findings
):
    narrative = f"""
Situation:
Mamaearth generated cleaned revenue of
₹{findings['cleaned_total_revenue_inr']:,.2f}.

Complication:
COD shows a return rate of
{findings['return_rate_by_payment']['COD']}%.
Tier-2 COD customers show the highest
return rate of
{findings['highest_risk_segment']['return_rate_pct']}%.

Resolution:
The revenue reconciliation difference of
₹{findings['duplicate_reconciliation_delta_inr']:,.2f}
comes entirely from duplicate orders.

After removing outlier effects,
March becomes the true peak month with
₹{findings['true_peak_month']['revenue_inr']:,.2f}.
"""
    return {
        "status": "success",
        "narrative": narrative,
        "tokens": 0
    }

with open(
    "narrator/findings.json"
) as f:
    findings = json.load(f)

result = generate_scr_narrative_offline(
    findings
)

print(result["narrative"])

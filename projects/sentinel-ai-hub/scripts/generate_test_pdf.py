"""
-------------------------------------------------------------------------
PROJECT SENTINEL: DYNAMIC SLA PDF GENERATOR
-------------------------------------------------------------------------
This script allows you to create professional-looking PDF contracts (SLAs) 
on the fly. Each PDF contains specific disaster protocols that the 
Sentinel AI agents will discover during an event.

USAGE:
    python scripts/generate_test_pdf.py "<Warehouse>" "<BackupHub>" <DelayLimit> <WeeklyFine>

EXAMPLE:
    python scripts/generate_test_pdf.py "Chicago Warehouse" "Detroit-Backup-9" 12 8500

WHAT HAPPENS NEXT:
    1. The PDF is saved in projects/sentinel-ai-hub/pdfs/
    2. You run 'python scripts/ingest_doc.py <path_to_pdf>' to index it.
    3. You run 'python scripts/simulate_event.py' to test the AI's response.
-------------------------------------------------------------------------
"""

import sys
import os
try:
    from fpdf import FPDF
except ImportError:
    print("Error: 'fpdf2' library not found. Please run 'pip install fpdf2'.")
    sys.exit(1)

def generate_dynamic_pdf(warehouse_name, hub_name, delay_hours, penalty_amount):
    """
    Constructs a Service Level Agreement (SLA) PDF with custom disruption rules.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Document Title
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(33, 37, 41) # Dark Grey
    pdf.cell(0, 15, "MASTER SERVICE AGREEMENT: GLOBAL LOGISTICS", ln=True, align='C')
    pdf.ln(5)

    # 2. Specific Facility Reference
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"TARGET FACILITY: {warehouse_name.upper()}", ln=True, align='L')
    pdf.ln(5)

    # 3. Disruption & Force Majeure Clause
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ARTICLE 1.1: EMERGENCY DIVERSION PROTOCOL", ln=True)
    pdf.set_font("Arial", size=11)
    
    clause_text = (
        f"In the event of a documented Force Majeure (weather, strike, or hardware failure), "
        f"all critical operations at {warehouse_name} shall be transitioned to the designated "
        f"Alternate Processing Center: {hub_name}. This transition must occur within {delay_hours} "
        f"hours of the initial timestamped alert."
    )
    pdf.multi_cell(0, 7, clause_text)
    pdf.ln(5)

    # 4. Penalty & Compliance Clause
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ARTICLE 2.4: FINANCIAL REMEDIATION FOR DELAYS", ln=True)
    pdf.set_font("Arial", size=11)
    
    penalty_text = (
        f"In the case of delayed diversion exceeding the limit defined in Article 1.1, the "
        f"Contracting Party shall incur a recurring penalty of ${penalty_amount} USD per 24-hour "
        f"period. This penalty is non-negotiable and accumulates starting at hour {int(delay_hours) + 1}."
    )
    pdf.multi_cell(0, 7, penalty_text)
    pdf.ln(10)

    # 5. Electronic Signature Placeholder
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Digitally signed and verified by Project Sentinel Compliance Hub.", ln=True)

    # Output Management
    output_dir = "projects/sentinel-ai-hub/pdfs"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{warehouse_name.lower().replace(' ', '_')}_sla.pdf")
    
    pdf.output(filename)
    print(f"\n--- PDF GENERATED SUCCESSFULLY ---")
    print(f"Location: {filename}")
    print(f"Target:   {warehouse_name}")
    print(f"Backup:   {hub_name}")
    print(f"Fine:     ${penalty_amount}")
    print(f"----------------------------------\n")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("\n[!] Error: Missing arguments.")
        print("Usage: python scripts/generate_test_pdf.py <Warehouse> <Hub> <DelayHours> <Penalty>")
        print("Hint:  Use quotes for multi-word names, e.g. \"Miami Dock\"")
    else:
        generate_dynamic_pdf(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

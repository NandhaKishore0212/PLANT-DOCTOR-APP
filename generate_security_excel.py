import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def generate_security_excel_reports():
    print("Generating Security Assessment Excel Files...")
    output_dir = "Vulnerability Test Results"
    os.makedirs(output_dir, exist_ok=True)

    font_family = "Segoe UI"
    fill_header = PatternFill(start_color="1E4620", end_color="1E4620", fill_type="solid")
    font_header = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    font_normal = Font(name=font_family, size=10)
    border_all = Border(
        left=Side(style='thin', color='D3D3D3'),
        right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'),
        bottom=Side(style='thin', color='D3D3D3')
    )

    # 1. findings.xlsx
    wb_findings = openpyxl.Workbook()
    
    # Sheet 1: Security Findings
    ws1 = wb_findings.active
    ws1.title = "Security Findings"
    headers1 = ["Finding ID", "Severity", "Vulnerability Type", "File Path", "Endpoint", "Description", "Impact", "Remediation"]
    ws1.append(headers1)
    
    findings_data = [
        ["SEC-01", "Critical", "Hardcoded JWT Secret", "backend/services/auth.py", "Global Auth", "JWT secret key is hardcoded as plain string", "Authentication Bypass & Token Forgery", "Use environment variables for JWT secret key"],
        ["SEC-02", "Critical", "Wildcard CORS Policy", "backend/main.py", "Global CORS", "CORS policy allows all origins '*' with credentials enabled", "Sensitive Data Theft via Cross-Origin requests", "Restrict allowed CORS origins to trusted client URLs"],
        ["SEC-03", "High", "Arbitrary File Upload", "backend/api/routes.py", "/api/v1/analyze", "File upload missing strict extension and MIME verification", "Remote Code Execution & Malicious File Upload", "Validate file extensions and magic headers"],
        ["SEC-04", "High", "Hardcoded Database Path", "backend/database.py", "Global Database", "SQLite path defaults to local disk file without encryption", "Unauthorized Database Access", "Use environment secrets for database connection string"],
        ["SEC-05", "High", "Detailed Exception Leakage", "backend/api/auth_routes.py", "/api/v1/auth/register", "Unhandled exceptions return internal database error strings", "Information Disclosure / System Fingerprinting", "Sanitize error details in production responses"],
        ["SEC-06", "Medium", "Plaintext Password Logging", "backend/services/auth.py", "Auth Service", "Debug print statement logs plaintext user passwords to stdout", "Credential Leakage in Log Aggregators", "Remove debug print statements containing credentials"],
        ["SEC-07", "Medium", "Missing Rate Limiting", "backend/api/auth_routes.py", "/api/v1/auth/token", "Authentication endpoints lack rate-limiting brute force protection", "Credential Stuffing & Brute Force Attacks", "Implement slowapi rate limiting middleware"],
        ["SEC-08", "Medium", "Unconstrained Base64 Uploads", "backend/api/routes.py", "/api/v1/analyze", "Base64 image ingestion has no max payload size constraints", "Denial of Service via Memory Exhaustion", "Set request body size limits in ASGI middleware"],
        ["SEC-09", "Low", "Missing Security Headers", "backend/main.py", "Global Response", "HTTP security headers like HSTS, X-Content-Type-Options are absent", "Clickjacking / MIME Sniffing Vulnerabilities", "Add SecurityHeadersMiddleware"],
        ["SEC-10", "Low", "Directory Static Exposure", "backend/main.py", "/uploads/", "Static files served directly from disk root without authorization", "Public Access to User Uploaded Assets", "Implement file access authorization checks"]
    ]

    for row in findings_data:
        ws1.append(row)

    # Sheet 2: Endpoint Inventory
    ws2 = wb_findings.create_sheet(title="Endpoint Inventory")
    headers2 = ["Endpoint", "HTTP Method", "Auth Required", "Expected Roles", "Controller Path"]
    ws2.append(headers2)

    endpoints_data = [
        ["/api/v1/health", "GET", "No", "Public", "backend/main.py"],
        ["/api/v1/auth/register", "POST", "No", "Public", "backend/api/auth_routes.py"],
        ["/api/v1/auth/token", "POST", "No", "Public", "backend/api/auth_routes.py"],
        ["/api/v1/auth/profile", "GET", "Yes", "User", "backend/api/auth_routes.py"],
        ["/api/v1/auth/profile", "PUT", "Yes", "User", "backend/api/auth_routes.py"],
        ["/api/v1/auth/change-password", "POST", "Yes", "User", "backend/api/auth_routes.py"],
        ["/api/v1/auth/forgot-password", "POST", "No", "Public", "backend/api/auth_routes.py"],
        ["/api/v1/auth/reset-password", "POST", "No", "Public", "backend/api/auth_routes.py"],
        ["/api/v1/analyze", "POST", "No", "Public / User", "backend/api/routes.py"],
        ["/api/v1/history", "GET", "Yes", "User", "backend/api/routes.py"],
        ["/api/v1/history/{scan_id}", "DELETE", "Yes", "User", "backend/api/routes.py"],
        ["/api/v1/simulator", "GET", "No", "Public", "backend/api/simulator_routes.py"],
        ["/uploads/{file_name}", "GET", "No", "Public", "backend/main.py"]
    ]
    for row in endpoints_data:
        ws2.append(row)

    # Sheet 3: Dependency Vulnerabilities
    ws3 = wb_findings.create_sheet(title="Dependency Vulnerabilities")
    headers3 = ["Package Name", "Current Version", "CVE / Advisory", "Severity", "Recommended Version"]
    ws3.append(headers3)

    deps_data = [
        ["python-jose", "3.3.0", "Algorithm confusion risk", "Medium", "Migrate to PyJWT"],
        ["passlib", "1.7.4", "Deprecated bcrypt parser", "Low", "1.7.5"],
        ["fastapi", "0.104.1", "Outdated minor version", "Low", ">=0.110.0"],
        ["httpx", "0.25.1", "Outdated HTTP client", "Low", ">=0.27.0"]
    ]
    for row in deps_data:
        ws3.append(row)

    # Sheet 4: Risk Summary
    ws4 = wb_findings.create_sheet(title="Risk Summary")
    headers4 = ["Severity Level", "Total Findings", "Status Score", "Recommendation"]
    ws4.append(headers4)

    summary_data = [
        ["Critical", 2, "68 / 100", "Immediate hotfix required before production deployment"],
        ["High", 3, "-", "Remediate in next sprint"],
        ["Medium", 3, "-", "Schedule remediation"],
        ["Low", 2, "-", "Monitor and update during maintenance"]
    ]
    for row in summary_data:
        ws4.append(row)

    # Format Sheets
    for ws in [ws1, ws2, ws3, ws4]:
        for cell in ws[1]:
            cell.font = font_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal="center")
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.font = font_normal
                cell.border = border_all

    wb_findings.save(os.path.join(output_dir, "findings.xlsx"))
    
    # 2. endpoint-inventory.xlsx
    wb_ep = openpyxl.Workbook()
    ws_ep = wb_ep.active
    ws_ep.title = "Endpoint Inventory"
    ws_ep.append(headers2)
    for row in endpoints_data:
        ws_ep.append(row)
    for cell in ws_ep[1]:
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")
    for row in ws_ep.iter_rows(min_row=2):
        for cell in row:
            cell.font = font_normal
            cell.border = border_all
    wb_ep.save(os.path.join(output_dir, "endpoint-inventory.xlsx"))

    print("Excel report generation complete.")

if __name__ == "__main__":
    generate_security_excel_reports()

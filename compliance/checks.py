import os, re, shutil
from .utils import run_cmd, safe_read, is_root

def check_password_policy():
    res = {"name": "Password Policy", "status": "UNKNOWN", "details": []}
    content = safe_read("/etc/login.defs")
    if content.startswith("__ERROR__"):
        res["status"] = "SKIPPED"
        res["details"].append(content)
        return res

    min_len = max_days = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("PASS_MIN_LEN"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                min_len = int(parts[1])
        if line.startswith("PASS_MAX_DAYS"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                max_days = int(parts[1])

    res["details"].append(f"PASS_MIN_LEN = {min_len}")
    res["details"].append(f"PASS_MAX_DAYS = {max_days}")

    ok = True
    if not min_len or min_len < 8:
        ok = False
        res["details"].append("PASS_MIN_LEN should be >= 8")
    if not max_days or max_days > 90:
        ok = False
        res["details"].append("PASS_MAX_DAYS should be <= 90")

    res["status"] = "OK" if ok else "WARNING"
    return res

def check_ssh_root_login():
    res = {"name": "SSH Root Login", "status": "UNKNOWN", "details": []}
    path = "/etc/ssh/sshd_config"
    if not os.path.exists(path):
        res["status"] = "SKIPPED"
        res["details"].append(f"{path} not found.")
        return res
    content = safe_read(path)
    permit = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"PermitRootLogin\s+(.+)", line, re.IGNORECASE)
        if m:
            permit = m.group(1).strip()
            break
    res["details"].append(f"PermitRootLogin = {permit}")
    res["status"] = "OK" if permit and permit.lower() in ("no", "prohibit-password") else "FAIL"
    return res

def check_firewall_status():
    res = {"name": "Firewall Status", "status": "UNKNOWN", "details": []}
    rc, out, err = run_cmd(["ufw", "status"])
    if rc == 0:
        res["details"].append(out)
        res["status"] = "OK" if "active" in out.lower() else "FAIL"
        return res
    rc, out, err = run_cmd(["firewall-cmd", "--state"])
    if rc == 0:
        res["details"].append(out)
        res["status"] = "OK" if out.strip() == "running" else "FAIL"
        return res
    res["status"] = "SKIPPED"
    res["details"].append("No firewall tool found.")
    return res

def run_all_checks():
    checks = [check_password_policy, check_ssh_root_login, check_firewall_status]
    results = []
    for fn in checks:
        try:
            results.append(fn())
        except Exception as e:
            results.append({"name": fn.__name__, "status": "ERROR", "details": [str(e)]})
    return results

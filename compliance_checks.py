import subprocess

def check_password_policy():
    # Mock check – in real world, we'd parse /etc/login.defs
    return ("Password Length", "Pass", "Minimum 8 characters enforced")

def check_ssh_root_login():
    # Simulated check
    return ("SSH Root Login", "Warning", "Root login over SSH is enabled")

def check_firewall_status():
    # Simulate subprocess call
    try:
        subprocess.run(["ufw", "status"], capture_output=True)
        return ("Firewall Status", "Pass", "Firewall is active")
    except FileNotFoundError:
        return ("Firewall Status", "Fail", "UFW not installed")

def run_all_checks():
    return [
        check_password_policy(),
        check_ssh_root_login(),
        check_firewall_status()
    ]

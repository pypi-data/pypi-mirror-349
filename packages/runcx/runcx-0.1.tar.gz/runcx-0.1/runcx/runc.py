import os, sys, shutil, subprocess

BIN_DIR = os.path.expanduser("~/.runc_bin")
os.makedirs(BIN_DIR, exist_ok=True)

def runc_add(name):
    source = os.path.abspath(name)
    if not os.path.isfile(source):
        print(f"[!] File '{name}' not found in current directory.")
        sys.exit(1)
    target = os.path.join(BIN_DIR, name)
    shutil.copy(source, target)
    os.chmod(target, 0o755)
    print(f"[+] Added '{name}' to runc (stored in ~/.runc_bin/)")

def runc_run(name, args):
    target = os.path.join(BIN_DIR, name)
    if not os.path.exists(target):
        print(f"[!] '{name}' not found in runc. Use: runc add {name}")
        sys.exit(1)
    subprocess.run([target] + args)

def main():
    if len(sys.argv) < 2:
        print("Usage:\n  runc add <file>\n  runc <file> [args...]")
        sys.exit(1)

    if sys.argv[1] == "add" and len(sys.argv) == 3:
        runc_add(sys.argv[2])
    else:
        runc_run(sys.argv[1], sys.argv[2:])

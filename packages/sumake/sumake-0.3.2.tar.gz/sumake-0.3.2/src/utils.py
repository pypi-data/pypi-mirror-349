import argparse
import os
import subprocess
import sys
import time
import traceback
from os.path import basename, splitext

DEPLOY_HOST = os.environ["DEPLOY_HOST"]
DEPLOY_PORT = os.environ["DEPLOY_PORT"]
DEPLOY_PASSWORD = os.getenv("DEPLOY_PASSWORD")


def run_cmd(_cmd):
    try:
        cmd = [
            "bash", "-c",
            _cmd.replace("\n", "").strip()
        ]
        print(_cmd)
        subprocess.run(cmd, check=True)
        print("success")
        return True
    except Exception as e:
        # traceback.print_exc()
        # raise e
        print("failed", e)


def ssh_root(cmd):
    cmd = escape_cmd(cmd)
    # cmd = cmd.replace('"', '\\"')
    run_cmd(f"""
    ssh -o StrictHostKeyChecking=no
    -p {DEPLOY_PORT} {DEPLOY_HOST} 'echo {DEPLOY_PASSWORD} | sudo -S bash -c "{cmd}"'
    """.strip())


def ssh(cmd):
    cmd = escape_cmd(cmd)
    # cmd = "source ~/.zshrc && " + cmd
    cmd = " [[ -f ~/.zshrc ]] && source ~/.zshrc; " + cmd
    run_cmd(f"""
    ssh -o StrictHostKeyChecking=no
    -p {DEPLOY_PORT} {DEPLOY_HOST} '{cmd}'
    """)


def upload(source_path, destination_path):
    print(f"upload: {source_path} -> {destination_path}")
    des_dir = os.path.dirname(destination_path)
    if des_dir != "":
        ssh(f"mkdir -p {des_dir}")
    run_cmd(
        f"rsync -av --progress --rsh='ssh -o StrictHostKeyChecking=no -p {DEPLOY_PORT}' "
        f" {source_path} "
        f" {DEPLOY_HOST}:{destination_path}"
    )


def upload_root(source_path, destination_path):
    print(f"upload_root: {source_path} -> {destination_path}")
    tmp = "/tmp/" + destination_path
    # tmp_dir = os.path.dirname(tmp)
    des_dir = os.path.dirname(destination_path)
    # ssh(f"mkdir -p {tmp_dir}")
    upload(source_path, tmp)
    rsync_cmd = f"rsync -av {tmp} {destination_path}"
    # ssh_root(f"mkdir -p {des_dir} && mv {tmp} {destination_path}")
    if des_dir != "" and des_dir != "/tmp":
        cmd = f"mkdir -p {des_dir} && {rsync_cmd}"
    else:
        cmd = rsync_cmd
    ssh_root(cmd)


def download(source_path, destination_path):
    dir = os.path.dirname(destination_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    run_cmd(
        f"rsync -av --rsh='ssh -o StrictHostKeyChecking=no -p {DEPLOY_PORT}' "
        f" {DEPLOY_HOST}:{source_path}"
        f" {destination_path} "
    )


def parse_upload_args(remaining_args):
    src = remaining_args[0].strip()
    if len(remaining_args) > 1:
        dst = remaining_args[1].strip()
    else:
        dst = f"~/{src}"
    return src, dst


def escape_cmd(cmd):
    cmd = remove_quota(cmd)
    cmd = cmd.replace('"', '\\"')
    return cmd


def remove_quota(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return s


def ssh_action(args: argparse.Namespace, remaining_args: list[str]):
    if args.file:
        file = args.file
        name = splitext(basename(file))[0]
        suffix = splitext(basename(file))[1]
        timestamp = int(time.time())
        # dest_file = f"/tmp/{name}_{timestamp}{suffix}"
        dest_file = f"/tmp/{name}{suffix}"
        upload(file, dest_file)
        cmd = f"chmod +x {dest_file} && {dest_file} "
        if len(remaining_args) > 0:
            cmd += remove_quota(" ".join(remaining_args))
    else:
        cmd = remaining_args[0]

    if args.root:
        ssh_root(cmd)
    else:
        ssh(cmd)


def parse_download_args():
    src = sys.argv[2].strip()
    src_relative = False
    if not src.startswith("~/") and not src.startswith("/"):
        src_relative = True
    if len(sys.argv) > 3:
        dst = sys.argv[3].strip()
    else:
        if src_relative:
            dst = f"{src}"
        else:
            sys.exit("dst is required")
    if src_relative:
        src = f"~/{src}"
    return src, dst


parser = argparse.ArgumentParser(description="A script with complex command-line arguments.")
parser.add_argument("action", help="action: upload, download, ssh")
parser.add_argument("--root", action="store_true", help="root")
parser.add_argument("--file", type=str, help="script file for ssh")

if __name__ == "__main__":
    print(sys.argv)
    args, remaining_args = parser.parse_known_args()
    print(args, remaining_args)

    action = args.action
    # cmd = sys.argv[1]
    if action == "upload":
        src, dst = parse_upload_args(remaining_args)
        if args.root:
            upload_root(src, dst)
        else:
            upload(src, dst)

    # elif cmd == "upload":
    #     src, dst = parse_upload_args()
    #     upload_root(src, dst)

    elif action in ["download"]:
        src, dst = parse_download_args()
        download(src, dst)

    elif action in ["ssh", "command"]:
        ssh_action(args, remaining_args)
        # cmd = sys.argv[2]
        # cmd = remaining_args[0]
        # if args.file:
        #
        # if args.roort:
        #     ssh_root(cmd)
        # else:
        #     ssh(cmd)
        #
    else:
        print("unknown command", action)

name = "k_launcher"
version = "1.0.0"
author = "felix benicourt"

description = "Custom launcher command"

build_command = False
requires = ['k_config', 'k_constants', 'python-3.10']

def commands():
    env.PYTHONPATH.append(this.root)
    env.PYTHONPATH.append("{root}/k_launcher")
    env.PATH.append(this.root)
    env.PATH.append("{root}/k_launcher")
    alias("rez", "python {root}/k_launcher/k_launcher_rez.py")
    alias("git", "python {root}/k_launcher/k_launcher_git.py")
    #alias("test", "python {root}/k_launcher/k_launcher_context.py")


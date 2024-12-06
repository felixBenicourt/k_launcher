name = "k_launcher"
version = "1.0.0"
author = "felix benicourt"

description = "Custom launcher command"

build_command = False
requires = ['k_config']

def commands():
    env.PYTHONPATH.append(this.root)
    env.PYTHONPATH.append("{root}/k_launcher")
    env.PATH.append(this.root)
    env.PATH.append("{root}/k_launcher")


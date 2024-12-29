
# K_launcher

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Git Commands](#git-commands)
- [License](#license)

`k_launcher` is a command-line utility designed for managing different configurations and launching DCC (Digital Content Creation) tools such as Maya, Houdini, and more, with custom environment settings and packages. The tool simplifies the process of working with different configurations, packages, and contexts.

## Features

- **Environment Management**: Manage and set up environment variables based on the selected configuration.
- **DCC Tool Launch**: Launch popular DCC tools like Maya, Houdini, and others with the correct configuration and environment setup.
- **Package Management**: Add and remove switch packages for DCC tools.
- **Context Management**: Save and load context configurations to resume workflows.

## Prerequisites

- `rez` package manager installed
- Required software installed (e.g., Maya, Houdini)
- Correct configuration files set up in the `CONTEXT` folder. These configuration files (e.g., `dev-k_config.rxt`, `main-k_config.rxt`) should define the environment variables and packages needed for your workflow.

## Installation

1. Ensure `rez` is installed and configured in your environment.
2. Clone the repository or copy the `k_launcher` tool to your local system.
3. Set up the `CONTEXT` folder with the necessary configuration files (e.g., `dev-k_config.rxt`, `main-k_config.rxt`).

## Usage

The `k_launcher` utility can be used from the command line to manage the environment and launch DCC tools. Below are the key commands:

### Manage dev config

```bash
rez env k_launcher -- rez -config dev -launch maya
```
Launch the DCC with the custom config

```bash
rez env k_launcher -- rez -config <config_name> -save
```
This will save the context for the specified configuration.

```bash
rez env k_launcher -- rez -config <config_name> -load <context_name>
```
This will load the environment context saved under <context_name> for the specified configuration.

```bash
rez env k_launcher -- rez -config dev -add myPackage -launch maya
```
This will launch Maya with the dev configuration and add myPackage to the environment.

```bash
rez env k_launcher -- rez -config dev -add myPackage -launch maya
```
This will grab Iter latest version from the PROD to LOCAL.

```bash
rez env k_launcher -- rez -grab iter
```

This will launch Iter from the LOCAL environment.

```bash
rez env k_launcher -- rez -switch iter -launch iter
```

## Git Commands

`k_launcher` also supports Git-related functionality for managing repositories, branches, and commits. Below are the available Git commands:

### 1. Clone a Git repository

```bash
rez env k_launcher -- git -clone_repo <repository_url> <local_folder> [optional_repo_folder_name]
```

### 2. Create a new branch

```bash
rez env k_launcher -- git -create_branch <repository_path> <repository_name> <new_branch_name>
```

### 3. Checkout an existing branch

```bash
rez env k_launcher -- git -checkout_branch <repository_path> <repository_name> <branch_name>
```

### 4. Check the repository status

```bash
rez env k_launcher -- git -status <repository_path> <repository_name>
```

### 5. Pull the latest changes from remote

```bash
rez env k_launcher -- git -pull <repository_path> <repository_name>
```

### 6. Push local commits to the remote repository

```bash
rez env k_launcher -- git -push <repository_path> <repository_name>
```

### 7. Show the commit log

```bash
rez env k_launcher -- git -log <repository_path> <repository_name>
```

### Example Git Commands

```bash
rez env k_launcher -- git -clone_repo https://example.com/repo.git /path/to/folder my-repo
rez env k_launcher -- git -create_branch /path/to/folder my-repo new-feature-branch
rez env k_launcher -- git -checkout_branch /path/to/folder my-repo main
rez env k_launcher -- git -status /path/to/folder my-repo
rez env k_launcher -- git -pull /path/to/folder my-repo
rez env k_launcher -- git -push /path/to/folder my-repo
rez env k_launcher -- git -log /path/to/folder my-repo
```

## License
```text
Custom License Agreement

Copyright (c) 2024 Felix Benicourt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use,
study, and modify the Software for personal, educational, or internal purposes,
subject to the following conditions:

1. Redistribution and Resale:
   - Redistribution, sublicensing, or resale of the Software, in whole or in part, 
     is strictly prohibited without prior written consent from the author.

2. Attribution:
   - This copyright notice and permission notice shall be included in all copies 
     or substantial portions of the Software.

3. No Warranty:
   - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
     FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL 
     THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER 
     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING 
     FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
     IN THE SOFTWARE.
```


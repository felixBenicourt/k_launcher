
# K_launcher

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Git Commands](#git-commands)
- [License](#license)


`k_launcher` is a versatile command-line utility designed to streamline the management of configurations and the launching of DCC (Digital Content Creation) tools such as Maya, Houdini, and more. With its ability to handle custom environment settings and packages, `k_launcher` simplifies complex workflows, enabling artists and developers to focus on their work without worrying about setup intricacies.


## Overview

[![Watch the video](https://i.imgur.com/RkaPYbH.png)](https://vimeo.com/manage/videos/1044001514)


## Key Features

- **Configuration Management**: Easily manage various environment settings and packages for DCC tools.
- **Git Workflow Automation**: Simplifies Git operations within production pipelines, offering seamless handling of packages, branches, commits, tags, pull requests, and releases.

## How `k_launcher` Enhances Workflow

`k_launcher` intelligently saves session-specific information based on the terminal being used. This allows users to retrieve and reuse their configurations, context, and environment settings effortlessly across your session. By automating and organizing these elements, `k_launcher` provides a smoother and more productive experience for managing digital content creation tools and production pipelines.


## Features
### **1. Package Management**
- **Grab Packages**: Easily fetch packages from production to local environments.
- **Clone Packages**: Clone packages with or without specifying custom paths.

### **2. Branch Management**
- **Create Branches**: Automatically create new branches for development.
- **Checkout Branches**: Switch between branches effortlessly.

### **3. Commit and Tag Management**
- **Commit Changes**: Stage and commit changes with meaningful messages.
- **Tag Management**: Create and manage tags for versioning and releases.

### **4. Release Management**
- **Automated Releases**: Push changes to production (`PROD`) environments with minimal effort.

## Benefits
### **Advanced Production Pipeline Integration**
The tool is designed to fit seamlessly into production pipelines, handling tasks like environment synchronization, version control, and release management with precision.

### **Version Control Mastery**
By automating Git workflows, this tool eliminates manual errors and ensures that team collaboration is streamlined.

## Use Cases
- **Local to Production Workflow**: Grab packages from production, develop locally, and push back to production with proper versioning and releases.
- **Team Collaboration**: Manage branches and pull requests across multiple contributors with ease.
- **Versioning and Releases**: Tag commits, create pull requests, and push releases with confidence.

## How It Works
1. **Cloning Packages**: Run the command to clone a package from production.
2. **Branching**: Create or switch to a development branch.
3. **Committing Changes**: Add and commit your changes with a meaningful message.
4. **Releasing to Production**: Merge the pull request and execute the release command to push changes to production.

## Technical Details
### **Supported Workflows**
- Git operations: cloning, branching, committing, tagging, pull requests, merging, and releases.
- Environment-specific paths: local and production synchronization.

### **Automation Highlights**
- Simplifies branching and merging workflows.
- Ensures consistency with automated pull requests and tagging.
- Reduces downtime with reliable package handling and releases.

## Future Enhancements
- Add a graphical user interface (GUI) for non-technical users.
- Integrate CI/CD pipelines for automated testing and deployment.


## Prerequisites

- `rez` package manager installed
- Required software installed (e.g., Maya, Houdini)
- Correct configuration files set up in the `CONTEXT` folder. These configuration files should define the environment variables and packages needed for your workflow.


## Usage

### Rez Commands

The `k_launcher` utility can be used from the command line to manage the environment and launch DCC tools.

```text
This is the documentation for the k_launcher Rez Functionality.

Usage:
    python k_launcher_rez.py [args*]

Arguments (args*):
    -c, --config : name of the config you're working on.
    -co, --context : display the current context.
    -p, --package : package to load with the environment.
    -a, --add : additional packages to be added.
    -l, --launch : launch the DCC software by name.
    -s, --save : save the context/configuration.
    -lo, --load : load the saved context/configuration.
    -i, --info : display information about the tool.
    -e, --echo : display the current settings.
    -g, --grab : grab the package in PROD to LOCAL.
    -w, --switch : switch the package to the local version.
    -r, --release : chosen LOCAL package to release.
    -pr, --prod_release : chosen version of the package to release on PROD.
    -vs, --vs_code : launch vs code with the path and package.

Example Launch Commands:
    python k_launcher_rez.py --info
    python k_launcher_rez.py --config dev --launch maya --add myPackage
    python k_launcher_rez.py --save devConfig
    python k_launcher_rez.py --load prodConfig

Config Structure:
    config : package : context/path/file.rxt

Class KLauncher_rez:
    The KLauncher_rez class manages the environment setup and execution of DCC software.
    It handles various tasks such as setting and displaying configuration details,
    managing the environment variables using `rez`, and launching DCC software with
    the specified packages and settings.

    Attributes:
        - config_set (str): The configuration set to use.
        - package (str): The main package to load with the environment.
        - add_package (str): Additional packages to be added to the environment.
        - dcc_launch (str): The DCC software to launch.
        - save_config (str): The configuration to save.
        - load_config (str): The configuration to load.
        - grab_commande (list): List of packages to grab.
        - switch_commande (list): List of packages to switch.

    Methods:
        - echo_settings(): Logs the current configuration settings for the KLauncher_rez instance.
        - eval_rez_command(): Executes the generated `rez` command to set up the environment.
```

## Git Commands

`k_launcher` also supports Git-related functionality for managing repositories, branches, and commits.


```text
Documentation for k_launcher Git Functionality:

Usage:
    python k_launcher_git.py [args*]

Arguments (args*):
    -i, --info : Display information about the tool.
    -p, --package : Load package.
    -co, --context : Display the current context.
    -gc, --git_clone : Clone a Git repository.
        Parameters:
            - URL of the repository.
            - Local folder to clone into.
            - Optional name for the repository folder.
    -gf, --git_fetch : Fetch the latest changes from the remote repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
    -gp, --git_pull : Update the repository by pulling the latest changes from the remote.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
    -ch, --git_check : Switch to a specific branch in the repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
            - Name of the branch to checkout.
    -c, --git_commit : Commit changes to the repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
            - Commit message.
    -cr, --git_create : Create a new branch in the specified repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
            - Name of the new branch.
    -gl, --git_list : List remote branches of the repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
    -log, --git_log : Display the commit log for the repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
    -t, --git_tag : Tag the repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
    -gh, --history : Display the history of the repository.
        Parameters:
            - Path to the local folder containing the repository.
            - Name of the repository.
    -pa, --path : Folder path argument.
    -gu, --git_url : Git URL for cloning.
    -b, --branch : Branch name.
    -m, --msg : Commit message.
    -vs, --vs_code : launch vs code with the path and package.

Description:
    The Git functionality of `k_launcher` is designed to simplify the process of managing Git repositories. 
    It provides commands for common Git operations such as cloning repositories, creating and switching branches, 
    and synchronizing with remote repositories. These commands help streamline version control tasks 
    within the context of a production pipeline.
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


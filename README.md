# K_launcher

## Table of Contents

- [Features](#Features)
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [Usage](#Usage)
- [License](#License)

`k_launcher` is a command-line utility designed for managing different configurations and launching DCC (Digital Content Creation) tools such as Maya, Houdini, and more, with custom environment settings and packages. The tool simplifies the process of working with different configurations, packages, and contexts.

## Features

- **Environment Management**: Manage and set up environment variables based on the selected configuration.
- **DCC Tool Launch**: Launch popular DCC tools like Maya, Houdini, and others with the correct configuration and environment setup.
- **Package Management**: Add and remove packages for DCC tools.
- **Context Management**: Save and load context configurations to resume workflows.

## Prerequisites

- `rez` package manager installed
- Required software installed (e.g., Maya, Houdini)
- Correct configuration files set up in the `CONTEXT` folder

## Installation

1. Ensure `rez` is installed and configured in your environment.
2. Clone the repository or copy the `k_launcher` tool to your local system.
3. Set up the `CONTEXT` folder with the necessary configuration files (e.g., `dev-k_config.rxt`, `main-k_config.rxt`).

## Usage

The `k_launcher` utility can be used from the command line to manage the environment and launch DCC tools. Below are the key commands:

### 1. Display Info

To display the documentation and available options for `k_launcher`:

```bash
rez env k_launcher -- run --info
```
```bash
This is the documentation for the k_launcher.

Usage:
   rez env k_launcher -- wrapper args*

arg:
   config : name of the config you working on.

args*:
   -package : package you are working on.
   -launch : launch the dcc with his default packages.
   -add : add packages.
   -save : save the context.
   -load : load the context.
   -info : listing of the options

launch command:
   rez env k_launcher -- run config ...
   rez env k_launcher -- run config value -pa package -add packages -save
   rez env k_launcher -- run config value -load value
   rez env k_launcher -- run config value -launch value
```

```bash
rez env k_launcher -- run --config dev -launch maya
```
Launch the DCC with the custom config

```bash
rez env k_launcher -- run --config <config_name> -save
```
This will save the context for the specified configuration.

```bash
rez env k_launcher -- run --config <config_name> -load <context_name>
```
This will load the environment context saved under <context_name> for the specified configuration.

```bash
rez env k_launcher -- run --config dev -launch maya -add myPackage
```
This will launch Maya with the dev configuration and add myPackage to the environment.

```bash
rez env k_launcher -- run --config dev -launch maya -add myPackage
rez env k_launcher -- run --config main -launch houdini
```
You can chain commands to launch different tools with their respective configurations:

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






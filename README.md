# CSE112-22 Assignment: Simple Assembler Simulator

This repository contains the framework for a simple Assembler and Simulator for a specified 16-bit ISA
Please **download the entire folder** and refrain from modifying the provided structure.  
Simply **add your files** in the appropriate directories and adjust the run files as necessary.

## Naming Convention

Ensure your source files follow this naming convention:  
- `SimpleAssembler`  
- `SimpleSimulator`  

Modify the run files within the **SimpleSimulator** and **SimpleAssembler** directories based on the programming language you choose.

## Run File Execution Instructions

All run files must be granted execution permissions before running them.

### Granting Execution Permission  
For Linux-based systems, navigate to the directory containing each run file using the terminal and run:  
```bash
chmod +x run

### Running the Assembler
To execute the assembler tests, navigate to the Automated Testing folder and open a terminal.
Assuming the necessary permissions have been granted, run:

```bash
./run --no-sim

### Running the Simulator
To execute the simulator tests, navigate to the Automated Testing folder and open a terminal.
Run the following command:

```bash
./run --no-asm

### Running Both Assembler and Simulator
To execute tests for both the assembler and simulator, navigate to the Automated Testing folder and open a terminal.
Run one of the following commands:

```bash
./run

For verbose output, use:

```bash
./run --verbose

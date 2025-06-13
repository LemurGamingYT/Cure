# Cure
A simple, performant programming language

Cure is a simple programming language that is designed to **bring many features from other languages so you won't need to relearn a whole new language from scratch, be fast, general purpose and safe**. The language compiles using LLVM offering **high performance**.

*Note that the language is only tested on Windows - Linux and Mac support should be tested soon (hopefully).*

---

### Features
- **Speed**: Due to Cure being compiled to LLVM, it is very fast at runtime.
- **Simplicity**: Cure is designed to be simple to use and learn.
- **Static typing**: Cure is statically typed meaning that the compiler will check for errors at compile time. Cure also has type inference on variables.
- **High level**: Cure is a high level language meaning that it is designed to be easy to use and understand.
- **Memory safety**: Cure uses simple reference counting to manage memory. No garbage collector to hinder performance.

---

### Running the language
1. Clone the repository
    - If you have the `git` cli tool, you can do this by running `git clone https://github.com/LemurGamingYT/Cure.git`
    - If you don't have `git`, then you can install the repository as a .zip by clicking the drop down menu: 'Code' and then 'Download ZIP'
2. Install Python (not needed if you use the .exe file)
    - Install Python 3.12.0 or higher: https://www.python.org/downloads/
    - During the setup, add Python to PATH and install pip and run the command: `pip install -r requirements`.txt in the directory you have downloaded this repository.
3. Install LLVM from https://releases.llvm.org/
4. Run the compiler
    - Add the 'bin' directory of the compiler to your PATH environment variable
    - Run the compiler using the command: `cure [actions] [options]`
    Use `cure -h` to see all available options

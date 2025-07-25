# Cure
 **The cure of programming**

Cure is a programming language that is designed to be **very easy-to-learn, fast, general purpose and safe**. The language compiles to C offering **high performance** and supports all features on Windows but **not Linux and Mac** currently.

---

## Features
- **Speed**: Due to Cure being compiled to C, it is very fast at runtime. It is also quite fast to compile.
- **Simplicity**: Cure is designed to be simple to use and learn.
- **Static typing**: Cure is statically typed meaning that the compiler will check for errors at compile time. Cure also has type inference on variables.
- **High level**: Cure is a high level language meaning that it is designed to be easy to use and understand. Even though it is a high level language, it still offers low level capabilities such as Pointers.
- **Memory safety**: Cure is designed to be fast and safe at the same time. Therefore, Cure does not use any garbage collection or reference counting and instead automatically inserts free calls where necessary in the generated C code.

---

## Running the language
1. Clone the repository
    - If you have the `git` command line tool, you can use that to install the repository using: `git clone https://github.com/LemurGamingYT1/Cure.git`
    - If you don't have `git`, then you can install the repository as a .zip by clicking the drop down menu: 'Code' and then 'Download ZIP'
2. Install Python (*not needed if you use the .exe file*)
    - Install Python 3.12.0 or higher: https://www.python.org/downloads/
    - During the setup, add Python to PATH and install pip and run the command: pip install -r requirements.txt in the directory you have downloaded this repository.
3. Install a C compiler
    - MinGW (gcc): https://sourceforge.net/projects/mingw/files/latest/download
    - LLVM (clang): https://github.com/llvm/llvm-project/releases
4. Install CMake and Ninja
    - Install CMake 3.10 or higher: https://cmake.org/download/
    - Install Ninja: https://ninja-build.org
5. Run the compiler
    - Add the 'bin' directory of the compiler to your PATH environment variable
    - Run the compiler using the command: `cure [actions] [options]`
    - Use `cure -h` to see all available options

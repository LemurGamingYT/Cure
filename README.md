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
2. Install Python
    - Install Python 3.12.0 or higher: https://www.python.org/downloads/
    - During the setup, add Python to PATH and install pip and run the command: `pip install -r requirements.txt` in the directory you have downloaded this repository.
3. Install LLVM from https://releases.llvm.org/
4. Run the compiler *Note this is not completely done yet*
    - Add the 'bin' directory of the compiler to your PATH environment variable
    - Run the compiler using the command: `cure [action] [options]`
    Use `cure -h` to see all available actions and options

### Overview
Here's an overview of Cure's current features! Once you're done here, why not look at some of the examples?

#### Basic Hello World
```
fn main() -> int {
    print("Hello world")
    return 0
}
```

#### Basic variables
```
fn main() -> int {
    x = 20
    print(x)
    return 0
}
```

#### Mutable variables
```
fn main() -> int {
    // Immutable by default
    x = 20
    // x = 10 // error: 'x' is immutable
    print(x)

    mut y = 20
    y = 10
    print(y)
    return 0
}
```

#### Control flow
```
fn main() -> int {
    is_18 = input("Are you 18+? ")
    if is_18 == "y" {
        print("You are an adult")
    } else {
        print("You are not an adult")
    }

    return 0
}
```

#### Iteration
```
fn main() -> int {
    loop_to = 1000000
    mut i = 0
    while i < loop_to {
        i = i + 1
    }

    print("Done")
    return 0
}
```

#### Functions
```
fn add(int a, int b) -> int {
    return a + b
}

fn main() -> int {
    print(add(2, 2))
    return 0
}
```

#### Mutable function parameters
```
fn test(mut int x) {
    // note that this does not change anything outside of this scope
    x = 50
}

fn main() -> int {
    x = 1
    print(x)

    test(x)

    print(x) // still 1, value has not changed
    return 0
}
```

#### Mathematical functions
```
fn main() -> int {
    print(Math.pi)
    print(Math.e)
    print(Math.ceil(3.4))
    print(Math.floor(2.6))
    print(Math.pow(10, 5))
    print(Math.sqrt(4))
    return 0
}
```

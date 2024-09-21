# TODOs
 TODOs for the Cure programming language

*as of v0.0.32*
- [ ] Fix nested arrays
- [ ] Support toplevel/global variables
- [ ] Support overloaded function modifications
- [ ] Functions
    - [ ] Anonymous functions: For example `print(func(int a) {
    print(a)
}(2))`
    - [x] Overloading
    - [x] Default Arguments
    - [ ] Variadic Functions
    - [x] Keyword Arguments
    - [x] Parameter references (actually just pointers)
    - [ ] Modifications (like Python decorators)
        - [x] Benchmark: Prints the time taken to execute a function when the function ends
        - [x] Cache: Cache function results
        - [ ] Timeout: Set a maximum execution time for the function
        - [ ] Validate: Check input parameters against specified conditions before executing the function
- [x] Dictionary type
- [x] Time functions
- [x] More math functions
- [x] More string attributes
- [ ] Import aliasing (use "abc" as abc): Alias the used library into an object that can be used like a class in the program.
- [ ] REPL (Read Eval Print Loop): For quick experimentation.
- [ ] Dependency Manager: Allow programmers to have a built-in dependency manager to manage bringing in packages.
    - [x] Use local files: Use not only libraries but other .cure files
- [ ] Array Comprehensions: Apply an expression to each element of an array
- [ ] Metaprogramming: Compile-time code generation capabilities
    - [ ] AST Manipulation: the ability to manipulate the IR/AST at compile time
    - [ ] Macros: Code transformation before compilation. For example `macro double(x) x*2
value = double(5) // Expands to 5*2`
- [ ] Error handling (try/catch): Catch runtime errors and handle them accordingly
- [ ] Coroutines and async/await: Asynchronous programming features for better concurrency handling
- [x] Enums: A simple way to define a set of named constants
- [ ] First class functions: Gives the ability to have functions as types
- [ ] 'extern' keyword: Allows the use of external functions from C
- [ ] Generic parameters: Every time a function with generic parameters is called, the compiler will define a new function for the new generic type. For example `func add[T](T a, T b) -> T {
    return a + b
}

print(func(8, 10)) // Generates add(int, int) -> int
print(func(5.7, 9)) // Generates add(float, int) -> float`
- [x] Casting: Convert a type to another type
- [ ] Libraries
    - [x] More File I/O functions
    - [ ] Buffer library: Fixed size arrays
    - [x] Big integers and floats
    - [ ] Language building library: Provides a way to build a language within the Cure language. Provides a configurable lexer, parser and visitor.
        - [ ] Regular Expressions: Regular expressions for pattern matching.
            - [x] Match
            - [x] Full match
            - [ ] Replace
            - [ ] Split
            - [ ] Find
            - [ ] Find All
            - [ ] Sub
            - [ ] RegexBuilder class: An interface for building regular expressions easier. Each attribute returns a new RegexBuilder object. For example: `pattern = RegexBuilder().start_of_line().digit().repeat(3).literal("-").digit().repeat(4).build()
if pattern.match("123-4567") {
    print("Valid")
}`
    - [ ] Command line parsing library: Parses command line arguments
    - [ ] Crypto library: Encryption, hashing, etc
    - [ ] LL library: Low level library for Cure
        - [x] Pointers: Allocate memory and deallocate memory
        - [x] Inline Assembly: Inline assembly code (not tested)
        - [x] Process manipulation: Read and write memory to processes
        - [ ] Memory Pool: Memory pool class for allocating chunks of memory efficiently, https://en.wikipedia.org/wiki/Memory_pool
        - [ ] Slab Allocator: A slab allocator for allocating memory, https://en.wikipedia.org/wiki/Slab_allocation
    - [ ] Windows API: Wrapper around the C `Windows.h` header
    - [ ] Http library: GET or POST requests and TCP/IP, UDP, sockets, etc
    - [ ] Text library: Text wrapping and locale
        - TODO: Fix
    - [ ] Compression library: RLE and other compression techniques
    - [x] Threading library: Thread code in different threads on the CPU
    - [ ] Language Interopability
        - [ ] Lua: Lua programming language bindings
        - [ ] Python: Python programming language bindings
    - [ ] Parsing library: Parsing of different kinds of information files
        - [x] JSON
        - [ ] XML
        - [ ] TOML
        - [ ] HTML
        - [ ] YAML
    - [ ] UI library: A library for creating user interfaces
        - [ ] Window, Button, Label and Frame
        - [ ] Textbox/Textarea, Slider, Checkbox, Radio buttons, Scrolling Frames, etc
        - [ ] Linux and Mac support
    - [ ] Testing functionality/framework: A library for testing code
    - [x] Iterables library: includes Stack and Linked List implementations
    - [x] Color library: RGB, HSV, etc with conversions between them
    - [x] Sound library: Low and high level sound control, gives control over low level things like sample rate or number of channels of a .wav file but also has high level functions like play
    - [x] Serialization library: Serialize objects
    - [ ] Machine learning library
        - [ ] Neural networks: Neural Network support for Cure
    - [ ] Sockets
- [ ] Classes defined by the programmer (not built-in)
    - [x] Class methods: Functions inside a class
    - [x] Class properties: Similar to variables but inside a class
    - [ ] Special class methods: Methods like to_string(), init(), type(), etc. Giving the programmer the ability to define how the compiler handles certain things to do with the custom class
        - [ ] Operator overloading: Define how operators work for a class
    - [ ] Inheritance: Classes inherit attributes, methods, etc from a parent class


Here are some places to get library, class and function ideas from:
https://github.com/vinta/awesome-python
https://github.com/JessicaBarclay/awesome-csharp
https://github.com/avelino/awesome-go
https://github.com/oz123/awesome-c
https://project-awesome.org/inputsh/awesome-c


Things to take a deeper look at:
General: http://p99.gforge.inria.fr/
General: http://attractivechaos.github.io/klib/#About
Deep Learning: https://pjreddie.com/darknet/
Neural Networks: https://github.com/codeplea/genann
Advanced Maths: https://github.com/ferreiradaselva/mathc

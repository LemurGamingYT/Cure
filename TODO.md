# TODOs
 TODOs for the Cure programming language

*as of v0.0.7*
- [ ] Strings
    - [ ] Fix strings
    - [ ] Implement string C struct
    - [ ] Different string types (probably in a strings library)
- [ ] Closure support
- [x] Fix nested arrays
- [x] Support toplevel/global variables
- [ ] Support overloaded function modifications
- [ ] Functions
    - [x] First class functions: Gives the ability to have functions as types (hopefully works)
    - [ ] Anonymous functions: Functions that are not named
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
- [ ] Import aliasing (`use "abc" as abc`): Alias the used library into an object that can be used like a class in the program.
- [ ] REPL (Read Eval Print Loop): For quick experimentation.
- [ ] Dependency Manager: Allow programmers to have a built-in dependency manager to manage bringing in packages.
    - [x] Use local files: Use not only libraries but other .cure files
- [ ] Array Comprehensions: Apply an expression to each element of an array
- [ ] Metaprogramming: Compile-time code generation capabilities
    - [ ] AST Manipulation: the ability to manipulate the IR/AST at compile time
    - [ ] Macros: Code transformation before compilation. For example `macro double(x) x*2
value = double(5) // Expands to 5*2`
- [ ] Coroutines and async/await: Asynchronous programming features for better concurrency handling
- [x] Enums: A simple way to define a set of named constants
- [ ] 'defer' keyword: Runs a function at the end of the function scope
- [ ] 'extern' keyword: Allows the use of external functions from C
    - [ ] Header libraries
    - [ ] Finish all headers
    - [ ] Allow inclusion of C files/headers
    - [ ] Windows API: Wrapper around the C `Windows.h` header from https://en.wikipedia.org/wiki/Windows.h
- [x] Type extensions: Add new methods to existing types
```
func int.hello() -> string {
    return "Hello"
}

x = 10
print(x.hello()) // Prints "Hello"
```
- [ ] Generic functions: Every time a function with generic parameters is called, the compiler will define a new function for the new generic type. For example `func add[T](T a, T b) -> T {
    return a + b
}

print(func(8, 10)) // Generates add(int, int) -> int
print(func(5.7, 9)) // Generates add(float, int) -> float`
    - [ ] Make the implementation better
- [x] Optionals: A type that can be either a value or nil. This is implemented as another type (needs more testing)
- [x] Casting: Convert a type to another type
- [ ] Libraries
    - [x] More File I/O functions
    - [x] Big integers and floats
    - [ ] Language building library: Provides a way to build a language within the Cure language. Provides a configurable lexer, parser and visitor.
        - [ ] Regular Expressions: Regular expressions for pattern matching.
            - [x] Match
            - [x] Full match
            - [ ] Search
            - [ ] Replace
            - [ ] Split
            - [ ] Find
            - [ ] Find All
            - [ ] Sub
            - [ ] RegexBuilder class: An interface for building regular expressions easier. Each attribute returns a new RegexBuilder object. For example: ```pattern = RegexBuilder().start_of_line().digit().repeat(3).literal("-").digit().repeat(4).build()
if pattern.match("123-4567") {
    print("Valid")
}```
    - [ ] Command line parsing library: Parses command line arguments
    - [ ] Crypto library: Encryption, hashing, etc
    - [ ] LL library: Low level library for Cure
        - [x] Pointers: Allocate memory and deallocate memory
        - [x] Inline Assembly: Inline assembly code (not tested)
        - [x] Process manipulation: Read and write memory to processes
        - [ ] Memory Pool: Memory pool class for allocating chunks of memory efficiently, https://en.wikipedia.org/wiki/Memory_pool
        - [ ] Allocators
            - [ ] Slab Allocator: A slab allocator for allocating memory, https://en.wikipedia.org/wiki/Slab_allocation
            - [ ] Page Allocator: The most basic allocator, whenever it makes an allocation it will ask the OS for entire pages of memory. This is of course fairly inefficient and slow.
            - [ ] Fixed Buffer Allocator: allocates memory into a fixed buffer and does not make any heap allocations. Very performant but requires you to know the size of the buffer ahead of time.
            - [ ] Arena Allocator: Takes in a child allocator and allocates memory multiply times but only free it once. This is useful for when you wish to allocate multiple things and free them all at once since they are all allocated in the same memory block.
            - [ ] General Purpose Allocator: a general purpose safe allocator that can be used for most cases. This is not the most performant or efficient allocator but it can be made much faster than the page allocator by turning off features such as thread safety and other safety checks.
            - [ ] C Allocator: A very high performance allocator with limited to no safety features. It will essentially call malloc and free from the C standard library, which basically removes the main benefit of using allocators which is no behind the scenes allocations and deallocations.
    - [ ] HTTP library: HTTP library for making HTTP requests
        - [ ] Interface for creating HTTP servers and Web applications
        - [ ] GET/POST HTTP(S) requests
        - [ ] Sockets: Sockets for networking
            - [ ] Incorporate tinycsocket library
    - [x] Text library: Text wrapping and locale
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
        - [ ] INI
            - [ ] Test
        - [ ] Markdown
    - [ ] UI library: A library for creating user interfaces
        - [ ] Window, Button, Label and Frame
        - [ ] Textbox/Textarea, Slider, Checkbox, Radio buttons, Scrolling Frames, etc
        - [ ] Linux and Mac support
    - [ ] Testing functionality/framework: A library for testing code
    - [x] Iterables library: includes Stack and Linked List implementations
        - [x] Buffer: Fixed size arrays
    - [x] Color library: RGB, HSV, etc with conversions between them
    - [ ] Sound library: Low and high level sound control, gives control over low level things like sample rate or number of channels of a .wav file but also has high level functions like play
    - [x] Serialization library: Serialize objects
    - [ ] Machine learning library: Machine learning for Cure
        - [ ] Neural networks: Neural Network support for Cure
- [ ] Classes defined by the programmer (not built-in)
    - [x] Class methods: Functions inside a class
    - [x] Class properties: Similar to variables but inside a class
    - [x] Special class methods: Methods like to_string(), init(), type(), etc. Giving the programmer the ability to define how the compiler handles certain things to do with the custom class
        - [x] Operator overloading: Define how operators work for a class
    - [x] Inheritance: Classes inherit attributes, methods, etc from a parent class (needs more testing)
    - [ ] Generic classes: Classes that can be used with any type
    - [ ] Interfaces: Classes that define a set of methods that a class must implement, it can also be used as a type. Create a struct in C and make the compiler check if the class implements the interface.
    - [ ] Static functions can't access other static functions or properties for some reason


Here are some places to get library, class and function ideas from:
https://github.com/vinta/awesome-python
https://github.com/JessicaBarclay/awesome-csharp
https://github.com/avelino/awesome-go
https://github.com/oz123/awesome-c
https://project-awesome.org/inputsh/awesome-c
https://pkg.go.dev/std


Things to take a deeper look at:
General: http://p99.gforge.inria.fr/
General: http://attractivechaos.github.io/klib/#About
Deep Learning: https://pjreddie.com/darknet/
Neural Networks: https://github.com/codeplea/genann
Advanced Maths: https://github.com/ferreiradaselva/mathc
Calling other languages into C: https://github.com/metacall/core
General: https://github.com/tboox/tbox/tree/master
GPU Rendering: https://github.com/recp/gpu
HTTP GET and POST: https://github.com/recp/http/tree/master
Images: https://github.com/libvips/libvips

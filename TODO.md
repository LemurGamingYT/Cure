# TODOs
 TODOs for the Cure programming language

*as of v0.0.1*
- [ ] Make the compiler use an AST instead of strings.
- [x] Fix the bug where the compiler inserts a free call at the end of a function that needs to be returned
- [ ] Fix nested call, e.g. `print(Math.max(Math.pow(Math.pow(6, 6)), Math.pow(10, 5))) // Maximum value of 6^6 and 10^5`
- [ ] **(possibly fixed)** Fix compiler free variables scoping issues
- [ ] Functions
    - [x] Overloading
    - [ ] Default Arguments
    - [ ] Variadic Functions
    - [x] Parameter references (actually just pointers)
    - [ ] Modifications (Python decorators): Such as a Warn modification that prints a warning at compile time
        - [x] Benchmark: Prints the time taken to execute a function when the function ends
        - [ ] Memoize: Cache function results
        - [ ] Timeout: Set a maximum execution time for the function
        - [ ] Validate: Check input parameters against specified conditions before executing the function
- [x] Dictionary type
- [x] Time functions
- [x] More math functions
- [x] More string attributes
- [ ] REPL (Read Eval Print Loop): For quick experimentation
- [ ] Dependency Manager: Allow programmers to have a built-in dependency manager to manage bringing in packages.
    - [ ] Use local files: Use not only libraries but other .cure files
- [ ] Iterative attribute apply operator: Applies an attribute to all elements in an array
- [ ] Metaprogramming: Compile-time code generation capabilities
- [ ] Coroutines and async/await: Asynchronous programming features for better concurrency handling.
- [ ] Libraries
    - [x] More File I/O functions
    - [ ] Buffer library
    - [x] Big integers and floats
    - [ ] Language building library
        - [ ] Regular Expressions
    - [ ] Command line parsing library
    - [ ] Crypto library: Encryption, hashing, etc
    - [ ] Add more low level functionality to the 'LL' library (such as memory pools, reading and writing from registers, inlining assembly and system call interfaces)
    - [ ] Windows API: Wrapper around the C `Windows.h` header
    - [ ] Http library (GET or POST requests and TCP/IP, UDP, etc sockets)
    - [x] Text library (text wrapping and locale)
    - [ ] Compression library: RLE and other compression techniques
    - [x] Threading library: Thread code in different threads on the CPU
    - [ ] Parsing library
        - [ ] JSON
        - [ ] XML
        - [ ] TOML
        - [ ] HTML
        - [ ] YAML
    - [ ] UI library
        - [x] Window, Button, Label and Frame
        - [ ] Textbox/Textarea, Slider, Checkbox, Radio buttons, Scrolling Frames, etc
        - [ ] Linux and Mac support
    - [ ] Testing functionality/framework
    - [x] Iterables library: includes Stack and Linked List implementations
    - [x] Color library: RGB, HSV, etc with conversions between them
    - [x] Sound library: Low and high level sound control, gives control over low level things like sample rate or number of channels of a .wav file but also has high level functions like play
    - [ ] Serialization library: Serialize objects
- [ ] Classes defined by the programmer (not built-in)
    - [ ] Special class methods: Methods like to_string(), init(), type(), etc. Giving the programmer the ability to define how the compiler handles certain things to do with the custom class
    - [ ] Operator overloading: Define how operators work for a class
    - [ ] Inheritance: Classes inherit attributes, methods, etc from a parent class


Here are some places to get library, class and function ideas from:
https://github.com/vinta/awesome-python
https://github.com/JessicaBarclay/awesome-csharp
https://github.com/avelino/awesome-go
https://github.com/oz123/awesome-c

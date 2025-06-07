from typing import Any

from llvmlite import ir


def NULL():
    return ir.Constant(ir.IntType(8).as_pointer(), None) # void*

def store_in_pointer(builder: ir.IRBuilder, type: ir.Type, value: ir.Value):
    """Stores a value in as a pointer"""
    ptr = builder.alloca(type)
    builder.store(value, ptr)
    return ptr


def get_or_add_global(module: ir.Module, name: str, global_value: Any):
    """Gets or adds a global value"""
    if name in module.globals:
        return module.get_global(name)
    
    module.add_global(global_value)
    return global_value


def max_value(type: ir.IntType):
    return 2 ** type.width

def min_value(type: ir.IntType):
    return -(2 ** type.width - 1)


def create_identified_struct_type(context: ir.Context, name: str,
                                  field_types: list[ir.Type] | None = None):
    """Create an identified (named) struct type"""
    struct_type = context.get_identified_type(name)
    if field_types:
        struct_type.set_body(*field_types)
    
    return struct_type

def set_struct_body(struct_type: ir.IdentifiedStructType, field_types: list[ir.Type]):
    """Set the body of an identified struct type"""
    struct_type.set_body(*field_types)

def create_recursive_struct(context: ir.Context, name: str, field_types: list[ir.Type], 
                           self_ref_indices: list[int]):
    """Create a struct that can reference itself
    
    Args:
        context: LLVM context
        name: Struct name
        field_types: List of field types (use None for self-reference positions)
        self_ref_indices: Indices where self-references should be placed
    """
    struct_type = context.get_identified_type(name)
    
    # Replace None entries with self-pointer references
    final_types = []
    for i, field_type in enumerate(field_types):
        if i in self_ref_indices:
            final_types.append(struct_type.as_pointer())
        else:
            final_types.append(field_type)
    
    struct_type.set_body(*final_types)
    return struct_type


def declare_malloc(module: ir.Module) -> ir.Function:
    """Declare malloc function: void* malloc(size_t size)"""
    size_t = ir.IntType(64)  # Assuming 64-bit size_t
    void_ptr = ir.IntType(8).as_pointer()
    malloc_type = ir.FunctionType(void_ptr, [size_t])
    
    if 'malloc' not in module.globals:
        malloc_func = ir.Function(module, malloc_type, name='malloc')
        malloc_func.linkage = 'external'
        return malloc_func
    
    return module.get_global('malloc')

def declare_free(module: ir.Module) -> ir.Function:
    """Declare free function: void free(void* ptr)"""
    void_ptr = ir.IntType(8).as_pointer()
    void_type = ir.VoidType()
    free_type = ir.FunctionType(void_type, [void_ptr])
    
    if 'free' not in module.globals:
        free_func = ir.Function(module, free_type, name='free')
        free_func.linkage = 'external'
        return free_func
    
    return module.get_global('free')

def declare_calloc(module: ir.Module) -> ir.Function:
    """Declare calloc function: void* calloc(size_t num, size_t size)"""
    size_t = ir.IntType(64)
    void_ptr = ir.IntType(8).as_pointer()
    calloc_type = ir.FunctionType(void_ptr, [size_t, size_t])
    
    if 'calloc' not in module.globals:
        calloc_func = ir.Function(module, calloc_type, name='calloc')
        calloc_func.linkage = 'external'
        return calloc_func
    
    return module.get_global('calloc')

def declare_realloc(module: ir.Module) -> ir.Function:
    """Declare realloc function: void* realloc(void* ptr, size_t size)"""
    size_t = ir.IntType(64)
    void_ptr = ir.IntType(8).as_pointer()
    realloc_type = ir.FunctionType(void_ptr, [void_ptr, size_t])
    
    if 'realloc' not in module.globals:
        realloc_func = ir.Function(module, realloc_type, name='realloc')
        realloc_func.linkage = 'external'
        return realloc_func
    
    return module.get_global('realloc')

def heap_malloc(module: ir.Module, builder: ir.IRBuilder, size: ir.Value) -> ir.Value:
    """Allocate memory on heap using malloc"""
    malloc_func = declare_malloc(module)
    # Convert size to size_t (64-bit) if needed
    if size.type != ir.IntType(64):
        size = builder.zext(size, ir.IntType(64))
    
    return builder.call(malloc_func, [size])

def heap_calloc(module: ir.Module, builder: ir.IRBuilder, num: ir.Value, size: ir.Value) -> ir.Value:
    """Allocate zero-initialized memory on heap using calloc"""
    calloc_func = declare_calloc(module)
    # Convert to size_t (64-bit) if needed
    if num.type != ir.IntType(64):
        num = builder.zext(num, ir.IntType(64))
    if size.type != ir.IntType(64):
        size = builder.zext(size, ir.IntType(64))
    
    return builder.call(calloc_func, [num, size])

def heap_realloc(module: ir.Module, builder: ir.IRBuilder, ptr: ir.Value, size: ir.Value) -> ir.Value:
    """Reallocate memory on heap using realloc"""
    realloc_func = declare_realloc(module)
    # Convert size to size_t (64-bit) if needed
    if size.type != ir.IntType(64):
        size = builder.zext(size, ir.IntType(64))
    
    # Cast pointer to void* if needed
    void_ptr = ir.IntType(8).as_pointer()
    if ptr.type != void_ptr:
        ptr = builder.bitcast(ptr, void_ptr)
    
    return builder.call(realloc_func, [ptr, size])

def heap_free(module: ir.Module, builder: ir.IRBuilder, ptr: ir.Value) -> None:
    """Free heap memory using free"""
    free_func = declare_free(module)
    # Cast pointer to void* if needed
    void_ptr = ir.IntType(8).as_pointer()
    if ptr.type != void_ptr:
        ptr = builder.bitcast(ptr, void_ptr)
    
    builder.call(free_func, [ptr])

def heap_malloc_type(module: ir.Module, builder: ir.IRBuilder, type: ir.Type,
                     count: ir.Value = None) -> ir.Value:
    """Allocate memory for a specific type on heap"""
    type_size = ir.Constant(ir.IntType(64), type.get_abi_size(module.data_layout))
    if count is None:
        # Allocate for single instance
        size = type_size
    else:
        # Allocate for array
        if count.type != ir.IntType(64):
            count = builder.zext(count, ir.IntType(64))
        
        size = builder.mul(type_size, count)
    
    void_ptr = heap_malloc(module, builder, size)
    return builder.bitcast(void_ptr, type.as_pointer())

def heap_calloc_type(module: ir.Module, builder: ir.IRBuilder, type: ir.Type,
                     count: ir.Value) -> ir.Value:
    """Allocate zero-initialized memory for a specific type on heap"""
    type_size = ir.Constant(ir.IntType(64), type.get_abi_size(module.data_layout))
    
    if count.type != ir.IntType(64):
        count = builder.zext(count, ir.IntType(64))
    
    void_ptr = heap_calloc(module, builder, count, type_size)
    return builder.bitcast(void_ptr, type.as_pointer())

def heap_malloc_struct(module: ir.Module, builder: ir.IRBuilder, struct_type: ir.Type,
                       count: ir.Value = None) -> ir.Value:
    """Allocate memory for struct(s) on heap"""
    return heap_malloc_type(module, builder, struct_type, count)

def heap_malloc_array(module: ir.Module, builder: ir.IRBuilder, element_type: ir.Type,
                      count: ir.Value) -> ir.Value:
    """Allocate memory for an array on heap"""
    return heap_malloc_type(module, builder, element_type, count)

def heap_realloc_array(module: ir.Module, builder: ir.IRBuilder, ptr: ir.Value, element_type: ir.Type,
                       new_count: ir.Value) -> ir.Value:
    """Reallocate array memory on heap"""
    type_size = ir.Constant(ir.IntType(64), element_type.get_abi_size(module.data_layout))
    
    if new_count.type != ir.IntType(64):
        new_count = builder.zext(new_count, ir.IntType(64))
    
    new_size = builder.mul(type_size, new_count)
    void_ptr = heap_realloc(module, builder, ptr, new_size)
    return builder.bitcast(void_ptr, element_type.as_pointer())

def heap_malloc_string(module: ir.Module, builder: ir.IRBuilder, length: ir.Value) -> ir.Value:
    """Allocate memory for a string (char array) on heap"""
    char_type = ir.IntType(8)
    # Add 1 for null terminator
    one = ir.Constant(ir.IntType(64), 1)
    if length.type != ir.IntType(64):
        length = builder.zext(length, ir.IntType(64))
    
    size_with_null = builder.add(length, one)
    return heap_malloc_type(module, builder, char_type, size_with_null)

def is_null_ptr(builder: ir.IRBuilder, ptr: ir.Value) -> ir.Value:
    """Check if pointer is null"""
    null_ptr = ir.Constant(ptr.type, None)
    return builder.icmp_unsigned('==', ptr, null_ptr)


def create_struct_type(field_types: list[ir.Type], packed: bool = False):
    """Create a struct type from field types"""
    return ir.LiteralStructType(field_types, packed)

def create_struct_value(builder: ir.IRBuilder, struct_type: ir.Type, field_values: list[ir.Value]):
    """Create a struct value from field values"""
    struct_val = ir.Constant(struct_type, ir.Undefined)
    for i, field_val in enumerate(field_values):
        struct_val = builder.insert_value(struct_val, field_val, i)
    
    return struct_val

def allocate_struct(builder: ir.IRBuilder, struct_type: ir.Type, name: str = ''):
    """Allocate space for a struct on the stack"""
    return builder.alloca(struct_type, name=name)

def get_struct_field_ptr(builder: ir.IRBuilder, struct: ir.Value, field_index: int):
    """Get pointer to a struct field"""
    zero = ir.Constant(ir.IntType(32), 0)
    field_idx = ir.Constant(ir.IntType(32), field_index)
    return builder.gep(struct, [zero, field_idx])

def get_struct_field_value(builder: ir.IRBuilder, struct: ir.Value, field_index: int):
    """Extract a field value from a struct value"""
    return builder.extract_value(struct, field_index)

def set_struct_field(builder: ir.IRBuilder, struct: ir.Value, field_index: int, value: ir.Value):
    """Set a field in a struct (struct must be allocated)"""
    ptr = get_struct_field_ptr(builder, struct, field_index)
    builder.store(value, ptr)


def create_string_constant(module: ir.Module, text: str, name: str = ''):
    """Create a global string constant and return pointer to it"""
    if not text.endswith('\0'):
        text += '\0'
    
    const_type = ir.ArrayType(ir.IntType(8), len(text))
    const = ir.GlobalVariable(module, const_type, name or module.get_unique_name('str'))
    const.initializer = ir.Constant(const_type, bytearray(text.encode('utf-8')))
    const.global_constant = True
    const.linkage = 'internal'
    
    zero = ir.Constant(ir.IntType(32), 0)
    return ir.Constant.gep(const, [zero, zero])

def create_string_struct(module: ir.Module, builder: ir.IRBuilder, text: str, 
                        name: str = "") -> ir.Value:
    """Create a string struct {i8*, i64} with pointer and length"""
    str_ptr = create_string_constant(module, text, name)
    length = ir.Constant(ir.IntType(64), len(text))
    
    string_type = ir.LiteralStructType([ir.IntType(8).as_pointer(), ir.IntType(64)])
    return create_struct_value(builder, string_type, [str_ptr, length])

def allocate_string(builder: ir.IRBuilder, name: str = "") -> ir.Value:
    """Allocate space for a string struct on the stack"""
    string_type = ir.LiteralStructType([ir.IntType(8).as_pointer(), ir.IntType(64)])
    return builder.alloca(string_type, name=name)


def create_buffer(builder: ir.IRBuilder, element_type: ir.Type, size: int, 
                 name: str = "") -> ir.Value:
    """Create a buffer (array) on the stack"""
    array_type = ir.ArrayType(element_type, size)
    return builder.alloca(array_type, name=name)

def create_buffer_ptr(builder: ir.IRBuilder, element_type: ir.Type, size: int, 
                     name: str = "") -> ir.Value:
    """Create a buffer and return pointer to first element"""
    buffer = create_buffer(builder, element_type, size, name)
    return builder.bitcast(buffer, element_type.as_pointer())

def get_buffer_element_ptr(builder: ir.IRBuilder, buffer_ptr: ir.Value, 
                          index: ir.Value) -> ir.Value:
    """Get pointer to buffer element at index"""
    return builder.gep(buffer_ptr, [index])

def set_buffer_element(builder: ir.IRBuilder, buffer_ptr: ir.Value, 
                      index: ir.Value, value: ir.Value) -> None:
    """Set buffer element at index"""
    element_ptr = get_buffer_element_ptr(builder, buffer_ptr, index)
    builder.store(value, element_ptr)

def get_buffer_element(builder: ir.IRBuilder, buffer_ptr: ir.Value, 
                      index: ir.Value) -> ir.Value:
    """Get buffer element at index"""
    element_ptr = get_buffer_element_ptr(builder, buffer_ptr, index)
    return builder.load(element_ptr)

def create_static_buffer(module: ir.Module, element_type: ir.Type, size: int, name = ''):
    buf_type = ir.ArrayType(element_type, size)
    buf = ir.GlobalVariable(module, buf_type, name or module.get_unique_name())
    buf.initializer = ir.Constant(buf_type, None)
    buf.linkage = 'internal'

    zero = ir.Constant(ir.IntType(32), 0)
    return ir.Constant.gep(buf, [zero, zero])


def create_ternary(builder: ir.IRBuilder, condition: ir.Value, 
                  true_val: ir.Value, false_val: ir.Value) -> ir.Value:
    """Create ternary operator: condition ? true_val : false_val"""
    return builder.select(condition, true_val, false_val)

class IfBuilder:
    """Helper class for building if-elif-else chains"""
    
    def __init__(self, builder: ir.IRBuilder, condition: ir.Value):
        self.builder = builder
        self.function = builder.function
        self.conditions = [condition]
        self.blocks = []
        self.else_block = None
        self.merge_block = None
        self.phi_values: list[Any] = []
        self.phi_blocks: list[Any] = []
        
        # Create initial blocks
        self.then_block = self.function.append_basic_block('if_then')
        self.blocks.append(self.then_block)
        
    def elif_(self, condition: ir.Value) -> 'IfBuilder':
        """Add an elif condition"""
        self.conditions.append(condition)
        elif_block = self.function.append_basic_block(f'elif_{len(self.blocks)}')
        self.blocks.append(elif_block)
        return self
    
    def else_(self) -> 'IfBuilder':
        """Add else block"""
        self.else_block = self.function.append_basic_block('else')
        return self
    
    def build(self, then_func, *elif_funcs, else_func=None):
        """Build the if-elif-else chain
        
        Args:
            then_func: Function to call for if block
            elif_funcs: Functions to call for elif blocks  
            else_func: Function to call for else block
        """
        # Create all blocks first
        self.blocks = []
        for i in range(len(self.conditions)):
            self.blocks.append(self.function.append_basic_block(f'if_then_{i}'))
        
        if else_func:
            self.else_block = self.function.append_basic_block('if_else')
        
        self.merge_block = self.function.append_basic_block('if_merge')
        
        # Save current block
        current_block = self.builder.block
        
        # Build the condition chain
        self.builder.position_at_end(current_block)
        self._build_condition_chain()
        
        # Build then block
        self.builder.position_at_end(self.blocks[0])
        then_result = then_func(self.builder)
        if then_result is not None:
            self.phi_values.append(then_result)
            self.phi_blocks.append(self.builder.block)
        
        # CRITICAL: Only add branch if block isn't already terminated
        if not self.builder.block.is_terminated:
            self.builder.branch(self.merge_block)
        
        # Build elif blocks
        for i, elif_func in enumerate(elif_funcs):
            if i + 1 < len(self.blocks):
                self.builder.position_at_end(self.blocks[i + 1])
                elif_result = elif_func(self.builder)
                if elif_result is not None:
                    self.phi_values.append(elif_result)
                    self.phi_blocks.append(self.builder.block)
                
                # Only add branch if not terminated
                if not self.builder.block.is_terminated:
                    self.builder.branch(self.merge_block)
        
        # Build else block
        if self.else_block and else_func:
            self.builder.position_at_end(self.else_block)
            else_result = else_func(self.builder)
            if else_result is not None:
                self.phi_values.append(else_result)
                self.phi_blocks.append(self.builder.block)
            
            # Only add branch if not terminated
            if not self.builder.block.is_terminated:
                self.builder.branch(self.merge_block)
        
        # Position at merge block
        self.builder.position_at_end(self.merge_block)
        
        # Create phi node if there are return values
        if self.phi_values:
            phi = self.builder.phi(self.phi_values[0].type)
            for val, block in zip(self.phi_values, self.phi_blocks):
                phi.add_incoming(val, block)
            return phi
        
        return None

def create_if_else(builder: ir.IRBuilder, condition: ir.Value, 
                  then_func, else_func=None):
    """Simple if-else helper
    
    Args:
        builder: IR builder
        condition: Boolean condition
        then_func: Function to call for then block: then_func(builder) -> Optional[ir.Value]
        else_func: Function to call for else block: else_func(builder) -> Optional[ir.Value]
    """
    function = builder.function
    then_block = function.append_basic_block('then')
    else_block = function.append_basic_block('else') if else_func else None
    merge_block = function.append_basic_block('merge')
    
    # Branch on condition
    if else_block:
        builder.cbranch(condition, then_block, else_block)
    else:
        builder.cbranch(condition, then_block, merge_block)
    
    # Then block
    builder.position_at_end(then_block)
    then_result = then_func(builder)
    then_end_block = builder.block
    builder.branch(merge_block)
    
    # Else block
    else_result = None
    else_end_block = None
    if else_block and else_func:
        builder.position_at_end(else_block)
        else_result = else_func(builder)
        else_end_block = builder.block
        builder.branch(merge_block)
    
    # Merge block
    builder.position_at_end(merge_block)
    
    # Create phi node if both branches return values
    if then_result is not None and else_result is not None:
        phi = builder.phi(then_result.type)
        phi.add_incoming(then_result, then_end_block)
        phi.add_incoming(else_result, else_end_block)
        return phi
    elif then_result is not None:
        return then_result
    elif else_result is not None:
        return else_result
    
    return None


def create_while_loop(builder: ir.IRBuilder, condition_func, body_func):
    """Create a while loop"""
    
    function = builder.function
    
    # Create blocks
    condition_block = function.append_basic_block('while_condition')
    body_block = function.append_basic_block('while_body')
    exit_block = function.append_basic_block('while_exit')
    
    # Jump to condition block (only if current block isn't terminated)
    if not builder.block.is_terminated:
        builder.branch(condition_block)
    
    # Condition block
    builder.position_at_end(condition_block)
    condition = condition_func(builder)
    
    # Only add cbranch if the block isn't already terminated
    if not builder.block.is_terminated:
        builder.cbranch(condition, body_block, exit_block)
    
    # Body block
    builder.position_at_end(body_block)
    body_func(builder)
    
    # Loop back to condition (only if not terminated)
    if not builder.block.is_terminated:
        builder.branch(condition_block)
    
    # Exit block - position builder here for continuation
    builder.position_at_end(exit_block)

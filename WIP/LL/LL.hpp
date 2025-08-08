#pragma once

#include "builtins/builtins.hpp"


template<typename T>
class Pointer {
    T* ptr;
public:
    Pointer(T* ptr = nullptr) : ptr(ptr) {}

    T get() const noexcept { return *ptr; }
    nil set(T value) noexcept {
        *ptr = value;
        return nil();
    }

    nil free() const {
        delete ptr;
        return nil();
    }
};

template<typename T>
string Pointer_to_string(Pointer<T> ptr) {
    return "Pointer(" + to_string(ptr.get()) + ")";
}

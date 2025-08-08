#pragma once

#include "builtins/builtins.hpp"

#include <stack>


template<typename T>
class Stack : public std::stack<T> {
public:
    Stack(std::initializer_list<T> l) : std::stack<T>(l) {}
    Stack() : std::stack<T>() {}

    // push, pop and top are defined in std::stack

    T peek(int n = 0) const {
        std::stack<T> copy = *this;
        for (int i = 0; i < n; i++) {
            copy.pop();
        }

        return copy.top();
    }

    nil clear() {
        this->c.clear();
        return nil();
    }


    int length() const { return this->size(); }
    bool is_empty() const { return length() == 0; }
};

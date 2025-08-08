#pragma once

#include "builtins/builtins.hpp"

#include <list>


template<typename T>
class LinkedList : public std::list<T> {
public:
    LinkedList(std::initializer_list<T> l) : std::list<T>(l) {}
    LinkedList() {}

    nil add_back(T value) {
        this->push_back(value);
        return nil();
    }

    nil add_front(T value) {
        this->push_front(value);
        return nil();
    }

    nil add_after(int index, T value) {
        auto it = this->begin();
        std::advance(it, index);
        this->insert(it, value);
        return nil();
    }

    nil add_before(int index, T value) {
        auto it = this->begin();
        std::advance(it, index);
        this->insert(it, value);
        return nil();
    }

    T get(int index) const {
        auto it = this->begin();
        std::advance(it, index);
        return *it;
    }

    nil remove(T value) {
        this->remove(value);
        return nil();
    }

    nil remove_at(int index) {
        auto it = this->begin();
        std::advance(it, index);
        this->erase(it);
        return nil();
    }

    // clear is part of std::list


    int length() const { return this->size(); }
    bool is_empty() const { return length() == 0; }
};

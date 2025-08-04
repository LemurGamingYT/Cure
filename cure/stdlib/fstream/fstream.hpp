#pragma once

#include "builtins/builtins.hpp"

#include <filesystem>
#include <fstream>


class File {
public:
    std::filesystem::path path;

    File(string filename) : path(std::filesystem::path(filename.c_str())) { }

    string to_string() const { return "File('" + path.string() + "')"; }
    string contents() {
        std::ifstream file(path.string());
        string result;
        result.assign((std::istreambuf_iterator<char>(file)),
                      (std::istreambuf_iterator<char>()));
        return result;
    }

    nil write(string content) {
        std::ofstream file(path.string());
        file << content;
        return nil();
    }

    bool exists() {
        return std::filesystem::exists(path);
    }
};

string to_string(const File& file) { return file.to_string(); }

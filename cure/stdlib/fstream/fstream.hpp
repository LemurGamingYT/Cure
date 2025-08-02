#pragma once

#include "builtins/builtins.hpp"

#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;


class File {
public:
    fs::path path;

    File(string filename) : path(fs::path(filename.c_str())) { }

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
        return fs::exists(path);
    }

    static bool exists(string filename) {
        return fs::exists(fs::path(filename.c_str()));
    }
};

string to_string(const File& file) { return file.to_string(); }

#pragma once

#include "builtins/builtins.hpp"

#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;


class File {
public:
    fs::path path;
    
    File(const string& filename) : path(fs::path(filename.c_str())) {}

    bool exists() const { return fs::exists(path); }
    string extension() const { return path.extension().string(); }
    string name() const { return path.filename().string(); }
    string stem() const { return path.stem().string(); }
    int size() const { return fs::file_size(path); }
    File absolute() const { return File{fs::absolute(path).string()}; }
    File relative_to(const string& other) const { return File{
        fs::relative(path, fs::path(other.c_str())).string()
    }; }
    File relative_to(const File& other) const { return File{fs::relative(path, other.path).string()}; }
    bool is_file() const { return fs::is_regular_file(path); }
    bool is_dir() const { return fs::is_directory(path); }
    bool is_link() const { return fs::is_symlink(path); }
    string contents() const {
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

    nil create() {
        std::ofstream file(path.string());
        return nil();
    }

    nil mkdir() {
        fs::create_directory(path);
        return nil();
    }

    nil remove() {
        fs::remove(path);
        return nil();
    }

    nil rmdir() {
        fs::remove(path);
        return nil();
    }

    nil rename(const string& new_path) {
        fs::rename(path, fs::path(new_path.c_str()));
        return nil();
    }

    nil rename(const File& new_path) {
        fs::rename(path, new_path.path);
        return nil();
    }
};

string to_string(const File& file) { return "File('" + file.path.string() + "')"; }

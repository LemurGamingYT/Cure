#pragma once

#include <builtins/builtins.hpp>


static const char* table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static const char* table_url = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

static string encode(const string& data, bool url_safe = false) {
    const char* map = url_safe ? table_url : table;

    std::string out;
    out.reserve(((data.length() + 2) / 3) * 4);

    size_t i = 0;
    while (i + 2 < data.length()) {
        uint32_t triple = (uint32_t(data[i]) << 16) | (uint32_t(data[i+1]) << 8) | uint32_t(data[i+2]);
        out.push_back(map[(triple >> 18) & 0x3F]);
        out.push_back(map[(triple >> 12) & 0x3F]);
        out.push_back(map[(triple >> 6) & 0x3F]);
        out.push_back(map[triple & 0x3F]);
        i += 3;
    }

    if (i < data.length()) {
        uint32_t triple = uint32_t(data[i]) << 16;
        out.push_back(map[(triple >> 18) & 0x3F]);

        if (i + 1 < data.length()) {
            triple |= uint32_t(data[i+1]) << 8;
            out.push_back(map[(triple >> 12) & 0x3F]);
            out.push_back(map[(triple >> 6) & 0x3F]);
            out.push_back('=');
        } else {
            out.push_back(map[(triple >> 12) & 0x3F]);
            out.push_back('=');
            out.push_back('=');
        }
    }

    return out;
}

static array<int> decode(const string& b64) {
    static int8_t rev[256];
    static bool initialized = false;
    if (!initialized) {
        for (int i = 0; i < 256; ++i) rev[i] = -1;
        for (int i = 0; i < 64; ++i) rev[static_cast<int>(table[i])] = i;
        // URL-safe variants
        rev[static_cast<int>('-')] = rev[static_cast<int>('A')]; // temporarily unused
        rev[static_cast<int>('_')] = rev[static_cast<int>('A')];
        initialized = true;
    }

    array<int> out;
    out.reserve((b64.size() * 3) / 4);

    uint32_t buffer = 0;
    int bits_collected = 0;
    size_t padding_count = 0;

    auto decode_val = [&](int ch) -> int {
        if (ch == '=') return -2; // padding
        // handle URL-safe characters
        if (ch == '-') return 62; // '-'' maps to 62 in URL-safe
        if (ch == '_') return 63; // '_' maps to 63 in URL-safe
        int8_t v = rev[ch];
        return v;
    };

    for (size_t i = 0; i < b64.size(); ++i) {
        int ch = static_cast<int>(b64[i]);
        if (isspace(ch)) continue; // ignore whitespace
        int val = decode_val(ch);
        if (val == -2) {
            // padding: stop reading further non-space chars except additional padding
            ++padding_count;
            // Each padding char contributes 0 bits; we break if padding is followed by non-padding non-space
            // But we must still allow trailing whitespace and '=' signs.
            continue;
        }

        if (val < 0) {
            error("Invalid character in Base64 string");
        }

        if (padding_count) {
            // we saw padding earlier but now another non-padding character -> invalid
            error("Invalid padding in Base64 string");
        }

        buffer = (buffer << 6) | uint32_t(val);
        bits_collected += 6;
        if (bits_collected >= 8) {
            bits_collected -= 8;
            uint8_t byte = static_cast<uint8_t>((buffer >> bits_collected) & 0xFF);
            out.push_back(byte);
        }
    }

    // Handle padding at end (if exists)
    // Count actual '=' at end (ignoring whitespace)
    size_t tail_eq = 0;
    for (size_t i = b64.size(); i > 0; --i) {
        int ch = static_cast<int>(b64[i-1]);
        if (isspace(ch)) continue;
        if (ch == '=') ++tail_eq; else break;
    }

    if (tail_eq > 2) error("Too much padding in Base64 string");

    // If there was padding, we must trim corresponding bytes from the end
    if (tail_eq) {
        if (out.size() < tail_eq) error("Invalid padding resulting in negative length");
        out.resize(out.size() - tail_eq);
    }

    return out;
}

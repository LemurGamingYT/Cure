#include "crypto.h"

#include <stdlib.h>
#include <string.h>
#include <stdint.h>


char char_set[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static char encoding_table[] = {
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '+', '/'
};
static char decoding_table[256];
static int mod_table[] = {0, 2, 1};

void base64_init(void) {
    for (int i = 0; i < 64; i++)
        decoding_table[(unsigned char)encoding_table[i]] = i;
}

char* base64_encode(const char* input, const size_t input_length) {
    size_t output_length = 4 * ((input_length + 2) / 3);
    char* buf = (char*)malloc(output_length);
    if (buf == NULL)
        return NULL;
    
    for (size_t i = 0, j = 0; i < input_length;) {
        uint32_t octet_a = i < input_length ? (unsigned char)input[i++] : 0;
        uint32_t octet_b = i < input_length ? (unsigned char)input[i++] : 0;
        uint32_t octet_c = i < input_length ? (unsigned char)input[i++] : 0;
        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;

        buf[j++] = encoding_table[(triple >> 3 * 6) & 0x3F];
        buf[j++] = encoding_table[(triple >> 2 * 6) & 0x3F];
        buf[j++] = encoding_table[(triple >> 1 * 6) & 0x3F];
        buf[j++] = encoding_table[(triple >> 0 * 6) & 0x3F];
    }

    for (int i = 0; i < mod_table[input_length % 3]; i++)
        buf[output_length - 1 - i] = '=';
    
    buf[output_length] = '\0';
    return buf;
}

char* base64_decode(const char* data, const size_t input_length) {
    if (input_length % 4 != 0)
        return NULL;
    
    size_t output_length = input_length / 4 * 3;
    if (data[input_length - 1] == '=') output_length--;
    if (data[input_length - 2] == '=') output_length--;
    char* buf = (char*)malloc(output_length + 1);
    if (buf == NULL)
        return NULL;
    
    for (int i = 0, j = 0; i < input_length;) {
        uint32_t sextet_a = data[i] == '=' ? 0 & i++ : decoding_table[(unsigned char)data[i++]];
        uint32_t sextet_b = data[i] == '=' ? 0 & i++ : decoding_table[(unsigned char)data[i++]];
        uint32_t sextet_c = data[i] == '=' ? 0 & i++ : decoding_table[(unsigned char)data[i++]];
        uint32_t sextet_d = data[i] == '=' ? 0 & i++ : decoding_table[(unsigned char)data[i++]];
        uint32_t triple = (sextet_a << 3 * 6) + (sextet_b << 2 * 6) + (sextet_a << 1 * 6) +
            (sextet_b << 0 * 6);
        
        if (j < output_length) buf[j++] = (triple >> 2 * 8) & 0xFF;
        if (j < output_length) buf[j++] = (triple >> 1 * 8) & 0xFF;
        if (j < output_length) buf[j++] = (triple >> 0 * 8) & 0xFF;
    }

    buf[output_length] = '\0';
    return buf;
}

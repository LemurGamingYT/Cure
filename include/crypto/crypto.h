#ifndef CRYPTO_H
#define CRYPTO_H


#include <stddef.h>


void base64_init(void);
char* base64_encode(const char* input, size_t input_length);
char* base64_decode(const char* data, size_t input_length);

char* AES_encrypt(void* buffer, size_t buffer_length, char* IV, char* key, size_t key_length);
char* AES_decrypt(void* buffer, size_t buffer_length, char* IV, char* key, size_t key_length);

char* SHA1(const char* input, size_t input_length);
char* SHA256(const char* input, size_t input_length);

char* RSA_generate_key(size_t key_length);
char* RSA_encrypt(const char* input, size_t input_length, char* key, size_t key_length);
char* RSA_decrypt(const char* input, size_t input_length, char* key, size_t key_length);


#endif

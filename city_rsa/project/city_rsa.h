//
// Created by rg on 10/15/17.
//

#ifndef RSACRT_CITY_RSA_H
#define RSACRT_CITY_RSA_H
#include <gmp.h>

typedef struct {
    mpz_t d_p;
    mpz_t d_q;
    mpz_t p;
    mpz_t q;
    mpz_t p_inv;
    mpz_t d;
    mpz_t e;
} city_rsa_config;

int city_rsa_read_cfg(const char* fname, city_rsa_config* cfg);

void city_rsa_init(city_rsa_config *cfg,
const char* p_str,
const char* q_str,
const char* p_inv_str,
const char* d_str,
const char* e_str,
const char* d_p_str,
const char* d_q_str);

void city_print_config(city_rsa_config *cfg);

void city_rsa_sign(city_rsa_config *cfg, char *res_str, char *msg_str);

#endif //RSACRT_CITY_RSA_H

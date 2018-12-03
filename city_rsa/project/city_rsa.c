//
// Created by rg on 10/15/17.
//

#include <gmp.h>
#include <stdio.h>
#include "city_rsa.h"

int city_rsa_read_cfg(const char* fname, city_rsa_config* cfg) {
    FILE* f;
    char p_str[1024];
    char p_inv_str[1024];
    char q_str[1024];
    char d_str[1024];
    char e_str[1024];
    char d_p_str[1024];
    char d_q_str[1024];

    if ((f = fopen(fname, "r")) == NULL) {
        return 0;
    }

    if(7 != fscanf(f, "%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%s",
                   p_str, q_str, p_inv_str,
                   d_str, e_str, d_p_str, d_q_str)) {
        return 0;
    }

    city_rsa_init(cfg, p_str, q_str, p_inv_str, d_str, e_str, d_p_str, d_q_str);
    return 1;
}

void city_print_config(city_rsa_config *cfg) {
    gmp_printf(
            "p: %Zx\nq: %Zx\np_inv: %Zx\nd: %Zx\ne: %Zx\nd_p: %Zx\nd_q: %Zx\n",
            cfg->p, cfg->q, cfg->p_inv, cfg->d, cfg->e, cfg->d_p, cfg->d_q
    );
}

void city_rsa_init(city_rsa_config *cfg,
        const char* p_str,
        const char* q_str,
        const char* p_inv_str,
        const char* d_str,
        const char* e_str,
        const char* d_p_str,
        const char* d_q_str) {
    /* Init config structure */
    mpz_init(cfg->d_p);
    mpz_init(cfg->d_q);
    mpz_init(cfg->p);
    mpz_init(cfg->q);
    mpz_init(cfg->p_inv);
    mpz_init(cfg->d);
    mpz_init(cfg->e);

    /* Set values from strings */
    mpz_set_str(cfg->p, p_str, 0);
    mpz_set_str(cfg->q, q_str, 0);
    mpz_set_str(cfg->p_inv, p_inv_str, 0);
    mpz_set_str(cfg->e, e_str, 0);
    mpz_set_str(cfg->d, d_str, 0);
    mpz_set_str(cfg->d_p, d_p_str, 0);
    mpz_set_str(cfg->d_q, d_q_str, 0);
}

void city_rsa_sign(city_rsa_config *cfg, char *res_str, char *msg_str) {
    /* Init temp vars for calculations */
    mpz_t res;
    mpz_t res_tmp;
    mpz_t msg;
    mpz_t x_p;
    mpz_t x_q;
    mpz_t y_q;
    mpz_t y_p;
    mpz_init(res_tmp);
    mpz_init(res);
    mpz_init(msg);
    mpz_init(x_p);
    mpz_init(x_q);
    mpz_init(y_q);
    mpz_init(y_p);

    mpz_set_str(msg, msg_str, 0);
    // gmp_printf("%Zx\n", msg);
    mpz_mod(x_p, msg, cfg->p);
    mpz_mod(x_q, msg, cfg->q);

    mpz_powm(y_q, x_q, cfg->d_q, cfg->q);
    mpz_powm_sec(y_p, x_p, cfg->d_p, cfg->p);

    mpz_sub(res, y_q, y_p);
    mpz_mul(res_tmp, res, cfg->p_inv);
    mpz_mod(res, res_tmp, cfg->q);
    mpz_mul(res_tmp, res, cfg->p);
    mpz_add(res, res_tmp, y_p);

    mpz_get_str(res_str, 16, res);
}

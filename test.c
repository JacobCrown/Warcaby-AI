#include <stdio.h>

int main()
{

    unsigned char buf, hsw1, hsw5, hsw9, hsw13, PINA;

    PINA = 0b10100000;

    hsw1 = 0xa5;
    hsw5 = 0xa5;
    hsw9 = 0x5a;
    hsw13 = 0x5a;

    buf = PINA <<3; hsw1 = (hsw1<<1) | (buf>>7);
    buf = PINA << 2; hsw5 = (hsw5<<1) | (buf>>7);
    buf = PINA << 1; hsw9 = (hsw9<<1) | (buf>>7);
    buf = PINA <<0; hsw13 = (hsw13<<1) | (buf>>7);

    printf("h_sw1 : %x \n", hsw1);
    printf("h_sw5 : %x \n", hsw5);
    printf("h_sw9 : %x \n", hsw9);
    printf("h_sw13 : %x \n", hsw13);



}
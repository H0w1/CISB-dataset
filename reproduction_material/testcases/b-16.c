// gcc -O2 -g3  -o ttt test.c && ./ttt
// expected output:
// smac:1122334455667788
// dmac:1020304050607080
// result:80 70 60 50 40 30 88 77 66 55 44 33 
// if result is something else, there is a bug.

#include <stdio.h>
#include <strings.h>
#include <stdint.h>
#include <assert.h>

uint64_t DATA_UNI_MAC_l[8]={
  0x1122334455667788,
  0x1122334455667788,
  0x1122334455667788,
  0x1122334455667788,
  0x1122334455667788,
  0x1122334455667788,
  0x1122334455667788,
  0x1122334455667788
};
uint64_t dst_mac=0x1020304050607080ull;

__attribute__ ((noinline))
static void pmac64(const char *info,const uint64_t mac)
{
    printf("%s:%016lx\n",info,mac);
}

__attribute__ ((noinline))
static void pmac(const char *info,const uint8_t *mac,int n)
{
    printf("%s:",info);
    int i;
    for(i=0;i<n;i++)
        printf("%02x ",mac[i]);
    printf("\n");
}

__attribute__ ((always_inline))
__inline__ static void ShortCopy(const char * Shortfrom ,char *Shortto , uint32_t Len)
{

    uint32_t ShortLen;
    uint32_t i;
    uint32_t LeftBytes;

    ShortLen=Len / 2;
    LeftBytes=Len % 2;
    for(i=0;i<ShortLen;i++)
    {
        *(short*)Shortto=*(short*)Shortfrom;
        Shortto+=2;
        Shortfrom+=2;
    }

    for(i=0;i<LeftBytes;i++)
    {
        *Shortto=*Shortfrom;
        Shortto++;
        Shortfrom++;
    }
    return;
}

__attribute__ ((always_inline))
__inline__ static void MACCopy(const char * MACfrom ,char *MACto , uint32_t Len)
{
#if 0
    // this will run correctly
    union{
        char b[8];
        uint64_t d;
    }MAC_temp;
     
     MAC_temp.d=*(uint64_t *)MACfrom;
     ShortCopy(MAC_temp.b,(char*)MACto,Len);
#else
     // this statement is also good
     // volatile uint64_t MAC_temp=*(uint64_t *)MACfrom;
     
     // this statement will run wrongly
     uint64_t MAC_temp=*(uint64_t *)MACfrom;
     ShortCopy((char*)&MAC_temp,(char*)MACto,Len);
#endif
}

static void IPsecCacheBuildImpl(uint8_t OutPortIndex_l,
                                const char *macda)
{
    uint64_t localCache[32];
    bzero(&localCache[0], sizeof(localCache));
    uint8_t *PktHdrPtr=((uint8_t *)&localCache[0]) + sizeof(localCache);
    pmac64("smac",DATA_UNI_MAC_l[OutPortIndex_l]);
    pmac64("dmac",*(uint64_t*)macda);

    PktHdrPtr = PktHdrPtr-6;
    MACCopy((const char*)&DATA_UNI_MAC_l[OutPortIndex_l],(char *)PktHdrPtr,6);

    PktHdrPtr = PktHdrPtr-6;
    MACCopy(macda,(char *)PktHdrPtr,6);

    pmac("result",(uint8_t*)PktHdrPtr,12);
}

int main()
{
    assert(sizeof(uint64_t)==8);
    assert(sizeof(uint32_t)==4);
    assert(sizeof(uint16_t)==2);
    assert(sizeof(uint8_t)==1);

    const char *macda=(char*)&dst_mac;
    uint8_t OutPortIndex_l=1;

    IPsecCacheBuildImpl(OutPortIndex_l, macda);
    return 0;
}
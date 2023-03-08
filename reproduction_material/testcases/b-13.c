/*https://gcc.gnu.org/bugzilla/show_bug.cgi?id=90267
 39             TpcFingerNum[TpcIdex][0] = *(UINT32*)(void*)pstruDlTpcPara;
 40             TpcFingerNum[TpcIdex][1] = pstruDlTpcPara->ucThreeSlotFngNum;
 41 
 42             *(volatile UINT32*)(void*)pstruDlTpcPara = 0;
 43 
 44             TpcFingerNum[TpcIdex][2] = *(UINT32*)(void*)pstruDlTpcPara;
 45             TpcFingerNum[TpcIdex][3] = pstruDlTpcPara->ucThreeSlotFngNum;
 the value of TpcFingerNum[TpcIdex][3] get before the operator of clear the memory
 if there is no "movl $0x0" between "movl %esi, 4(%r9)"  and "movl %esi, 12(%r9)"  in assemble code, that means the compiler reorder the instructions incorrectly.
*/


typedef unsigned char UINT8;
typedef unsigned short UINT16;
typedef unsigned int UINT32;
typedef signed char INT8;
typedef signed short INT16;
typedef signed int INT32;
typedef float FLOAT;
typedef double DOUBLE;
typedef char CHAR;
typedef unsigned char UCHAR;
typedef unsigned int BOOL;
typedef unsigned long long UINT64;
typedef signed long long INT64;

typedef struct
{
    UINT16 hfTpcSoft;
    UINT8 ucThreeSlotCmFlag;
    UINT8 ucThreeSlotFngNum;
}STRU_CCH_DLTPC_PARA;

__attribute__((section(".ll2.cch.bss"))) __attribute__ ((aligned(4))) STRU_CCH_DLTPC_PARA gastruDlTpcPara[(56)];
__attribute__((section(".ddr.cch.uncache.bss"))) UINT32 TpcFingerNum[20][4];
__attribute__((section(".ddr.cch.data"))) UINT32 TpcIdex = 0;

void UBB_CCH_DLTPC_Sche( UINT8 ucLocalChanlNo,
						 UINT8 ucSubSlotIdx,
						 UINT8 ucDpcMode,
						 UINT8 ucCfnNoFingerInd)
{
    STRU_CCH_DLTPC_PARA *pstruDlTpcPara;
    pstruDlTpcPara = &gastruDlTpcPara[ucLocalChanlNo];

    if((1) == ucDpcMode)
    {
        if((0) == ucSubSlotIdx)
        {
            TpcFingerNum[TpcIdex][0] = *(UINT32*)(void*)pstruDlTpcPara;
            TpcFingerNum[TpcIdex][1] = pstruDlTpcPara->ucThreeSlotFngNum;

            *(volatile UINT32*)(void*)pstruDlTpcPara = 0;

            TpcFingerNum[TpcIdex][2] = *(UINT32*)(void*)pstruDlTpcPara;
            TpcFingerNum[TpcIdex][3] = pstruDlTpcPara->ucThreeSlotFngNum;
            TpcIdex = (TpcIdex+1)%20;
        }

        pstruDlTpcPara->ucThreeSlotFngNum += ucCfnNoFingerInd;
    }
}

int main(){
	UBB_CCH_DLTPC_Sche(1, 2, 3, 4);
}
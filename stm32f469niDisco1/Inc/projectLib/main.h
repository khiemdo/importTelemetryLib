#include "stm32f4xx_hal.h"
#include "deviceConfig.h"

#define DEBUGUART_ID	3

#define USE_FULL_ASSERT
#define USE_MY_ASSERT
#define DEBUGON
#define DEBUGLV  LOG_INFO
#define ASSERTLV 2

#define CRC_CCITT



/**
 * \brief: help to index source files and make sure no duplication of index
 * \ref:http://www.barrgroup.com/Embedded-Systems/How-To/Define-Assert-Macro
 */
#define FILENUM(num) \
    enum { F_NUM=num }; \
    void _dummy ## num(void) {}

/*
 * cDebugUart				FILENUM(1);
 * TcDebugUart				FILENUM(2);
 * cFrameMsgGetter.h 		FILENUM(3);
 * TestcFrameMsgGetter.h	FILENUM(4);
 * cInternalStateReport.h	FILENUM(5);
 * TestcInternalStateReport.h	FILENUM(6);
 * cRingBuffer.h			FILENUM(7);
 * cSDLogger.h				FILENUM(9);
 * TestcSDLogger.h			FILENUM(10);
 * cUartPort.h				FILENUM(11);
 * cUartProtocolASCII.h		FILENUM(13);
 * TestcUartProtocolASCII.h	FILENUM(14);
 * utility.h				FILENUM(15);
 * cConfigHandle.h			FILENUM(17)
 * TestcConfigHandle.h		FILENUM(18)
 * crc.c					FILENUM(19);
 * TestCRC.h				FILENUM(20);
 * eeprom.h					FILENUM(21);
 * Tumbler3BSP.h			FILENUM(23);
 * TestTumbler3BSP.h		FILENUM(24);
 * cCanPort.h				FILENUM(25);
 * TestCanPort.h			FILENUM(26);
 * cCanCom					FILENUM(27);
 * TestcCanCom				FILENUM(28);
 * cCanProtocolSlifter		FILENUM(29);
 * TestcCanProtocolSlifter		FILENUM(30);
 * cDebounceSwitch			FILENUM(31);
 * TestDeboundSwitch2		FILENUM(32);
 * cPinOut					FILENUM(33);
 * TestcPintOut				FILENUM(34);
 *
 *
 *
 *
 * main.c 					FILENUM(100);
 * stm32f4xx_it.c 			FILENUM(1000);
 * cSLifter					FILENUM(1000000);
 * TestcSLifter				FILENUM(1000001);
 * cSLifterFSM				FILENUM(1000002);
 * TestcSLifterFSM			FILENUM(1000003);
 *
 *
 *
 *
 *
 *
 */

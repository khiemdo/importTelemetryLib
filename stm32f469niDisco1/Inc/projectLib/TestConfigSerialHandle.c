#include "main.h"
FILENUM(1000000)
#include "TestConfigSerialHandle.h"
#include "cConfigHandle.h"
#include "cAssert.h"
#include "eeprom.h"
#include "crc.h"
#include "configuration.h"
#include <stddef.h>
#include "string.h"
#include "cDebugUart.h"
#include "telemetry.h"
#include "driver.h"
#include "stdlib.h"

#define PSVN_FACTORYSETTINGS	(2)
#define PSVN_USERSETTINGS		(3)
#define SW_VERSION_FACTORYSETTINGS	(6)
#define SW_VERSION_USERSETTINGS		(6)
const FactorySettings DEFAULT_FACTORY_SETTINGS_TestConfigSerialHandle = {
		.psvn = PSVN_FACTORYSETTINGS, .psvnTilda = ~PSVN_FACTORYSETTINGS,
		.softwareVersion =
		SW_VERSION_FACTORYSETTINGS, .deviceID = 4, .paraU16 = 0x0222, .paraU32 =
				0x01111111, .paraI16 = -1024, .paraI32 = -131072, .paraF = 3.14,
		.string1 = { 'a', '\0' }, .string2 = "cd", .string3 = "ban", .char1 =
				'k' };

const UserSettings bullshit = { .psvn = PSVN_USERSETTINGS, .psvnTilda =
		~PSVN_USERSETTINGS, .softwareVersion =
SW_VERSION_USERSETTINGS, .deviceID = 10, .paraU16 = 0x7222, .paraU32 =
		0x71111111, .paraI16 = -1024, .paraI32 = -131072, .paraF = 3.14,
		.string1 = "khiem", .string3 = "hello\r\n" };

TM_transport testTransport;
char tempBuffer[200];
void TestcConfigSerialHandleConfig(void) {
	HAL_FLASH_Unlock();
	int ret = EE_Init();
	crcInit();
	REQUIRE(ret == EE_OK);
//	ret = ValidateConfigurations(&DEFAULT_FACTORY_SETTINGS,
//			&DEFAULT_USER_SETTINGS);
//	REQUIRE(ret > 0);
	testTransport.read = read;
	testTransport.write = write;
	testTransport.readable = readable;
	testTransport.writeable = writeable;
	init_telemetry(&testTransport);
}
void TestSendSettingsInfoOnSerialTelemetry() {
	memcpy(tempBuffer, &bullshit, sizeof(UserSettings));
	*(tempBuffer + sizeof(UserSettings) + 1) = 'a';
	frame("setting", TM_string, tempBuffer, sizeof(UserSettings) + 1);
}
void TestSendSettingsInfoOnSerialDebug() {
	char* ptr = tempBuffer;
	int thisIndex = 0;
	//allocation memory fail
//	sprintf(tempBuffer,"{%u,%u,%u,%u,%u,%u,%d,%d,%f,%s,%s}",
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.psvn,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.psvnTilda,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.softwareVersion,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.deviceID,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.paraU16,
//			(unsigned int)DEFAULT_USER_SETTINGS_TestConfigSerialHandle.paraU32,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.paraI16,
//			(int)DEFAULT_USER_SETTINGS_TestConfigSerialHandle.paraI32,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.paraF,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.string1,
//			DEFAULT_USER_SETTINGS_TestConfigSerialHandle.string3);

//fail when print float
//and somehow it just print double '}';
//	thisIndex = sprintf(ptr,"{");
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%u,",bullshit.psvn);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%u,",bullshit.psvnTilda);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%u,",bullshit.softwareVersion);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%u,",bullshit.deviceID);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%u,",bullshit.paraU16);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%u,",(unsigned int)bullshit.paraU32);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%d,",bullshit.paraI16);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%d,",(int)bullshit.paraI32);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%d,",(int)bullshit.paraF);//cannot print float or it ll overflow
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%s,",bullshit.string1);
//	ptr+=thisIndex;
//	thisIndex = sprintf((char*)ptr,"%s,",bullshit.string3);
//	ptr+=thisIndex;
//	*(ptr) = '}';
//	*(ptr+1) = '\0';
//	thisIndex = sprintf((char*)ptr,")}");
//	frame("setting", TM_string, tempBuffer, sizeof(UserSettings) + 1);

	publish_u16("psvn", bullshit.psvn);
	publish_u16("psvnTilda", bullshit.psvnTilda);
	publish_u16("softwareVersion", bullshit.softwareVersion);
	publish_u16("deviceID", bullshit.deviceID);
	publish_u16("paraU16", bullshit.paraU16);
	publish_u32("paraU32", bullshit.paraU32);
	publish_i16("paraI16", bullshit.paraI16);
	publish_i32("paraI32", bullshit.paraI32);
	publish_f32("paraF", bullshit.paraF);
	publish("string1", bullshit.string1);
	publish("string3", bullshit.string3);

}


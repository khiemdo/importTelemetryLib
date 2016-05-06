#include "main.h"
#include "cDebugUart.h"

#include "TcDebugUart.h"
#include "string.h"
#include "telemetry.h"
#include "driver.h"
#include "TestcConfigHandle.h"
#include "configuration.h"

typedef struct configStorage_{
	UserSettings hello;

}configStorage;
void SystemClock_Config(void);

int main(void) {
	HAL_Init();
	SystemClock_Config();
	UartDebugConfig0();
	FactorySettings fuck1;
	int fucker = sizeof(FactorySettings);
	fucker++;
//	TestcConfigHandleConfig();
	TesConfigWriteAndReadDIffTypes();
//	TestConfigAPI();
	while (1) {
//		TPrinf();

		UARTDebug_TBuffControllerLoop(GetUartDebugPtr());
	}
}

/** System Clock Configuration
 */
void SystemClock_Config(void) {

	RCC_OscInitTypeDef RCC_OscInitStruct;
	RCC_ClkInitTypeDef RCC_ClkInitStruct;

	__PWR_CLK_ENABLE()
	;

	__HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

	RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
	RCC_OscInitStruct.HSEState = RCC_HSE_ON;
	RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
	RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
	RCC_OscInitStruct.PLL.PLLM = 8;
	RCC_OscInitStruct.PLL.PLLN = 336;
	RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
	RCC_OscInitStruct.PLL.PLLQ = 4;
	RCC_OscInitStruct.PLL.PLLR = 2;
	HAL_RCC_OscConfig(&RCC_OscInitStruct);

	RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
			| RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
	RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
	RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
	RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
	RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;
	HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5);

	HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq() / 1000);

	HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);

	/* SysTick_IRQn interrupt configuration */
	HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
	if (huart->Instance == DEBUGUART_ADDR) {
		HAL_UARTDebug_RxCpltCallback(huart);
	}
}
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
	if (huart->Instance == DEBUGUART_ADDR) {
		HAL_UARTDebug_TxCpltCallback(huart);
	}
}
#ifdef USE_FULL_ASSERT
void assert_failed(uint8_t * file, uint32_t line) {
	// send2UartDebug
	UDebugPrintf("Wrong parameters value: file %s on line %d\r\n", (char*) file,
			(int) line);

	// report as errorCode :[version][F_NUM][__LINE__][TaskID]
	// save2eeprom
	// save2uSD
}

#endif
#ifdef  USE_MY_ASSERT
void my_assert_failed(uint8_t * file, uint32_t line, uint32_t fileIndex,
		int8_t * expression) {

	// send2UartDebug
	UDebugPrintf("Wrong parameters value: file %s on line %d\r\n", (char*) file,
			(int) line);
	// report as errorCode :[version][F_NUM][__LINE__][TaskID]
	// save2eeprom
	// save2uSD
	// ledIndicator
}
#endif
#ifdef DEBUGON
void DebugLogHandle(int8_t * msg, ...) {
	UDebugPrintf((char*) msg);
}
#endif

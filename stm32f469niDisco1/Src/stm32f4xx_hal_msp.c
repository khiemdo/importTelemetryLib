#include "main.h"

void HAL_MspInit(void) {
	HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);

	/* System interrupt init*/
	/* MemoryManagement_IRQn interrupt configuration */
	HAL_NVIC_SetPriority(MemoryManagement_IRQn, 0, 0);
	/* BusFault_IRQn interrupt configuration */
	HAL_NVIC_SetPriority(BusFault_IRQn, 0, 0);
	/* UsageFault_IRQn interrupt configuration */
	HAL_NVIC_SetPriority(UsageFault_IRQn, 0, 0);
	/* SysTick_IRQn interrupt configuration */
	HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
}

void HAL_UART_MspInit(UART_HandleTypeDef* huart) {
}

void HAL_UART_MspDeInit(UART_HandleTypeDef* huart) {
}

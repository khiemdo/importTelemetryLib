/* Includes ------------------------------------------------------------------*/
#include "main.h"
FILENUM(1000);

#include "stm32f4xx.h"
#include "stm32f4xx_it.h"
#include "cDebugUart.h"
#include "cCanCom.h"

#include "TestCanPort.h"

/* External variables --------------------------------------------------------*/
extern CAN_HandleTypeDef * testCan;
/**
 * @brief This function handles System tick timer.
 */
void SysTick_Handler(void) {
	HAL_IncTick();
	HAL_SYSTICK_IRQHandler();
}

#if DEBUGUART_ID == 6
/**
 * @brief This function handles USART1 global interrupt.
 */
void USART6_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_UART_IRQHandler(huart);
}

/**
 * @brief This function handles DMA2 stream2 global interrupt.
 */
void DMA2_Stream1_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmarx);
}

/**
 * @brief This function handles DMA2 stream7 global interrupt.
 */
void DMA2_Stream6_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmatx);
}

#elif DEBUGUART_ID == 1
/**
 * @brief This function handles USART1 global interrupt.
 */
void USART1_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_UART_IRQHandler(huart);
}

/**
 * @brief This function handles DMA2 stream2 global interrupt.
 */
void DMA2_Stream2_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmarx);
}

/**
 * @brief This function handles DMA2 stream7 global interrupt.
 */
void DMA2_Stream7_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmatx);
}
#elif DEBUGUART_ID == 3
/**
 * @brief This function handles USART1 global interrupt.
 */
void USART3_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_UART_IRQHandler(huart);
}

/**
 * @brief This function handles DMA2 stream2 global interrupt.
 */
void DMA1_Stream1_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmarx);
}

/**
 * @brief This function handles DMA2 stream7 global interrupt.
 */
void DMA1_Stream3_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmatx);
}
#elif DEBUGUART_ID == 2
/**
 * @brief This function handles USART1 global interrupt.
 */
void USART2_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_UART_IRQHandler(huart);
}

/**
 * @brief This function handles DMA2 stream2 global interrupt.
 */
void DMA1_Stream5_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmarx);
}

/**
 * @brief This function handles DMA2 stream7 global interrupt.
 */
void DMA1_Stream6_IRQHandler(void) {
	UART_HandleTypeDef* huart = GetUartDebugPtr();
	HAL_DMA_IRQHandler(huart->hdmatx);
}

#endif

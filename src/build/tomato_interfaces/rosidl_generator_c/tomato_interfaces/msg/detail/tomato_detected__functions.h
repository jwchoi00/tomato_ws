// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#ifndef TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__FUNCTIONS_H_
#define TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "tomato_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "tomato_interfaces/msg/detail/tomato_detected__struct.h"

/// Initialize msg/TomatoDetected message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * tomato_interfaces__msg__TomatoDetected
 * )) before or use
 * tomato_interfaces__msg__TomatoDetected__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
bool
tomato_interfaces__msg__TomatoDetected__init(tomato_interfaces__msg__TomatoDetected * msg);

/// Finalize msg/TomatoDetected message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
void
tomato_interfaces__msg__TomatoDetected__fini(tomato_interfaces__msg__TomatoDetected * msg);

/// Create msg/TomatoDetected message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * tomato_interfaces__msg__TomatoDetected__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
tomato_interfaces__msg__TomatoDetected *
tomato_interfaces__msg__TomatoDetected__create();

/// Destroy msg/TomatoDetected message.
/**
 * It calls
 * tomato_interfaces__msg__TomatoDetected__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
void
tomato_interfaces__msg__TomatoDetected__destroy(tomato_interfaces__msg__TomatoDetected * msg);

/// Check for msg/TomatoDetected message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
bool
tomato_interfaces__msg__TomatoDetected__are_equal(const tomato_interfaces__msg__TomatoDetected * lhs, const tomato_interfaces__msg__TomatoDetected * rhs);

/// Copy a msg/TomatoDetected message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
bool
tomato_interfaces__msg__TomatoDetected__copy(
  const tomato_interfaces__msg__TomatoDetected * input,
  tomato_interfaces__msg__TomatoDetected * output);

/// Initialize array of msg/TomatoDetected messages.
/**
 * It allocates the memory for the number of elements and calls
 * tomato_interfaces__msg__TomatoDetected__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
bool
tomato_interfaces__msg__TomatoDetected__Sequence__init(tomato_interfaces__msg__TomatoDetected__Sequence * array, size_t size);

/// Finalize array of msg/TomatoDetected messages.
/**
 * It calls
 * tomato_interfaces__msg__TomatoDetected__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
void
tomato_interfaces__msg__TomatoDetected__Sequence__fini(tomato_interfaces__msg__TomatoDetected__Sequence * array);

/// Create array of msg/TomatoDetected messages.
/**
 * It allocates the memory for the array and calls
 * tomato_interfaces__msg__TomatoDetected__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
tomato_interfaces__msg__TomatoDetected__Sequence *
tomato_interfaces__msg__TomatoDetected__Sequence__create(size_t size);

/// Destroy array of msg/TomatoDetected messages.
/**
 * It calls
 * tomato_interfaces__msg__TomatoDetected__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
void
tomato_interfaces__msg__TomatoDetected__Sequence__destroy(tomato_interfaces__msg__TomatoDetected__Sequence * array);

/// Check for msg/TomatoDetected message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
bool
tomato_interfaces__msg__TomatoDetected__Sequence__are_equal(const tomato_interfaces__msg__TomatoDetected__Sequence * lhs, const tomato_interfaces__msg__TomatoDetected__Sequence * rhs);

/// Copy an array of msg/TomatoDetected messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tomato_interfaces
bool
tomato_interfaces__msg__TomatoDetected__Sequence__copy(
  const tomato_interfaces__msg__TomatoDetected__Sequence * input,
  tomato_interfaces__msg__TomatoDetected__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__FUNCTIONS_H_

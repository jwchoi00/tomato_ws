// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#ifndef TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__STRUCT_H_
#define TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/TomatoDetected in the package tomato_interfaces.
typedef struct tomato_interfaces__msg__TomatoDetected
{
  bool detected;
} tomato_interfaces__msg__TomatoDetected;

// Struct for a sequence of tomato_interfaces__msg__TomatoDetected.
typedef struct tomato_interfaces__msg__TomatoDetected__Sequence
{
  tomato_interfaces__msg__TomatoDetected * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tomato_interfaces__msg__TomatoDetected__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__STRUCT_H_

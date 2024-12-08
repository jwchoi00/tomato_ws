// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#ifndef TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "tomato_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "tomato_interfaces/msg/detail/tomato_detected__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace tomato_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tomato_interfaces
cdr_serialize(
  const tomato_interfaces::msg::TomatoDetected & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tomato_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  tomato_interfaces::msg::TomatoDetected & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tomato_interfaces
get_serialized_size(
  const tomato_interfaces::msg::TomatoDetected & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tomato_interfaces
max_serialized_size_TomatoDetected(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace tomato_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tomato_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, tomato_interfaces, msg, TomatoDetected)();

#ifdef __cplusplus
}
#endif

#endif  // TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

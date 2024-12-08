// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice
#include "tomato_interfaces/msg/detail/tomato_detected__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "tomato_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "tomato_interfaces/msg/detail/tomato_detected__struct.h"
#include "tomato_interfaces/msg/detail/tomato_detected__functions.h"
#include "fastcdr/Cdr.h"

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

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _TomatoDetected__ros_msg_type = tomato_interfaces__msg__TomatoDetected;

static bool _TomatoDetected__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _TomatoDetected__ros_msg_type * ros_message = static_cast<const _TomatoDetected__ros_msg_type *>(untyped_ros_message);
  // Field name: detected
  {
    cdr << (ros_message->detected ? true : false);
  }

  return true;
}

static bool _TomatoDetected__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _TomatoDetected__ros_msg_type * ros_message = static_cast<_TomatoDetected__ros_msg_type *>(untyped_ros_message);
  // Field name: detected
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->detected = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_tomato_interfaces
size_t get_serialized_size_tomato_interfaces__msg__TomatoDetected(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _TomatoDetected__ros_msg_type * ros_message = static_cast<const _TomatoDetected__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name detected
  {
    size_t item_size = sizeof(ros_message->detected);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _TomatoDetected__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_tomato_interfaces__msg__TomatoDetected(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_tomato_interfaces
size_t max_serialized_size_tomato_interfaces__msg__TomatoDetected(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: detected
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = tomato_interfaces__msg__TomatoDetected;
    is_plain =
      (
      offsetof(DataType, detected) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _TomatoDetected__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_tomato_interfaces__msg__TomatoDetected(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_TomatoDetected = {
  "tomato_interfaces::msg",
  "TomatoDetected",
  _TomatoDetected__cdr_serialize,
  _TomatoDetected__cdr_deserialize,
  _TomatoDetected__get_serialized_size,
  _TomatoDetected__max_serialized_size
};

static rosidl_message_type_support_t _TomatoDetected__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_TomatoDetected,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, tomato_interfaces, msg, TomatoDetected)() {
  return &_TomatoDetected__type_support;
}

#if defined(__cplusplus)
}
#endif

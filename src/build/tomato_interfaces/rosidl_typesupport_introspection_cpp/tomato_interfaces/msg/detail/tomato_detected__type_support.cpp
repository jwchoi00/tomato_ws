// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "tomato_interfaces/msg/detail/tomato_detected__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace tomato_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void TomatoDetected_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) tomato_interfaces::msg::TomatoDetected(_init);
}

void TomatoDetected_fini_function(void * message_memory)
{
  auto typed_message = static_cast<tomato_interfaces::msg::TomatoDetected *>(message_memory);
  typed_message->~TomatoDetected();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember TomatoDetected_message_member_array[1] = {
  {
    "detected",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(tomato_interfaces::msg::TomatoDetected, detected),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers TomatoDetected_message_members = {
  "tomato_interfaces::msg",  // message namespace
  "TomatoDetected",  // message name
  1,  // number of fields
  sizeof(tomato_interfaces::msg::TomatoDetected),
  TomatoDetected_message_member_array,  // message members
  TomatoDetected_init_function,  // function to initialize message memory (memory has to be allocated)
  TomatoDetected_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t TomatoDetected_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &TomatoDetected_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace tomato_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<tomato_interfaces::msg::TomatoDetected>()
{
  return &::tomato_interfaces::msg::rosidl_typesupport_introspection_cpp::TomatoDetected_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, tomato_interfaces, msg, TomatoDetected)() {
  return &::tomato_interfaces::msg::rosidl_typesupport_introspection_cpp::TomatoDetected_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

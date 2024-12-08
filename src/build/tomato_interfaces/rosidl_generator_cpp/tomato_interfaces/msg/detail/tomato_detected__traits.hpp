// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#ifndef TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__TRAITS_HPP_
#define TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "tomato_interfaces/msg/detail/tomato_detected__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace tomato_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TomatoDetected & msg,
  std::ostream & out)
{
  out << "{";
  // member: detected
  {
    out << "detected: ";
    rosidl_generator_traits::value_to_yaml(msg.detected, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TomatoDetected & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "detected: ";
    rosidl_generator_traits::value_to_yaml(msg.detected, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TomatoDetected & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace tomato_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use tomato_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const tomato_interfaces::msg::TomatoDetected & msg,
  std::ostream & out, size_t indentation = 0)
{
  tomato_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use tomato_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const tomato_interfaces::msg::TomatoDetected & msg)
{
  return tomato_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<tomato_interfaces::msg::TomatoDetected>()
{
  return "tomato_interfaces::msg::TomatoDetected";
}

template<>
inline const char * name<tomato_interfaces::msg::TomatoDetected>()
{
  return "tomato_interfaces/msg/TomatoDetected";
}

template<>
struct has_fixed_size<tomato_interfaces::msg::TomatoDetected>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<tomato_interfaces::msg::TomatoDetected>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<tomato_interfaces::msg::TomatoDetected>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__TRAITS_HPP_

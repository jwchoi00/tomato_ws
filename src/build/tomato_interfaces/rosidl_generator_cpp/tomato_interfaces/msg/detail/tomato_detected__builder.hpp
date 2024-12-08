// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#ifndef TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__BUILDER_HPP_
#define TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tomato_interfaces/msg/detail/tomato_detected__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tomato_interfaces
{

namespace msg
{

namespace builder
{

class Init_TomatoDetected_detected
{
public:
  Init_TomatoDetected_detected()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::tomato_interfaces::msg::TomatoDetected detected(::tomato_interfaces::msg::TomatoDetected::_detected_type arg)
  {
    msg_.detected = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tomato_interfaces::msg::TomatoDetected msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::tomato_interfaces::msg::TomatoDetected>()
{
  return tomato_interfaces::msg::builder::Init_TomatoDetected_detected();
}

}  // namespace tomato_interfaces

#endif  // TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__BUILDER_HPP_

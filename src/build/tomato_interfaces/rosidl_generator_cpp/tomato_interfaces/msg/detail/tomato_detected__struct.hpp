// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice

#ifndef TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__STRUCT_HPP_
#define TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tomato_interfaces__msg__TomatoDetected __attribute__((deprecated))
#else
# define DEPRECATED__tomato_interfaces__msg__TomatoDetected __declspec(deprecated)
#endif

namespace tomato_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TomatoDetected_
{
  using Type = TomatoDetected_<ContainerAllocator>;

  explicit TomatoDetected_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->detected = false;
    }
  }

  explicit TomatoDetected_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->detected = false;
    }
  }

  // field types and members
  using _detected_type =
    bool;
  _detected_type detected;

  // setters for named parameter idiom
  Type & set__detected(
    const bool & _arg)
  {
    this->detected = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tomato_interfaces::msg::TomatoDetected_<ContainerAllocator> *;
  using ConstRawPtr =
    const tomato_interfaces::msg::TomatoDetected_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tomato_interfaces::msg::TomatoDetected_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tomato_interfaces::msg::TomatoDetected_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tomato_interfaces__msg__TomatoDetected
    std::shared_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tomato_interfaces__msg__TomatoDetected
    std::shared_ptr<tomato_interfaces::msg::TomatoDetected_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TomatoDetected_ & other) const
  {
    if (this->detected != other.detected) {
      return false;
    }
    return true;
  }
  bool operator!=(const TomatoDetected_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TomatoDetected_

// alias to use template instance with default allocator
using TomatoDetected =
  tomato_interfaces::msg::TomatoDetected_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace tomato_interfaces

#endif  // TOMATO_INTERFACES__MSG__DETAIL__TOMATO_DETECTED__STRUCT_HPP_

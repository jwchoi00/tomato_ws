// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from tomato_interfaces:msg/TomatoDetected.idl
// generated code does not contain a copyright notice
#include "tomato_interfaces/msg/detail/tomato_detected__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
tomato_interfaces__msg__TomatoDetected__init(tomato_interfaces__msg__TomatoDetected * msg)
{
  if (!msg) {
    return false;
  }
  // detected
  return true;
}

void
tomato_interfaces__msg__TomatoDetected__fini(tomato_interfaces__msg__TomatoDetected * msg)
{
  if (!msg) {
    return;
  }
  // detected
}

bool
tomato_interfaces__msg__TomatoDetected__are_equal(const tomato_interfaces__msg__TomatoDetected * lhs, const tomato_interfaces__msg__TomatoDetected * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // detected
  if (lhs->detected != rhs->detected) {
    return false;
  }
  return true;
}

bool
tomato_interfaces__msg__TomatoDetected__copy(
  const tomato_interfaces__msg__TomatoDetected * input,
  tomato_interfaces__msg__TomatoDetected * output)
{
  if (!input || !output) {
    return false;
  }
  // detected
  output->detected = input->detected;
  return true;
}

tomato_interfaces__msg__TomatoDetected *
tomato_interfaces__msg__TomatoDetected__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tomato_interfaces__msg__TomatoDetected * msg = (tomato_interfaces__msg__TomatoDetected *)allocator.allocate(sizeof(tomato_interfaces__msg__TomatoDetected), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(tomato_interfaces__msg__TomatoDetected));
  bool success = tomato_interfaces__msg__TomatoDetected__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
tomato_interfaces__msg__TomatoDetected__destroy(tomato_interfaces__msg__TomatoDetected * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    tomato_interfaces__msg__TomatoDetected__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
tomato_interfaces__msg__TomatoDetected__Sequence__init(tomato_interfaces__msg__TomatoDetected__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tomato_interfaces__msg__TomatoDetected * data = NULL;

  if (size) {
    data = (tomato_interfaces__msg__TomatoDetected *)allocator.zero_allocate(size, sizeof(tomato_interfaces__msg__TomatoDetected), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = tomato_interfaces__msg__TomatoDetected__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        tomato_interfaces__msg__TomatoDetected__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
tomato_interfaces__msg__TomatoDetected__Sequence__fini(tomato_interfaces__msg__TomatoDetected__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      tomato_interfaces__msg__TomatoDetected__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

tomato_interfaces__msg__TomatoDetected__Sequence *
tomato_interfaces__msg__TomatoDetected__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tomato_interfaces__msg__TomatoDetected__Sequence * array = (tomato_interfaces__msg__TomatoDetected__Sequence *)allocator.allocate(sizeof(tomato_interfaces__msg__TomatoDetected__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = tomato_interfaces__msg__TomatoDetected__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
tomato_interfaces__msg__TomatoDetected__Sequence__destroy(tomato_interfaces__msg__TomatoDetected__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    tomato_interfaces__msg__TomatoDetected__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
tomato_interfaces__msg__TomatoDetected__Sequence__are_equal(const tomato_interfaces__msg__TomatoDetected__Sequence * lhs, const tomato_interfaces__msg__TomatoDetected__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!tomato_interfaces__msg__TomatoDetected__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
tomato_interfaces__msg__TomatoDetected__Sequence__copy(
  const tomato_interfaces__msg__TomatoDetected__Sequence * input,
  tomato_interfaces__msg__TomatoDetected__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(tomato_interfaces__msg__TomatoDetected);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    tomato_interfaces__msg__TomatoDetected * data =
      (tomato_interfaces__msg__TomatoDetected *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!tomato_interfaces__msg__TomatoDetected__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          tomato_interfaces__msg__TomatoDetected__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!tomato_interfaces__msg__TomatoDetected__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

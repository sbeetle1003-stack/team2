// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from project2_interfaces:action/PlacePiece.idl
// generated code does not contain a copyright notice
#include "project2_interfaces/action/detail/place_piece__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
project2_interfaces__action__PlacePiece_Goal__init(project2_interfaces__action__PlacePiece_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // cell_id
  return true;
}

void
project2_interfaces__action__PlacePiece_Goal__fini(project2_interfaces__action__PlacePiece_Goal * msg)
{
  if (!msg) {
    return;
  }
  // cell_id
}

bool
project2_interfaces__action__PlacePiece_Goal__are_equal(const project2_interfaces__action__PlacePiece_Goal * lhs, const project2_interfaces__action__PlacePiece_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // cell_id
  if (lhs->cell_id != rhs->cell_id) {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_Goal__copy(
  const project2_interfaces__action__PlacePiece_Goal * input,
  project2_interfaces__action__PlacePiece_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // cell_id
  output->cell_id = input->cell_id;
  return true;
}

project2_interfaces__action__PlacePiece_Goal *
project2_interfaces__action__PlacePiece_Goal__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Goal * msg = (project2_interfaces__action__PlacePiece_Goal *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_Goal));
  bool success = project2_interfaces__action__PlacePiece_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_Goal__destroy(project2_interfaces__action__PlacePiece_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_Goal__Sequence__init(project2_interfaces__action__PlacePiece_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Goal * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_Goal)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_Goal *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_Goal__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_Goal__Sequence__fini(project2_interfaces__action__PlacePiece_Goal__Sequence * array)
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
      project2_interfaces__action__PlacePiece_Goal__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_Goal__Sequence *
project2_interfaces__action__PlacePiece_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Goal__Sequence * array = (project2_interfaces__action__PlacePiece_Goal__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_Goal__Sequence__destroy(project2_interfaces__action__PlacePiece_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_Goal__Sequence__are_equal(const project2_interfaces__action__PlacePiece_Goal__Sequence * lhs, const project2_interfaces__action__PlacePiece_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_Goal__Sequence__copy(
  const project2_interfaces__action__PlacePiece_Goal__Sequence * input,
  project2_interfaces__action__PlacePiece_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_Goal)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_Goal * data =
      (project2_interfaces__action__PlacePiece_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
project2_interfaces__action__PlacePiece_Result__init(project2_interfaces__action__PlacePiece_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // error_code
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    project2_interfaces__action__PlacePiece_Result__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_Result__fini(project2_interfaces__action__PlacePiece_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // error_code
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
project2_interfaces__action__PlacePiece_Result__are_equal(const project2_interfaces__action__PlacePiece_Result * lhs, const project2_interfaces__action__PlacePiece_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // error_code
  if (lhs->error_code != rhs->error_code) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_Result__copy(
  const project2_interfaces__action__PlacePiece_Result * input,
  project2_interfaces__action__PlacePiece_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // error_code
  output->error_code = input->error_code;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_Result *
project2_interfaces__action__PlacePiece_Result__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Result * msg = (project2_interfaces__action__PlacePiece_Result *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_Result));
  bool success = project2_interfaces__action__PlacePiece_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_Result__destroy(project2_interfaces__action__PlacePiece_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_Result__Sequence__init(project2_interfaces__action__PlacePiece_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Result * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_Result)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_Result *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_Result__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_Result__Sequence__fini(project2_interfaces__action__PlacePiece_Result__Sequence * array)
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
      project2_interfaces__action__PlacePiece_Result__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_Result__Sequence *
project2_interfaces__action__PlacePiece_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Result__Sequence * array = (project2_interfaces__action__PlacePiece_Result__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_Result__Sequence__destroy(project2_interfaces__action__PlacePiece_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_Result__Sequence__are_equal(const project2_interfaces__action__PlacePiece_Result__Sequence * lhs, const project2_interfaces__action__PlacePiece_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_Result__Sequence__copy(
  const project2_interfaces__action__PlacePiece_Result__Sequence * input,
  project2_interfaces__action__PlacePiece_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_Result)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_Result * data =
      (project2_interfaces__action__PlacePiece_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stage`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
project2_interfaces__action__PlacePiece_Feedback__init(project2_interfaces__action__PlacePiece_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // stage
  if (!rosidl_runtime_c__String__init(&msg->stage)) {
    project2_interfaces__action__PlacePiece_Feedback__fini(msg);
    return false;
  }
  // progress
  return true;
}

void
project2_interfaces__action__PlacePiece_Feedback__fini(project2_interfaces__action__PlacePiece_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // stage
  rosidl_runtime_c__String__fini(&msg->stage);
  // progress
}

bool
project2_interfaces__action__PlacePiece_Feedback__are_equal(const project2_interfaces__action__PlacePiece_Feedback * lhs, const project2_interfaces__action__PlacePiece_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stage
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->stage), &(rhs->stage)))
  {
    return false;
  }
  // progress
  if (lhs->progress != rhs->progress) {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_Feedback__copy(
  const project2_interfaces__action__PlacePiece_Feedback * input,
  project2_interfaces__action__PlacePiece_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // stage
  if (!rosidl_runtime_c__String__copy(
      &(input->stage), &(output->stage)))
  {
    return false;
  }
  // progress
  output->progress = input->progress;
  return true;
}

project2_interfaces__action__PlacePiece_Feedback *
project2_interfaces__action__PlacePiece_Feedback__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Feedback * msg = (project2_interfaces__action__PlacePiece_Feedback *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_Feedback));
  bool success = project2_interfaces__action__PlacePiece_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_Feedback__destroy(project2_interfaces__action__PlacePiece_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_Feedback__Sequence__init(project2_interfaces__action__PlacePiece_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Feedback * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_Feedback)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_Feedback *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_Feedback__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_Feedback__Sequence__fini(project2_interfaces__action__PlacePiece_Feedback__Sequence * array)
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
      project2_interfaces__action__PlacePiece_Feedback__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_Feedback__Sequence *
project2_interfaces__action__PlacePiece_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_Feedback__Sequence * array = (project2_interfaces__action__PlacePiece_Feedback__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_Feedback__Sequence__destroy(project2_interfaces__action__PlacePiece_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_Feedback__Sequence__are_equal(const project2_interfaces__action__PlacePiece_Feedback__Sequence * lhs, const project2_interfaces__action__PlacePiece_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_Feedback__Sequence__copy(
  const project2_interfaces__action__PlacePiece_Feedback__Sequence * input,
  project2_interfaces__action__PlacePiece_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_Feedback)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_Feedback * data =
      (project2_interfaces__action__PlacePiece_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "project2_interfaces/action/detail/place_piece__functions.h"

bool
project2_interfaces__action__PlacePiece_SendGoal_Request__init(project2_interfaces__action__PlacePiece_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    project2_interfaces__action__PlacePiece_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!project2_interfaces__action__PlacePiece_Goal__init(&msg->goal)) {
    project2_interfaces__action__PlacePiece_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Request__fini(project2_interfaces__action__PlacePiece_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  project2_interfaces__action__PlacePiece_Goal__fini(&msg->goal);
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Request__are_equal(const project2_interfaces__action__PlacePiece_SendGoal_Request * lhs, const project2_interfaces__action__PlacePiece_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!project2_interfaces__action__PlacePiece_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Request__copy(
  const project2_interfaces__action__PlacePiece_SendGoal_Request * input,
  project2_interfaces__action__PlacePiece_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!project2_interfaces__action__PlacePiece_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_SendGoal_Request *
project2_interfaces__action__PlacePiece_SendGoal_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Request * msg = (project2_interfaces__action__PlacePiece_SendGoal_Request *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request));
  bool success = project2_interfaces__action__PlacePiece_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Request__destroy(project2_interfaces__action__PlacePiece_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__init(project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_SendGoal_Request *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_SendGoal_Request__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__fini(project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * array)
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
      project2_interfaces__action__PlacePiece_SendGoal_Request__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence *
project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * array = (project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__destroy(project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__are_equal(const project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * lhs, const project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__copy(
  const project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * input,
  project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_SendGoal_Request * data =
      (project2_interfaces__action__PlacePiece_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
project2_interfaces__action__PlacePiece_SendGoal_Response__init(project2_interfaces__action__PlacePiece_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    project2_interfaces__action__PlacePiece_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Response__fini(project2_interfaces__action__PlacePiece_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Response__are_equal(const project2_interfaces__action__PlacePiece_SendGoal_Response * lhs, const project2_interfaces__action__PlacePiece_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Response__copy(
  const project2_interfaces__action__PlacePiece_SendGoal_Response * input,
  project2_interfaces__action__PlacePiece_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_SendGoal_Response *
project2_interfaces__action__PlacePiece_SendGoal_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Response * msg = (project2_interfaces__action__PlacePiece_SendGoal_Response *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response));
  bool success = project2_interfaces__action__PlacePiece_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Response__destroy(project2_interfaces__action__PlacePiece_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__init(project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_SendGoal_Response *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_SendGoal_Response__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__fini(project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * array)
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
      project2_interfaces__action__PlacePiece_SendGoal_Response__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence *
project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * array = (project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__destroy(project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__are_equal(const project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * lhs, const project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__copy(
  const project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * input,
  project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_SendGoal_Response * data =
      (project2_interfaces__action__PlacePiece_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "project2_interfaces/action/detail/place_piece__functions.h"

bool
project2_interfaces__action__PlacePiece_SendGoal_Event__init(project2_interfaces__action__PlacePiece_SendGoal_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    project2_interfaces__action__PlacePiece_SendGoal_Event__fini(msg);
    return false;
  }
  // request
  if (!project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__init(&msg->request, 0)) {
    project2_interfaces__action__PlacePiece_SendGoal_Event__fini(msg);
    return false;
  }
  // response
  if (!project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__init(&msg->response, 0)) {
    project2_interfaces__action__PlacePiece_SendGoal_Event__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Event__fini(project2_interfaces__action__PlacePiece_SendGoal_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__fini(&msg->request);
  // response
  project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__fini(&msg->response);
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Event__are_equal(const project2_interfaces__action__PlacePiece_SendGoal_Event * lhs, const project2_interfaces__action__PlacePiece_SendGoal_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Event__copy(
  const project2_interfaces__action__PlacePiece_SendGoal_Event * input,
  project2_interfaces__action__PlacePiece_SendGoal_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_SendGoal_Event *
project2_interfaces__action__PlacePiece_SendGoal_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Event * msg = (project2_interfaces__action__PlacePiece_SendGoal_Event *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event));
  bool success = project2_interfaces__action__PlacePiece_SendGoal_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Event__destroy(project2_interfaces__action__PlacePiece_SendGoal_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_SendGoal_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__init(project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_SendGoal_Event *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_SendGoal_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_SendGoal_Event__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__fini(project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * array)
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
      project2_interfaces__action__PlacePiece_SendGoal_Event__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence *
project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * array = (project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__destroy(project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__are_equal(const project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * lhs, const project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_SendGoal_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence__copy(
  const project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * input,
  project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_SendGoal_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_SendGoal_Event * data =
      (project2_interfaces__action__PlacePiece_SendGoal_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_SendGoal_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_SendGoal_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_SendGoal_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
project2_interfaces__action__PlacePiece_GetResult_Request__init(project2_interfaces__action__PlacePiece_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    project2_interfaces__action__PlacePiece_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_GetResult_Request__fini(project2_interfaces__action__PlacePiece_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
project2_interfaces__action__PlacePiece_GetResult_Request__are_equal(const project2_interfaces__action__PlacePiece_GetResult_Request * lhs, const project2_interfaces__action__PlacePiece_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_GetResult_Request__copy(
  const project2_interfaces__action__PlacePiece_GetResult_Request * input,
  project2_interfaces__action__PlacePiece_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_GetResult_Request *
project2_interfaces__action__PlacePiece_GetResult_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Request * msg = (project2_interfaces__action__PlacePiece_GetResult_Request *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_GetResult_Request));
  bool success = project2_interfaces__action__PlacePiece_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_GetResult_Request__destroy(project2_interfaces__action__PlacePiece_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__init(project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_GetResult_Request)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_GetResult_Request *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_GetResult_Request__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__fini(project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * array)
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
      project2_interfaces__action__PlacePiece_GetResult_Request__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_GetResult_Request__Sequence *
project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * array = (project2_interfaces__action__PlacePiece_GetResult_Request__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__destroy(project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__are_equal(const project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * lhs, const project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__copy(
  const project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * input,
  project2_interfaces__action__PlacePiece_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_GetResult_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_GetResult_Request * data =
      (project2_interfaces__action__PlacePiece_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "project2_interfaces/action/detail/place_piece__functions.h"

bool
project2_interfaces__action__PlacePiece_GetResult_Response__init(project2_interfaces__action__PlacePiece_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!project2_interfaces__action__PlacePiece_Result__init(&msg->result)) {
    project2_interfaces__action__PlacePiece_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_GetResult_Response__fini(project2_interfaces__action__PlacePiece_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  project2_interfaces__action__PlacePiece_Result__fini(&msg->result);
}

bool
project2_interfaces__action__PlacePiece_GetResult_Response__are_equal(const project2_interfaces__action__PlacePiece_GetResult_Response * lhs, const project2_interfaces__action__PlacePiece_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!project2_interfaces__action__PlacePiece_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_GetResult_Response__copy(
  const project2_interfaces__action__PlacePiece_GetResult_Response * input,
  project2_interfaces__action__PlacePiece_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!project2_interfaces__action__PlacePiece_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_GetResult_Response *
project2_interfaces__action__PlacePiece_GetResult_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Response * msg = (project2_interfaces__action__PlacePiece_GetResult_Response *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_GetResult_Response));
  bool success = project2_interfaces__action__PlacePiece_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_GetResult_Response__destroy(project2_interfaces__action__PlacePiece_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__init(project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_GetResult_Response)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_GetResult_Response *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_GetResult_Response__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__fini(project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * array)
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
      project2_interfaces__action__PlacePiece_GetResult_Response__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_GetResult_Response__Sequence *
project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * array = (project2_interfaces__action__PlacePiece_GetResult_Response__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__destroy(project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__are_equal(const project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * lhs, const project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__copy(
  const project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * input,
  project2_interfaces__action__PlacePiece_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_GetResult_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_GetResult_Response * data =
      (project2_interfaces__action__PlacePiece_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
// already included above
// #include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "project2_interfaces/action/detail/place_piece__functions.h"

bool
project2_interfaces__action__PlacePiece_GetResult_Event__init(project2_interfaces__action__PlacePiece_GetResult_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    project2_interfaces__action__PlacePiece_GetResult_Event__fini(msg);
    return false;
  }
  // request
  if (!project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__init(&msg->request, 0)) {
    project2_interfaces__action__PlacePiece_GetResult_Event__fini(msg);
    return false;
  }
  // response
  if (!project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__init(&msg->response, 0)) {
    project2_interfaces__action__PlacePiece_GetResult_Event__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_GetResult_Event__fini(project2_interfaces__action__PlacePiece_GetResult_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__fini(&msg->request);
  // response
  project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__fini(&msg->response);
}

bool
project2_interfaces__action__PlacePiece_GetResult_Event__are_equal(const project2_interfaces__action__PlacePiece_GetResult_Event * lhs, const project2_interfaces__action__PlacePiece_GetResult_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_GetResult_Event__copy(
  const project2_interfaces__action__PlacePiece_GetResult_Event * input,
  project2_interfaces__action__PlacePiece_GetResult_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_GetResult_Event *
project2_interfaces__action__PlacePiece_GetResult_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Event * msg = (project2_interfaces__action__PlacePiece_GetResult_Event *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_GetResult_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_GetResult_Event));
  bool success = project2_interfaces__action__PlacePiece_GetResult_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_GetResult_Event__destroy(project2_interfaces__action__PlacePiece_GetResult_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_GetResult_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__init(project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_GetResult_Event)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_GetResult_Event *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_GetResult_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_GetResult_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_GetResult_Event__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__fini(project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * array)
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
      project2_interfaces__action__PlacePiece_GetResult_Event__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_GetResult_Event__Sequence *
project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * array = (project2_interfaces__action__PlacePiece_GetResult_Event__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_GetResult_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__destroy(project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__are_equal(const project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * lhs, const project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_GetResult_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_GetResult_Event__Sequence__copy(
  const project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * input,
  project2_interfaces__action__PlacePiece_GetResult_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_GetResult_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_GetResult_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_GetResult_Event * data =
      (project2_interfaces__action__PlacePiece_GetResult_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_GetResult_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_GetResult_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_GetResult_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "project2_interfaces/action/detail/place_piece__functions.h"

bool
project2_interfaces__action__PlacePiece_FeedbackMessage__init(project2_interfaces__action__PlacePiece_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    project2_interfaces__action__PlacePiece_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!project2_interfaces__action__PlacePiece_Feedback__init(&msg->feedback)) {
    project2_interfaces__action__PlacePiece_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
project2_interfaces__action__PlacePiece_FeedbackMessage__fini(project2_interfaces__action__PlacePiece_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  project2_interfaces__action__PlacePiece_Feedback__fini(&msg->feedback);
}

bool
project2_interfaces__action__PlacePiece_FeedbackMessage__are_equal(const project2_interfaces__action__PlacePiece_FeedbackMessage * lhs, const project2_interfaces__action__PlacePiece_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!project2_interfaces__action__PlacePiece_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_FeedbackMessage__copy(
  const project2_interfaces__action__PlacePiece_FeedbackMessage * input,
  project2_interfaces__action__PlacePiece_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!project2_interfaces__action__PlacePiece_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

project2_interfaces__action__PlacePiece_FeedbackMessage *
project2_interfaces__action__PlacePiece_FeedbackMessage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_FeedbackMessage * msg = (project2_interfaces__action__PlacePiece_FeedbackMessage *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage));
  bool success = project2_interfaces__action__PlacePiece_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project2_interfaces__action__PlacePiece_FeedbackMessage__destroy(project2_interfaces__action__PlacePiece_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project2_interfaces__action__PlacePiece_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__init(project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_FeedbackMessage * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage)) {
      return false;
    }
    data = (project2_interfaces__action__PlacePiece_FeedbackMessage *)allocator.zero_allocate(size, sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project2_interfaces__action__PlacePiece_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project2_interfaces__action__PlacePiece_FeedbackMessage__fini(&data[i - 1]);
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
project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__fini(project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * array)
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
      project2_interfaces__action__PlacePiece_FeedbackMessage__fini(&array->data[i]);
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

project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence *
project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * array = (project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence *)allocator.allocate(sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__destroy(project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__are_equal(const project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * lhs, const project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__copy(
  const project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * input,
  project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(project2_interfaces__action__PlacePiece_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project2_interfaces__action__PlacePiece_FeedbackMessage * data =
      (project2_interfaces__action__PlacePiece_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project2_interfaces__action__PlacePiece_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project2_interfaces__action__PlacePiece_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project2_interfaces__action__PlacePiece_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

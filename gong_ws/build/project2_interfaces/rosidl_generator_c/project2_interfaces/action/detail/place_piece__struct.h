// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project2_interfaces:action/PlacePiece.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "project2_interfaces/action/place_piece.h"


#ifndef PROJECT2_INTERFACES__ACTION__DETAIL__PLACE_PIECE__STRUCT_H_
#define PROJECT2_INTERFACES__ACTION__DETAIL__PLACE_PIECE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_Goal
{
  uint8_t cell_id;
} project2_interfaces__action__PlacePiece_Goal;

// Struct for a sequence of project2_interfaces__action__PlacePiece_Goal.
typedef struct project2_interfaces__action__PlacePiece_Goal__Sequence
{
  project2_interfaces__action__PlacePiece_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_Goal__Sequence;

// Constants defined in the message

/// Constant 'SUCCESS'.
enum
{
  project2_interfaces__action__PlacePiece_Result__SUCCESS = 0
};

/// Constant 'INVALID_CELL'.
enum
{
  project2_interfaces__action__PlacePiece_Result__INVALID_CELL = 1
};

/// Constant 'ROBOT_NOT_READY'.
enum
{
  project2_interfaces__action__PlacePiece_Result__ROBOT_NOT_READY = 2
};

/// Constant 'PLAN_FAILED'.
enum
{
  project2_interfaces__action__PlacePiece_Result__PLAN_FAILED = 3
};

/// Constant 'EXECUTION_FAILED'.
enum
{
  project2_interfaces__action__PlacePiece_Result__EXECUTION_FAILED = 4
};

/// Constant 'NO_PIECES_LEFT'.
enum
{
  project2_interfaces__action__PlacePiece_Result__NO_PIECES_LEFT = 5
};

/// Constant 'CANCELLED'.
enum
{
  project2_interfaces__action__PlacePiece_Result__CANCELLED = 6
};

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_Result
{
  bool success;
  uint8_t error_code;
  rosidl_runtime_c__String message;
} project2_interfaces__action__PlacePiece_Result;

// Struct for a sequence of project2_interfaces__action__PlacePiece_Result.
typedef struct project2_interfaces__action__PlacePiece_Result__Sequence
{
  project2_interfaces__action__PlacePiece_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stage'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_Feedback
{
  rosidl_runtime_c__String stage;
  float progress;
} project2_interfaces__action__PlacePiece_Feedback;

// Struct for a sequence of project2_interfaces__action__PlacePiece_Feedback.
typedef struct project2_interfaces__action__PlacePiece_Feedback__Sequence
{
  project2_interfaces__action__PlacePiece_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "project2_interfaces/action/detail/place_piece__struct.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  project2_interfaces__action__PlacePiece_Goal goal;
} project2_interfaces__action__PlacePiece_SendGoal_Request;

// Struct for a sequence of project2_interfaces__action__PlacePiece_SendGoal_Request.
typedef struct project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence
{
  project2_interfaces__action__PlacePiece_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} project2_interfaces__action__PlacePiece_SendGoal_Response;

// Struct for a sequence of project2_interfaces__action__PlacePiece_SendGoal_Response.
typedef struct project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence
{
  project2_interfaces__action__PlacePiece_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  project2_interfaces__action__PlacePiece_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  project2_interfaces__action__PlacePiece_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence request;
  project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence response;
} project2_interfaces__action__PlacePiece_SendGoal_Event;

// Struct for a sequence of project2_interfaces__action__PlacePiece_SendGoal_Event.
typedef struct project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence
{
  project2_interfaces__action__PlacePiece_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} project2_interfaces__action__PlacePiece_GetResult_Request;

// Struct for a sequence of project2_interfaces__action__PlacePiece_GetResult_Request.
typedef struct project2_interfaces__action__PlacePiece_GetResult_Request__Sequence
{
  project2_interfaces__action__PlacePiece_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "project2_interfaces/action/detail/place_piece__struct.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_GetResult_Response
{
  int8_t status;
  project2_interfaces__action__PlacePiece_Result result;
} project2_interfaces__action__PlacePiece_GetResult_Response;

// Struct for a sequence of project2_interfaces__action__PlacePiece_GetResult_Response.
typedef struct project2_interfaces__action__PlacePiece_GetResult_Response__Sequence
{
  project2_interfaces__action__PlacePiece_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  project2_interfaces__action__PlacePiece_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  project2_interfaces__action__PlacePiece_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  project2_interfaces__action__PlacePiece_GetResult_Request__Sequence request;
  project2_interfaces__action__PlacePiece_GetResult_Response__Sequence response;
} project2_interfaces__action__PlacePiece_GetResult_Event;

// Struct for a sequence of project2_interfaces__action__PlacePiece_GetResult_Event.
typedef struct project2_interfaces__action__PlacePiece_GetResult_Event__Sequence
{
  project2_interfaces__action__PlacePiece_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "project2_interfaces/action/detail/place_piece__struct.h"

/// Struct defined in action/PlacePiece in the package project2_interfaces.
typedef struct project2_interfaces__action__PlacePiece_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  project2_interfaces__action__PlacePiece_Feedback feedback;
} project2_interfaces__action__PlacePiece_FeedbackMessage;

// Struct for a sequence of project2_interfaces__action__PlacePiece_FeedbackMessage.
typedef struct project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence
{
  project2_interfaces__action__PlacePiece_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT2_INTERFACES__ACTION__DETAIL__PLACE_PIECE__STRUCT_H_

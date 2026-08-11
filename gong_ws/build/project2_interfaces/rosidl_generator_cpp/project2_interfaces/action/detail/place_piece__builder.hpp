// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project2_interfaces:action/PlacePiece.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "project2_interfaces/action/place_piece.hpp"


#ifndef PROJECT2_INTERFACES__ACTION__DETAIL__PLACE_PIECE__BUILDER_HPP_
#define PROJECT2_INTERFACES__ACTION__DETAIL__PLACE_PIECE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project2_interfaces/action/detail/place_piece__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_Goal_cell_id
{
public:
  Init_PlacePiece_Goal_cell_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project2_interfaces::action::PlacePiece_Goal cell_id(::project2_interfaces::action::PlacePiece_Goal::_cell_id_type arg)
  {
    msg_.cell_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_Goal>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_Goal_cell_id();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_Result_message
{
public:
  explicit Init_PlacePiece_Result_message(::project2_interfaces::action::PlacePiece_Result & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_Result message(::project2_interfaces::action::PlacePiece_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_Result msg_;
};

class Init_PlacePiece_Result_error_code
{
public:
  explicit Init_PlacePiece_Result_error_code(::project2_interfaces::action::PlacePiece_Result & msg)
  : msg_(msg)
  {}
  Init_PlacePiece_Result_message error_code(::project2_interfaces::action::PlacePiece_Result::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_PlacePiece_Result_message(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_Result msg_;
};

class Init_PlacePiece_Result_success
{
public:
  Init_PlacePiece_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_Result_error_code success(::project2_interfaces::action::PlacePiece_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PlacePiece_Result_error_code(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_Result>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_Result_success();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_Feedback_progress
{
public:
  explicit Init_PlacePiece_Feedback_progress(::project2_interfaces::action::PlacePiece_Feedback & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_Feedback progress(::project2_interfaces::action::PlacePiece_Feedback::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_Feedback msg_;
};

class Init_PlacePiece_Feedback_stage
{
public:
  Init_PlacePiece_Feedback_stage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_Feedback_progress stage(::project2_interfaces::action::PlacePiece_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return Init_PlacePiece_Feedback_progress(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_Feedback>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_Feedback_stage();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_SendGoal_Request_goal
{
public:
  explicit Init_PlacePiece_SendGoal_Request_goal(::project2_interfaces::action::PlacePiece_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_SendGoal_Request goal(::project2_interfaces::action::PlacePiece_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Request msg_;
};

class Init_PlacePiece_SendGoal_Request_goal_id
{
public:
  Init_PlacePiece_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_SendGoal_Request_goal goal_id(::project2_interfaces::action::PlacePiece_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PlacePiece_SendGoal_Request_goal(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_SendGoal_Request>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_SendGoal_Request_goal_id();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_SendGoal_Response_stamp
{
public:
  explicit Init_PlacePiece_SendGoal_Response_stamp(::project2_interfaces::action::PlacePiece_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_SendGoal_Response stamp(::project2_interfaces::action::PlacePiece_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Response msg_;
};

class Init_PlacePiece_SendGoal_Response_accepted
{
public:
  Init_PlacePiece_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_SendGoal_Response_stamp accepted(::project2_interfaces::action::PlacePiece_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_PlacePiece_SendGoal_Response_stamp(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_SendGoal_Response>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_SendGoal_Response_accepted();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_SendGoal_Event_response
{
public:
  explicit Init_PlacePiece_SendGoal_Event_response(::project2_interfaces::action::PlacePiece_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_SendGoal_Event response(::project2_interfaces::action::PlacePiece_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Event msg_;
};

class Init_PlacePiece_SendGoal_Event_request
{
public:
  explicit Init_PlacePiece_SendGoal_Event_request(::project2_interfaces::action::PlacePiece_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_PlacePiece_SendGoal_Event_response request(::project2_interfaces::action::PlacePiece_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_PlacePiece_SendGoal_Event_response(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Event msg_;
};

class Init_PlacePiece_SendGoal_Event_info
{
public:
  Init_PlacePiece_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_SendGoal_Event_request info(::project2_interfaces::action::PlacePiece_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_PlacePiece_SendGoal_Event_request(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_SendGoal_Event>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_SendGoal_Event_info();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_GetResult_Request_goal_id
{
public:
  Init_PlacePiece_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project2_interfaces::action::PlacePiece_GetResult_Request goal_id(::project2_interfaces::action::PlacePiece_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_GetResult_Request>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_GetResult_Request_goal_id();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_GetResult_Response_result
{
public:
  explicit Init_PlacePiece_GetResult_Response_result(::project2_interfaces::action::PlacePiece_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_GetResult_Response result(::project2_interfaces::action::PlacePiece_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_GetResult_Response msg_;
};

class Init_PlacePiece_GetResult_Response_status
{
public:
  Init_PlacePiece_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_GetResult_Response_result status(::project2_interfaces::action::PlacePiece_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_PlacePiece_GetResult_Response_result(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_GetResult_Response>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_GetResult_Response_status();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_GetResult_Event_response
{
public:
  explicit Init_PlacePiece_GetResult_Event_response(::project2_interfaces::action::PlacePiece_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_GetResult_Event response(::project2_interfaces::action::PlacePiece_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_GetResult_Event msg_;
};

class Init_PlacePiece_GetResult_Event_request
{
public:
  explicit Init_PlacePiece_GetResult_Event_request(::project2_interfaces::action::PlacePiece_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_PlacePiece_GetResult_Event_response request(::project2_interfaces::action::PlacePiece_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_PlacePiece_GetResult_Event_response(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_GetResult_Event msg_;
};

class Init_PlacePiece_GetResult_Event_info
{
public:
  Init_PlacePiece_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_GetResult_Event_request info(::project2_interfaces::action::PlacePiece_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_PlacePiece_GetResult_Event_request(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_GetResult_Event>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_GetResult_Event_info();
}

}  // namespace project2_interfaces


namespace project2_interfaces
{

namespace action
{

namespace builder
{

class Init_PlacePiece_FeedbackMessage_feedback
{
public:
  explicit Init_PlacePiece_FeedbackMessage_feedback(::project2_interfaces::action::PlacePiece_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::project2_interfaces::action::PlacePiece_FeedbackMessage feedback(::project2_interfaces::action::PlacePiece_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_FeedbackMessage msg_;
};

class Init_PlacePiece_FeedbackMessage_goal_id
{
public:
  Init_PlacePiece_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlacePiece_FeedbackMessage_feedback goal_id(::project2_interfaces::action::PlacePiece_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PlacePiece_FeedbackMessage_feedback(msg_);
  }

private:
  ::project2_interfaces::action::PlacePiece_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::project2_interfaces::action::PlacePiece_FeedbackMessage>()
{
  return project2_interfaces::action::builder::Init_PlacePiece_FeedbackMessage_goal_id();
}

}  // namespace project2_interfaces

#endif  // PROJECT2_INTERFACES__ACTION__DETAIL__PLACE_PIECE__BUILDER_HPP_


#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_Goal() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_Goal__init(msg: *mut PlacePiece_Goal) -> bool;
    fn project2_interfaces__action__PlacePiece_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Goal>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Goal>);
    fn project2_interfaces__action__PlacePiece_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Goal>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub cell_id: u8,

}



impl Default for PlacePiece_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_Goal__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_Goal() }
  }
}


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_Result() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_Result__init(msg: *mut PlacePiece_Result) -> bool;
    fn project2_interfaces__action__PlacePiece_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Result>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Result>);
    fn project2_interfaces__action__PlacePiece_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Result>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}

impl PlacePiece_Result {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SUCCESS: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_CELL: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ROBOT_NOT_READY: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PLAN_FAILED: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EXECUTION_FAILED: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NO_PIECES_LEFT: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CANCELLED: u8 = 6;

}


impl Default for PlacePiece_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_Result__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_Result where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_Result() }
  }
}


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_Feedback__init(msg: *mut PlacePiece_Feedback) -> bool;
    fn project2_interfaces__action__PlacePiece_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Feedback>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Feedback>);
    fn project2_interfaces__action__PlacePiece_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_Feedback>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub progress: f32,

}



impl Default for PlacePiece_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_Feedback__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_Feedback() }
  }
}


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_FeedbackMessage__init(msg: *mut PlacePiece_FeedbackMessage) -> bool;
    fn project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_FeedbackMessage>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_FeedbackMessage>);
    fn project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_FeedbackMessage>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::PlacePiece_Feedback,

}



impl Default for PlacePiece_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_FeedbackMessage() }
  }
}




#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_SendGoal_Request__init(msg: *mut PlacePiece_SendGoal_Request) -> bool;
    fn project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Request>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Request>);
    fn project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Request>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::PlacePiece_Goal,

}



impl Default for PlacePiece_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_SendGoal_Request() }
  }
}


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_SendGoal_Response__init(msg: *mut PlacePiece_SendGoal_Response) -> bool;
    fn project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Response>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Response>);
    fn project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_SendGoal_Response>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for PlacePiece_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_SendGoal_Response() }
  }
}


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_GetResult_Request__init(msg: *mut PlacePiece_GetResult_Request) -> bool;
    fn project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Request>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Request>);
    fn project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Request>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for PlacePiece_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_GetResult_Request() }
  }
}


#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "project2_interfaces__rosidl_generator_c")]
extern "C" {
    fn project2_interfaces__action__PlacePiece_GetResult_Response__init(msg: *mut PlacePiece_GetResult_Response) -> bool;
    fn project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Response>, size: usize) -> bool;
    fn project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Response>);
    fn project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<PlacePiece_GetResult_Response>) -> bool;
}

// Corresponds to project2_interfaces__action__PlacePiece_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlacePiece_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::PlacePiece_Result,

}



impl Default for PlacePiece_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !project2_interfaces__action__PlacePiece_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to project2_interfaces__action__PlacePiece_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlacePiece_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { project2_interfaces__action__PlacePiece_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlacePiece_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlacePiece_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "project2_interfaces/action/PlacePiece_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__project2_interfaces__action__PlacePiece_GetResult_Response() }
  }
}






#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__project2_interfaces__action__PlacePiece_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to project2_interfaces__action__PlacePiece_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct PlacePiece_SendGoal;

impl rosidl_runtime_rs::Service for PlacePiece_SendGoal {
    type Request = PlacePiece_SendGoal_Request;
    type Response = PlacePiece_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__project2_interfaces__action__PlacePiece_SendGoal() }
    }
}




#[link(name = "project2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__project2_interfaces__action__PlacePiece_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to project2_interfaces__action__PlacePiece_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct PlacePiece_GetResult;

impl rosidl_runtime_rs::Service for PlacePiece_GetResult {
    type Request = PlacePiece_GetResult_Request;
    type Response = PlacePiece_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__project2_interfaces__action__PlacePiece_GetResult() }
    }
}



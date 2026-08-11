# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target project2_interfaces::project2_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${project2_interfaces_TARGETS}.
if(project2_interfaces_TARGETS AND NOT TARGET project2_interfaces::project2_interfaces)
  add_library(project2_interfaces::project2_interfaces INTERFACE IMPORTED)
  set_target_properties(project2_interfaces::project2_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${project2_interfaces_TARGETS}")
endif()

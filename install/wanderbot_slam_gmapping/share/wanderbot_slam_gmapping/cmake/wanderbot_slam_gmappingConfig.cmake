# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_wanderbot_slam_gmapping_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED wanderbot_slam_gmapping_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(wanderbot_slam_gmapping_FOUND FALSE)
  elseif(NOT wanderbot_slam_gmapping_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(wanderbot_slam_gmapping_FOUND FALSE)
  endif()
  return()
endif()
set(_wanderbot_slam_gmapping_CONFIG_INCLUDED TRUE)

# output package information
if(NOT wanderbot_slam_gmapping_FIND_QUIETLY)
  message(STATUS "Found wanderbot_slam_gmapping: 0.0.0 (${wanderbot_slam_gmapping_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'wanderbot_slam_gmapping' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${wanderbot_slam_gmapping_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(wanderbot_slam_gmapping_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${wanderbot_slam_gmapping_DIR}/${_extra}")
endforeach()

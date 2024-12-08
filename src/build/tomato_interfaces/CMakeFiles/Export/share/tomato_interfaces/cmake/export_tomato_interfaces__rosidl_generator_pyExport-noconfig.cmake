#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tomato_interfaces::tomato_interfaces__rosidl_generator_py" for configuration ""
set_property(TARGET tomato_interfaces::tomato_interfaces__rosidl_generator_py APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(tomato_interfaces::tomato_interfaces__rosidl_generator_py PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libtomato_interfaces__rosidl_generator_py.so"
  IMPORTED_SONAME_NOCONFIG "libtomato_interfaces__rosidl_generator_py.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS tomato_interfaces::tomato_interfaces__rosidl_generator_py )
list(APPEND _IMPORT_CHECK_FILES_FOR_tomato_interfaces::tomato_interfaces__rosidl_generator_py "${_IMPORT_PREFIX}/lib/libtomato_interfaces__rosidl_generator_py.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

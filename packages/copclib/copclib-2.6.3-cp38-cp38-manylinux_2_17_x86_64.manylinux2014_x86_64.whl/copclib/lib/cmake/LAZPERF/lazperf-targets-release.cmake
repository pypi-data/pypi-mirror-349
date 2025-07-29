#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LAZPERF::lazperf" for configuration "Release"
set_property(TARGET LAZPERF::lazperf APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(LAZPERF::lazperf PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/liblazperf.so"
  IMPORTED_SONAME_RELEASE "liblazperf.so"
  )

list(APPEND _cmake_import_check_targets LAZPERF::lazperf )
list(APPEND _cmake_import_check_files_for_LAZPERF::lazperf "${_IMPORT_PREFIX}/lib/liblazperf.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

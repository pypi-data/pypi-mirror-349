# This is version 2.13
#
# 2.3 does not show up for some reason
# I reorganized the package for Version 2.0
# 2.1 added some functions I forgot to add
# 2.2 - 2.4 had to be made because I fucked the required packages up
#       Apparently, packages os and time could not be installed?
# 2.4 did not work because internal scripts could not import each other
# 2.5 fixed that
# 2.6 - I forgot to put everything into packages for all previous 2.x versions. Fixed that
# 2.7 Same as before, my fix did not work for some reason
# 2.8
#   Added some functions to filestuff for working with paths
#   Added helpers file for small useful functions
#   Added functions to helpers for replacing/removing multiple substrings in one command
# 2.9
#   Added SafetySwitch file
# 2.10
#   Added str_len function to helpers
#   Added merge_list function to helpers
#   Added Debug.py file
# 2.11
#   Some minor fixes
# 2.12
#   Added get_project_root_path function to filestuff
# 2.13
#   Removed merge_list function from helpers, because merge_list(<list>, <str>) does the same as '<str>'.join(<list>)
#   Commented, fixed some bugs and optimized the Tree class in Tree.py (which I added some time before but forgot to list here)


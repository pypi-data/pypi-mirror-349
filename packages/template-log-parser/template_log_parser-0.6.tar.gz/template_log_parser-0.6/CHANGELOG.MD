#### 0.3
---
-Various bug fixes.

-Added support for PiHole, Open Media Vault, and Debian.

#### 0.4
---
-Consolidated all built-in log file types to use `built_in_process_log()` for simplification (Breaking change).
Named function calls from version < 0.4 will need to be replaced with this function from the built_ins module.

#### 0.5
---
-Improved exception handling for additional column functions.

-Added support for PFSense (syslog format).

-Addition of type hints matching docstrings.

#### 0.6
---
-Revised docstrings and improved type hints

-Template tweaks and updates for built-ins (potential breaking changes; the number of Debian templates has been greatly reduced for simplification)

-Addition of optional `match` and `eliminate` parameters to applicable log_functions; filter log files prior to parsing (No Breaking Changes)

-Addition of functions `tag_and_or_combine_lines()` and `link_log_file_lines()` to aid in verbose outputs that span multiple lines.

-Added preliminary support for Kodi.

-Modified `parse_function()` to use compiled templates for small performance gain (No Breaking Changes). 
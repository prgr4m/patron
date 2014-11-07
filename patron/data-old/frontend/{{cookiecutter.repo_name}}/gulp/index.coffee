# index.coffee
# =============================================================================
# I could just use a loop from reading the filesystem but I want to be explicit
# when setting this up for the first time

require "./tasks/assets"
require "./tasks/default"
require "./tasks/jade"
require "./tasks/sass"
require "./tasks/scripts"
require "./tasks/server"
require "./tasks/watch"
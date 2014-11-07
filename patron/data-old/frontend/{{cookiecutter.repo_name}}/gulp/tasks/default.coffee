# default.coffee
# =============================================================================
gulp = require "gulp"

# if I need tasks to execute in order then I should npm install 'run-sequence'
gulp.task "default", [
  'jade'
  'sass'
  'images'
  'fonts'
  'root_images'
  'root_assets'
  'coffee'
  'vendor'
  'watch'
  'server'
]
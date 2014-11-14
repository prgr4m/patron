# default.coffee
# =============================================================================
gulp = require "gulp"

# if I need tasks to execute in order then I should npm install 'run-sequence'
gulp.task "default", [
  'sass'
  'images'
  'fonts'
  'coffee'
  'vendor'
  'app-jade'
  'app-coffee'
  'watch'
  'server-proxy'
]

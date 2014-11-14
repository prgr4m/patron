# watch.coffee
# =============================================================================
gulp = require "gulp"
config = require "../config"

gulp.task "watch", ->
  gulp.watch "#{config.input_dir}/templates/**/*.jade", ['jade']
  gulp.watch [
    "#{config.input_dir}/coffee/**/*.coffee"
    "!#{config.input_dir}/coffee/vendor/**/*.js"
  ], ['coffee']
  gulp.watch "#{config.input_dir}/coffee/vendor/**/*.js", ['vendor']
  gulp.watch "#{config.input_dir}/sass/**/*.sass", ['sass']
  gulp.watch "#{config.input_dir}/assets/img/**/*", ['images']
  gulp.watch "#{config.input_dir}/assets/fonts/**/*", ['fonts']
  gulp.watch "#{config.input_dir}/app/**/*.jade", ['app-jade']
  gulp.watch "#{config.input_dir}/app/**/*.coffee", ['app-coffee']
  return

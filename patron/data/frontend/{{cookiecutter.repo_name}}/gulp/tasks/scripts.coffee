# scripts.coffee
# =============================================================================
gulp = require "gulp"
rjs = require "gulp-requirejs"
coffee = require "gulp-coffee"
notify = require "gulp-notify"
uglify = require "gulp-uglify"
server = require "./server"

config = require "../config"

gulp.task "coffee", ->
  gulp.src "#{config.input_dir}/coffee/**/*.coffee"
    .pipe coffee bare: on
    .on "error", ->
      notify.onError
        title: "CoffeeScript Compile Error"
        message: "<%= error.message %>"
      .apply @, arguments
      @emit "end"
    .pipe uglify()
    # .pipe gulp.dest "#{config.output_dir}/js"
    .pipe server.reload stream: on
  return

gulp.task "vendor", ->
  gulp.src "#{config.input_dir}/coffee/vendor/**/*.js"
    .pipe gulp.dest "#{config.output_dir}/js/vendor"
  return

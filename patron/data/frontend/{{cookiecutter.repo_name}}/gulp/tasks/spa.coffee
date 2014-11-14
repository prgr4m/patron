# spa.coffee
# =============================================================================
gulp = require "gulp"
jade = require "gulp-jade"
coffee = require "gulp-coffee"
uglify = require "gulp-uglify"
rjs = require "gulp-requirejs"
notify = require "gulp-notify"

config = require "../config"
server = require "./server"

src_dir = "#{config.input_dir}/app"
target_dir = "#{config.output_dir}/app"

# jade compilation of app dir
# =============================================================================
gulp.task "app-jade", ->
  gulp.src "#{src_dir}/**/*.jade"
    .pipe jade()
    .on "error", ->
      notify.onError
        title: "Jade Compile Error"
        message: "<%= error.message %>"
      .apply @, arguments
      @emit "end"
    .pipe gulp.dest target_dir
  return

# coffeescript compilation of app dir
# =============================================================================
gulp.task "app-coffee", ->
  gulp.src "#{src_dir}/**/*.coffee"
    .pipe coffee bare: on
    .on "error", ->
      notify.onError
        title: "CoffeeScript Compile Error"
        message: "<%= error.message %>"
      .apply @, arguments
      @emit "end"
    .pipe gulp.dest target_dir
    .pipe server.reload stream: on
  return

# requirejs
# =============================================================================
gulp.task "rjs", ['coffee'], ->
  rjs config.rjs
    .pipe uglify()
  .pipe gulp.dest target_dir
  return

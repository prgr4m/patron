# sass.coffee
# =============================================================================
gulp = require "gulp"
sass = require "gulp-ruby-sass"
notify = require "gulp-notify"
server = require "./server"

config = require "../config"

gulp.task "sass", ->
  sass_conf =
    unixNewlines: on
    style: "compressed"

  gulp.src "#{config.input_dir}/sass/main.sass"
    .pipe sass sass_conf
    .on "error", ->
      notify.onError
        title: "Sass Compile Error"
        message: "<%= error.message %>"
      .apply @, arguments
      @emit "end"
    .pipe gulp.dest "#{config.output_dir}/css"
    .pipe server.reload stream: on
  return

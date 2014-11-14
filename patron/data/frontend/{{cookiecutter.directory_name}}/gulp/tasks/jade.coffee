# jade.coffee
# =============================================================================
gulp = require "gulp"
jade = require "gulp-jade"
notify = require "gulp-notify"
server = require "./server"

config = require "../config"

gulp.task "jade", ->
  gulp.src "#{config.input_dir}/templates/**/*.jade"
    .pipe jade()
    .on "error", ->
      notify.onError
        title: "Jade Compile Error"
        message: "<%= error.message %>"
      .apply @, arguments
      @emit "end"
    .pipe gulp.dest config.output_dir
    .pipe server.reload stream: on
  return

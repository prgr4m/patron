# watch.coffee
# =============================================================================
gulp = require "gulp"
server = require "./server"

gulp.task "watch", ->
  gulp.watch "app/templates/**/*.jade", ['jade']
  gulp.watch ["app/coffee/**/*.coffee", "!app/coffee/vendor/**/*.js"], ['coffee']
  gulp.watch "app/coffee/vendor/**/*.js", ['vendor']
  gulp.watch "app/sass/**/*.sass", ['sass']
  gulp.watch "app/assets/img/**/*", ['images']
  gulp.watch "app/assets/fonts/**/*", ['fonts']
  gulp.watch "./{{cookiecutter.project_name}}/**/*.jade", ['', server.reload]
  return

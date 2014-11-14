# assets.coffee
# =============================================================================
gulp = require "gulp"
imagemin = require "gulp-imagemin"

config = require "../config"

# images
gulp.task "images", ->
  gulp.src "#{config.input_dir}/assets/img/**/*"
    .pipe imagemin optimizationLevel: 5
    .pipe gulp.dest "#{config.output_dir}/img"
  return

# fonts
gulp.task "fonts", ->
  gulp.src "#{config.input_dir}/assets/fonts/**/*"
    .pipe gulp.dest "#{config.output_dir}/fonts"
  return

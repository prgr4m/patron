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

# root assets
gulp.task "root_images", ->
  gulp.src "#{config.input_dir}/assets/*.png"
    .pipe imagemin optimizationLevel: 5
    .pipe gulp.dest "#{config.output_dir}"
  return

gulp.task "root_assets", ->
  src_globs = [
    "#{config.input_dir}/assets/*.txt"
    "#{config.input_dir}/assets/*.xml"
    "#{config.input_dir}/assets/*.ico"
  ]
  gulp.src src_globs
    .pipe gulp.dest "#{config.output_dir}"
  return

# server.coffee
# =============================================================================
gulp = require "gulp"
browser_sync = require "browser-sync"

config = require "../config"

browser_sync_config =
  baseDir: "#{config.output_dir}"
  directory: off
  index: "index.html"
  online: off
  open: off
  notify: off

gulp.task "server", ->
  browser_sync
    proxy: "http://#{config.proxy.host}:#{config.proxy.port}"
  return

module.exports =
  reload: browser_sync.reload

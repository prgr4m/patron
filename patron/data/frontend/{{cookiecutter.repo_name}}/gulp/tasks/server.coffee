# server.coffee
# =============================================================================
gulp = require "gulp"
browser_sync = require "browser-sync"

config = require "../config"

gulp.task "server-proxy", ->
  browser_sync
    proxy: "http://#{config.proxy.host}:#{config.proxy.port}"
  return

module.exports =
  reload: browser_sync.reload

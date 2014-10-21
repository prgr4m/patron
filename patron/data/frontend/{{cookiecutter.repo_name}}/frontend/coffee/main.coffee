require.config
  baseUrl: "/js"
  paths:
    jquery: "vendor/jquery"
  shim:
    jquery: exports: "$"

require [

], ()->
  console.log "make your requires and write some code..."
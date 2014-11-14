require.config
  baseUrl: "/js"
  paths:
    ${paths}
  shim:
    ${shims}

require [

], ()->
  console.log "make your requires and write some code..."

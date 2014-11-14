# config.coffee
# =============================================================================
# This file holds configuration settings for the build system
# =============================================================================
env = if process.env.NODE_ENV then process.env.NODE_ENV else "development"
input_dir = "./frontend"
output_dir = "./{{cookiecutter.project_name}}/static"

# should eventually add arg parsing to set proxy and server host names
# ex: 0.0.0.0 so the server can receive external requests
module.exports =
  env: env
  input_dir: input_dir
  output_dir: output_dir
  proxy:
    host: "localhost"
    port: 5000
    route: "/api"
  rjs:
    baseUrl: "#{output_dir}/app"
    out: "main-built.js"
    paths:
      ${paths}
    shim:
      ${shims}

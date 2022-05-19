### Migration steps
1. `Cloud Code: New Application`: New Cloud Run Python Flask application
1. Converge file systems
1. Define `.dockerignore`, `.gitignore`, and `.gcloudignore` files. 
1. Remove setting `PORT` environment variables. Update ports to 8080. 
1. Update Flask app invocation to remove `debug=true`.
1. Add launch config to run python file locally, add environment variables, test.
1. Update scripts to build image and run locally and set environment variables in `run-image-locally.sh`.
1. Move `run-image-locally.sh` to `.vscode` to it doesn't get committed. 
1. Rename scripts to be consistent. 
1. Do not create a `Zsh` launch config to start the script to build and run locally. Extension does not permit `Ctrl-C` to terminate the app. Instead, run from a terminal. 
1. Create `Clode Code: Debug on Cloud Run Emulator`: Debug (or Run) image locally. Add environment variables in advanced setting or in `launch.json`.
1. `Cloud Code: Deploy to Cloud Run`: Depoy changes


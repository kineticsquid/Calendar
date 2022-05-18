#!/bin/bash

# Run this to create or re-deploy the function
gcloud run deploy calendar --allow-unauthenticated --project cloud-run-stuff --region us-central1 \
  --source ./ 
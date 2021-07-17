# Execute this command in main-cloud-run folder
# Set Environment Variables
GOOGLE_CLOUD_PROJECT=the-sentinel-project-320007

# Build Container of main-cloud-run API
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/the-sentinel-api

# Deploy cloud run main-cloud-run
gcloud beta run deploy the-sentinel-api \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/the-sentinel-api \
  --platform managed \
  --no-allow-unauthenticated
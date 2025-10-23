# Google Calendar Setup

## 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API

## 2. Create Credentials

1. Go to "Credentials" in the Google Cloud Console
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Download the JSON file and save it as `credentials.json` in the API directory

## 3. Environment Variables

Add these environment variables to your `.env` file:

```bash
# Google Calendar Configuration
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_TOKEN_PATH=token.json
GOOGLE_CALENDAR_ID=primary
CLINIC_TIMEZONE=America/Sao_Paulo
```

## 4. First Run

On the first run, the application will:
1. Open a browser window for Google OAuth authentication
2. Save the authentication token to `token.json`
3. Use this token for subsequent API calls

## 5. Calendar ID

- Use `primary` for the main calendar
- Or use a specific calendar ID from Google Calendar settings

## 6. Timezone

Set `CLINIC_TIMEZONE` to your clinic's timezone (e.g., `America/Sao_Paulo`, `America/New_York`)

## Security Notes

- Never commit `credentials.json` or `token.json` to version control
- Add these files to `.gitignore`
- Use environment variables for production deployments

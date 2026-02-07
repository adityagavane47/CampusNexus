# OAuth Setup Guide for CampusNexus

This guide will help you set up Google and GitHub OAuth authentication for your CampusNexus application.

## Prerequisites
- A Google Cloud account
- A GitHub account
- CampusNexus backend running on `http://localhost:8000`
- CampusNexus frontend running on `http://localhost:5173`

---

## Google OAuth Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter project name: `CampusNexus` (or your preferred name)
5. Click "Create"

### Step 2: Enable Google People API

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google People API"
3. Click on it and click "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: CampusNexus
   - User support email: Your email
   - Developer contact: Your email
   - Save and Continue through the scopes and test users screens
4. Back on "Create OAuth client ID":
   - Application type: Web application
   - Name: CampusNexus Web
   - Authorized redirect URIs:
     - `http://localhost:8000/api/oauth/google/callback`
   - Click "Create"
5. **Copy your Client ID and Client Secret** - you'll need these!

---

## GitHub OAuth Setup

### Step 1: Create a GitHub OAuth App

1. Go to [GitHub Settings > Developer Settings](https://github.com/settings/developers)
2. Click on "OAuth Apps"
3. Click "New OAuth App"

### Step 2: Configure the OAuth App

Fill in the following details:
- **Application name:** CampusNexus
- **Homepage URL:** `http://localhost:5173`
- **Application description:** Campus ecosystem for VIT Pune (optional)
- **Authorization callback URL:** `http://localhost:8000/api/oauth/github/callback`

### Step 3: Generate Client Secret

1. After creating the app, you'll see your **Client ID**
2. Click "Generate a new client secret"
3. **Copy both the Client ID and Client Secret** - you'll need these!

---

## Configure Your Backend

### Step 1: Create .env File

In your `backend` directory, create a `.env` file (if it doesn't exist):

```bash
cd d:\CAMPUSNEXUS\backend
copy .env.example .env
```

### Step 2: Add OAuth Credentials

Open the `.env` file and add your credentials:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id-here
GITHUB_CLIENT_SECRET=your-github-client-secret-here
```

**Important:** Replace the placeholder values with your actual credentials!

### Step 3: Restart the Backend Server

If your backend server is running, restart it to load the new environment variables:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
uvicorn app.main:app --reload
```

---

## Testing the OAuth Flow

### Step 1: Open the Application

Navigate to `http://localhost:5173` in your browser.

### Step 2: Test Google OAuth

1. Click "Continue with Google"
2. You'll be redirected to Google's login page
3. Sign in with your Google account
4. Grant permissions when prompted
5. You'll be redirected back to CampusNexus, logged in!

### Step 3: Test GitHub OAuth

1. Log out if you're logged in
2. Click "Continue with GitHub"
3. You'll be redirected to GitHub's authorization page
4. Click "Authorize" to grant permissions
5. You'll be redirected back to CampusNexus, logged in!

---

## Troubleshooting

### "OAuth not configured" Error
- Make sure you've added the credentials to your `.env` file
- Verify the environment variables are not empty strings
- Restart the backend server after adding credentials

### Redirect URI Mismatch
- Double-check that the redirect URIs in Google/GitHub match exactly:
  - Google: `http://localhost:8000/api/oauth/google/callback`
  - GitHub: `http://localhost:8000/api/oauth/github/callback`
- Make sure there are no trailing slashes

### "Authentication failed" Error
- Check the browser console for detailed error messages
- Verify your Client ID and Client Secret are correct
- Make sure the OAuth app is not restricted to specific domains

---

## Production Deployment

When deploying to production, you'll need to:

1. **Update Redirect URIs** in both Google and GitHub:
   - Google: `https://yourdomain.com/api/oauth/google/callback`
   - GitHub: `https://yourdomain.com/api/oauth/github/callback`

2. **Update Environment Variables**:
   ```bash
   FRONTEND_URL=https://yourdomain.com
   OAUTH_REDIRECT_URI=https://yourdomain.com/api/oauth
   ```

3. **Use HTTPS** - OAuth providers require HTTPS for production

4. **Update OAuth Consent Screen** (Google):
   - Change from "Testing" to "Production"
   - Add privacy policy and terms of service URLs

---

## Security Notes

⚠️ **Important Security Reminders:**

- Never commit your `.env` file to version control
- Keep your Client Secrets confidential
- Use different OAuth apps for development and production
- Regularly rotate your client secrets
- Monitor OAuth app usage in Google/GitHub dashboards

---

## Support

If you encounter any issues:
1. Check the backend logs for error messages
2. Verify all URLs match exactly
3. Make sure your backend and frontend are running
4. Clear browser cookies and try again

For more help, refer to:
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps)

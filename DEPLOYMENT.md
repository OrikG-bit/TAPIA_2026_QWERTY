# Deployment Guide - Streamlit Cloud

## 🚀 Deploy to Streamlit Cloud (Free!)

### Step 1: Prepare Your GitHub Repository

Your code is already on GitHub at: `https://github.com/OrikG-bit/TAPIA_2026_QWERTY`

Make sure the latest code is pushed:
```bash
git add .
git commit -m "prepare for deployment"
git push origin main
```

### Step 2: Sign Up for Streamlit Cloud

1. Go to: https://streamlit.io/cloud
2. Click **"Sign up"** or **"Get started"**
3. Sign in with your **GitHub account**
4. Authorize Streamlit to access your repositories

### Step 3: Deploy Your App

1. Click **"New app"** button

2. Fill in the deployment settings:
   - **Repository:** `OrikG-bit/TAPIA_2026_QWERTY`
   - **Branch:** `main`
   - **Main file path:** `Streamlit.py`

3. Click **"Advanced settings"** (optional but recommended):
   - **Python version:** `3.11` or higher
   - Leave other settings as default

4. Click **"Deploy!"**

### Step 4: Add Your API Key (CRITICAL!)

⚠️ **Your app won't work without this step!**

1. Once deployed, click **"⚙️ Settings"** (gear icon in bottom right)

2. Go to **"Secrets"** tab

3. Add your OpenRouter API key:
   ```toml
   LLM_API_KEY = "sk-or-v1-YOUR-KEY-HERE"
   ```
   
   **Replace `YOUR-KEY-HERE` with your actual OpenRouter API key!**

4. Click **"Save"**

5. Your app will automatically reboot with the secret

### Step 5: Share Your App

Your app will have a URL like:
```
https://tapia-2026-qwerty.streamlit.app
```

**Share this URL with:**
- Judges
- Your team
- Anyone who wants to try it!

---

## 🔧 Managing Your Deployment

### Update Your App

Just push to GitHub:
```bash
git add .
git commit -m "update app"
git push origin main
```

Streamlit Cloud auto-deploys within 1-2 minutes!

### View Logs

1. Go to your app dashboard
2. Click **"Manage app"**
3. View **"Logs"** tab for errors

### Reboot App

If something goes wrong:
1. Click **"⚙️ Settings"**
2. Click **"Reboot app"**

### Delete App

1. Click **"⚙️ Settings"**
2. Click **"Delete app"**
3. Confirm deletion

---

## 🐛 Troubleshooting Deployment

### "Module not found" errors

Check `requirements.txt` includes all packages:
```
openai
python-dotenv
streamlit
```

### "LLM_API_KEY not set"

Make sure you added the secret in Step 4!

### App keeps crashing

1. Check logs for errors
2. Test locally first: `streamlit run Streamlit.py`
3. Make sure `.gitignore` doesn't exclude important files

### API calls failing

- Verify your OpenRouter API key is valid
- Check you have credits remaining
- Test the key locally first

---

## 💰 Cost & Limits (Streamlit Cloud Free Tier)

**Free tier includes:**
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Shared CPU
- ✅ Auto-sleep after inactivity
- ✅ Community support

**Perfect for:**
- Demos
- Hackathons
- Prototypes
- Small projects

**Costs for API:**
- OpenRouter API calls use your $100 credit
- Streamlit hosting is FREE

---

## 🎯 For Your Demo

### Test Before Judges Arrive

1. Deploy the app
2. Open the URL
3. Go through full flow:
   - Generate materials
   - Take quiz
   - Check missed topics
4. Make sure everything works!

### During Demo

**Option 1: Show live deployed app**
- Judges can interact directly
- No setup needed
- Professional look

**Option 2: Run locally**
- Faster response times
- No internet dependency
- More control

**Recommendation:** Show deployed version first, have local backup ready

---

## 📱 Sharing Options

### Public URL
```
https://your-app-name.streamlit.app
```
Anyone with the link can access it!

### QR Code
1. Go to https://qr.io/
2. Enter your app URL
3. Download QR code
4. Add to presentation slides

### Embed in Presentation
```html
<iframe src="https://your-app-name.streamlit.app" width="800" height="600"></iframe>
```

---

## 🎉 After Deployment Checklist

- [ ] App deployed successfully
- [ ] API key added to secrets
- [ ] Test generation with sample chapter
- [ ] Test quiz submission
- [ ] Test missed topics page
- [ ] Verify memory persists
- [ ] Share URL with team
- [ ] Add URL to GitHub README
- [ ] Test on mobile device
- [ ] Practice demo with live URL

---

## 📞 Support

**Streamlit Cloud Issues:**
- Docs: https://docs.streamlit.io/streamlit-community-cloud
- Forum: https://discuss.streamlit.io/
- Status: https://streamlitstatus.com/

**Your App Issues:**
- Check logs in Streamlit dashboard
- Test locally first
- Review error messages

---

## 🚀 You're Ready to Deploy!

Follow the steps above and your app will be live in under 5 minutes!

**Good luck with your demo! 🎉**

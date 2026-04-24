# SpeakingWells

**Because everyone deserves to be noticed.**

A nonprofit platform that gives non-verbal individuals a simple card to hand to anyone they meet. When someone receives a card, they scan a QR code to send a message back — which goes straight to the family's inbox.

Inspired by Brogan Wells, who hands out cards wherever he goes.

---

## Tech Stack

| Layer | Service |
|---|---|
| Backend | FastAPI (Python) |
| Database | Supabase (Postgres) |
| Hosting | Render.com |
| Email | Resend |
| Inbox | Proton Mail |
| Domain | Namecheap |
| Version Control | GitHub |
| Local Environment | Anaconda (env: speakingwells) |
| Machine | bananas (Linux desktop) |

---

## Accounts & Credentials

### Domain
- **Registrar:** Namecheap
- **Domain:** speakingwells.org
- **Also owns:** wellsnoticed.org (redirects to speakingwells.org)

### Hosting
- **Render.com** — runs FastAPI backend
- **Plan:** Paid tier (always on)
- **Auto-deploys** from GitHub on push to main

### Database
- **Supabase**
- **Project URL:** https://lbwwucvxgyszmjjexhds.supabase.co
- **Project name:** Speakingwells database

### Email Sending
- **Resend.com**
- **From address:** hello@speakingwells.org
- **Domain:** verified and authenticated

### Email Receiving
- **Proton Mail** (paid plan)
- **Addresses:**
  - hello@speakingwells.org
  - brodie@speakingwells.org
- **Admin notifications go to:** brodie@speakingwells.org

### GitHub
- **Username:** tattonchantry
- **Repo:** tattonchantry/speakingwells (private)
- **Auth:** Personal access token with credential.helper store

---

## Environment Variables (.env)

```
SUPABASE_URL=https://lbwwucvxgyszmjjexhds.supabase.co
SUPABASE_KEY=your_anon_key
SECRET_KEY=your_secret_key
RESEND_API_KEY=your_resend_key
FROM_EMAIL=hello@speakingwells.org
ADMIN_EMAIL=brodie@speakingwells.org
```

These are also set in Render's environment variables dashboard.

---

## Project Structure

```
speakingwells/
├── .env                          # Never committed to GitHub
├── .gitignore
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI routes
│   ├── database.py               # Supabase connection
│   ├── models.py                 # Pydantic models
│   ├── auth.py                   # JWT auth, password hashing
│   ├── email.py                  # Resend email functions
│   └── qr.py                     # QR code generation
└── frontend/
    ├── index.html                # Homepage
    ├── setup.html                # Card setup after registration
    ├── welcome.html              # Post-setup welcome page
    ├── login.html                # Sign in
    ├── dashboard.html            # Family dashboard
    ├── verified.html             # Email verification success
    ├── forgot-password.html      # Forgot password
    ├── reset-password.html       # Reset password
    ├── images/
    │   └── brogan-card.jpg       # Photo of Brogan's card
    └── card/
        └── index.html            # Public card page (QR scan destination)
```

---

## Database Schema

### accounts
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| email | TEXT | Unique |
| hashed_password | TEXT | bcrypt |
| shipping_address | TEXT | For card delivery |
| email_verified | BOOLEAN | Default false |
| verification_token | TEXT | Cleared after verification |
| reset_token | TEXT | Password reset |
| reset_token_expires | TIMESTAMP | 1 hour expiry |
| created_at | TIMESTAMP | |

### cardholders
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| account_id | UUID | FK to accounts |
| name | TEXT | Appears on card |
| slug | TEXT | Unique URL slug |
| photo_url | TEXT | Not in use by design |
| card_message | TEXT | Card message text |
| color_scheme | TEXT | amber/ocean/forest/rose/slate |
| created_at | TIMESTAMP | |

### messages
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| cardholder_id | UUID | FK to cardholders |
| sender_name | TEXT | Optional |
| sender_email | TEXT | Optional |
| message_body | TEXT | Required |
| sent_at | TIMESTAMP | |

### card_orders
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| cardholder_id | UUID | FK to cardholders |
| quantity | INTEGER | Default 250 |
| status | TEXT | pending/approved/shipped |
| created_at | TIMESTAMP | |

---

## API Endpoints

### Public
| Method | Route | Description |
|---|---|---|
| GET | / | Homepage |
| GET | /card/{slug} | Public card page |
| GET | /card/{slug}/data | Card data (JSON) |
| GET | /card/{slug}/qr.png | QR code image |
| POST | /card/{slug}/message | Send message to family |
| GET | /slug-check/{slug} | Check slug availability |
| POST | /register | Create account |
| POST | /login | Login, returns JWT |
| GET | /verify | Verify email address |
| POST | /forgot-password | Request password reset |
| POST | /reset-password | Reset password with token |

### Authenticated
| Method | Route | Description |
|---|---|---|
| GET | /dashboard | Dashboard page |
| GET | /dashboard/data | Dashboard data (JSON) |
| POST | /cardholder | Create cardholder profile |
| PUT | /cardholder | Update cardholder profile |
| GET | /setup | Setup page |
| GET | /welcome | Welcome page |

### Pages
| Method | Route | Description |
|---|---|---|
| GET | /login | Login page |
| GET | /forgot-password | Forgot password page |
| GET | /reset-password | Reset password page |
| GET | /verified | Email verified page |

---

## Email Functions (app/email.py)

| Function | Trigger | Recipient |
|---|---|---|
| send_verification_email | Registration | New user |
| send_message_notification | Someone sends a message | Family |
| send_admin_card_notification | Cardholder setup complete | brodie@speakingwells.org |
| send_admin_signup_notification | New account created | brodie@speakingwells.org |
| send_welcome_email | (available, not currently called) | New user |
| send_password_reset_email | Forgot password request | User |

---

## Color Schemes

| Name | Primary Color |
|---|---|
| amber | #e8a838 |
| ocean | #2980b9 |
| forest | #27ae60 |
| rose | #e8386a |
| slate | #6c5ce7 |

---

## Local Development

```bash
# Activate environment
conda activate speakingwells

# Start server
cd ~/speakingwells
uvicorn app.main:app --reload

# Push to GitHub (triggers Render auto-deploy)
git add .
git commit -m "your message"
git push
```

**When testing locally**, change API URL in HTML files:
```javascript
//const API = 'https://speakingwells.org';
const API = 'http://127.0.0.1:8000';
```

**Before pushing**, change back to:
```javascript
const API = 'https://speakingwells.org';
//const API = 'http://127.0.0.1:8000';
```

Files that need this change: index.html, setup.html, welcome.html, login.html, dashboard.html, forgot-password.html, reset-password.html, card/index.html

---

## DNS Records (Namecheap)

| Type | Host | Value |
|---|---|---|
| ALIAS | @ | speakingwells.onrender.com |
| CNAME | www | speakingwells.onrender.com |
| MX | @ | mail.protonmail.ch (priority 10) |
| MX | @ | mailsec.protonmail.ch (priority 20) |
| TXT | @ | protonmail-verification=... |
| TXT | send | v=spf1 include:amazonses.com include:_spf.protonmail.ch ~all |
| TXT | resend._domainkey | p=MIGfMA... (DKIM for Resend) |
| TXT | _dmarc | v=DMARC1; p=none; |
| CNAME | protonmail._domainkey | protonmail.domainkey... (DKIM for Proton x3) |

---

## To-Do List

### Must Have Before Public Launch
- [ ] Our Story page (Brogan Wells, how it started, the mission)
- [ ] Brogan's photo on homepage
- [ ] Admin panel (view all signups, card orders, manage statuses)
- [ ] Rate limiting on message form (spam protection)
- [ ] Cloudflare setup (security, performance)
- [ ] Terms of Service page
- [ ] Privacy Policy page

### Nice to Have Soon
- [ ] Dashboard — ability to edit card message
- [ ] Dashboard — ability to change slug (before cards are printed)
- [ ] Login page — show error when email not verified with resend link
- [ ] Welcome email after card proof approved
- [ ] Card proof email workflow (you send proof, family approves)

### Future
- [ ] 501(c)(3) filing
- [ ] Stripe for donations
- [ ] Vistaprint/print service API integration
- [ ] Multiple cardholders per account (siblings, classrooms)
- [ ] Admin bulk export (CSV of orders)
- [ ] Mobile app

### Known Issues
- [ ] Setup page color scheme doesn't pre-load existing scheme correctly
- [ ] No resend verification email option on login if unverified

---

## Brogan's Card

- **URL:** speakingwells.org/card/brogan
- **Account:** brodiewells@protonmail.com
- **Color scheme:** amber
- **Original Joomla page:** tidewatertalk.com/bcontact (set up .htaccess redirect)

---

## The Story

SpeakingWells was inspired by Brogan Wells, a non-verbal young man who hands out cards wherever he goes that say:

*"Hi! I'm Brogan. I want you to know I noticed you and I care about you. Have a great day!"*

The cards include a QR code that lets strangers send messages back to his family.

One day, a woman named Elany wrote to say that Brogan had met her daughter Gabrielle — who has a traumatic brain injury — at a pet supply store. Brogan's card made Gabrielle smile in a way her mother rarely sees.

That email started a movement.

Brogan hands out cards everywhere he goes. The cards give him motivation to get out of the house and engage with the world. He has received messages back within minutes of handing them out.

SpeakingWells exists to give every non-verbal person in the world that same superpower.

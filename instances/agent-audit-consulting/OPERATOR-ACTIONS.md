# Operator actions — out-of-session

The builder writes the files. These steps require your accounts/keys and must be done by you. Per `factory/SPEC.md` § Working protocol step 3: in-session vs out-of-session boundary — the builder does not substitute one for the other.

## 1. Stripe Checkout link

- Log into Stripe dashboard
- Products → New product → "AI-Agent Audit", $2,500 USD, one-time
- Payment link → enable → copy the URL
- In `landing/index.html`, replace `{{STRIPE_CHECKOUT_URL}}` with the actual URL

## 2. Email address for intake

- Pick the email buyers reply to
- In `intake.md`, replace `{{OPERATOR_EMAIL}}` with the actual address
- Configure Stripe receipt-email reply-to so buyers see the right address

## 3. Deploy the landing page

Pick one (in order of simplicity):

### Option A: Cloudflare Pages (recommended)
- Create a Cloudflare account if needed
- Connect this repo
- Build settings: framework = none, build command = (empty), output dir = `instances/agent-audit-consulting/landing`
- Deploy → get a URL like `something.pages.dev`
- Optional: add a custom domain

### Option B: GitHub Pages
- Repo settings → Pages → Source = branch `master`, folder `/instances/agent-audit-consulting/landing`
- Wait ~1 min, get a URL like `holbizmetrics.github.io/verifiable-autonomy/...`

### Option C: local-only verify (smallest possible test)
- `cd instances/agent-audit-consulting/landing && python3 -m http.server 8000`
- Open `http://localhost:8000` in browser
- Note: Stripe checkout still requires the real URL substituted in step 1

## 4. Test-customer loop verify (done-condition)

- Open the deployed landing page
- Click the Buy button → Stripe Checkout opens
- Use Stripe test mode (test card 4242 4242 4242 4242), OR do a real $2,500 charge to your own card and refund
- Receipt arrives in your inbox
- Reply with the intake fields per `intake.md`
- Confirm the reply arrives

When all 4 steps above succeed end-to-end with you-as-test-customer → **Level-0 done.** Update `README.md` Status table.

## 5. Real-customer acquisition (out-of-session, post-deploy)

- Berlin Early AI-dopters 2026-06-17 talk = your lead-gen event
- Post-talk: hand out the landing URL
- First paying customer outside this list = the first real signal

The builder does NOT do step 5.

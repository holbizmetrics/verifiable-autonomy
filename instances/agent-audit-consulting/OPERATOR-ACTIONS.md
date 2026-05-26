# Operator actions — out-of-session

The builder writes templates + a render script. These steps require your accounts/keys and must be done by you. Per `factory/SPEC.md` § Working protocol step 3.

Templates use `{{OPERATOR_EMAIL}}` and `{{STRIPE_CHECKOUT_URL}}` placeholders. The render script (`render.py`) substitutes from env vars (preferred) or `.local/config.env` (gitignored). **Real values never enter git.**

## 1. Configure operator values (local)

- Copy `config.env.example` → `.local/config.env`
- Fill `OPERATOR_EMAIL` (address buyers reply to)
- Leave `STRIPE_CHECKOUT_URL` blank for now (set in step 2)
- Render: `python3 render.py` → output in `.local/dist/`
- Missing keys leave placeholders untouched (warning printed) — you can render + deploy with email only and add Stripe later

## 2. Stripe Checkout link (deferred per current operator decision)

- Log into Stripe dashboard
- Products → New product → `AI-Agent Audit`, $2,500 USD, one-time
- Payment link → enable → copy the URL
- Set `STRIPE_CHECKOUT_URL` in `.local/config.env` AND in the GitHub Actions secret (see step 3)
- Re-render: `python3 render.py`
- Configure Stripe receipt-email reply-to → your `OPERATOR_EMAIL`

## 3. Deploy the landing page

Pick one.

### Option A: GitHub Pages (workflow ready)

The `.github/workflows/pages.yml` workflow renders + deploys on push to master.

One-time operator setup:

- **Repo Settings → Pages → Source = "GitHub Actions"** (one toggle)
- **Repo Settings → Secrets and variables → Actions → New repository secret:**
  - `OPERATOR_EMAIL` = your real address
  - `STRIPE_CHECKOUT_URL` = your Stripe payment link (add when you have it)
- Push any change under `instances/agent-audit-consulting/` → workflow renders + deploys
- URL: `https://holbizmetrics.github.io/verifiable-autonomy/`

### Option B: Cloudflare Pages

- Create Cloudflare account, connect repo via CF dashboard
- Build command: `python3 instances/agent-audit-consulting/render.py`
- Output dir: `instances/agent-audit-consulting/.local/dist/landing`
- Add `OPERATOR_EMAIL`, `STRIPE_CHECKOUT_URL` as environment variables in CF dashboard

### Option C: local-only verify

- Set config in `.local/config.env`
- `python3 render.py`
- `cd .local/dist/landing && python3 -m http.server 8000`
- Open `http://localhost:8000`

## 4. Test-customer loop verify (done-condition)

Requires step 2 done.

- Open the deployed landing page
- Click the Buy button → Stripe Checkout opens
- Use Stripe test mode (test card `4242 4242 4242 4242`), OR do a real $2,500 charge to your own card + refund
- Receipt arrives in your inbox
- Reply with the intake fields per `.local/dist/intake.md`
- Confirm the reply arrives

When all of above succeed end-to-end → **Level-0 done.** Update `README.md` Status table.

## 5. Real-customer acquisition (out-of-session, post-deploy)

- Berlin Early AI-dopters 2026-06-17 talk = your lead-gen event
- Post-talk: hand out the landing URL
- First paying customer outside this list = the first real signal

The builder does NOT do step 5.

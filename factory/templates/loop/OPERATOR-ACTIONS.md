# Operator actions — deploy this storefront

Factory-built. The factory already baked the business content (headline, pitch,
price, promise, intake fields) into these files. The steps below need your
accounts/keys, so they are yours to run. Per `factory/SPEC.md` § Working
protocol step 3 (in-session builds; out-of-session = operator).

Remaining placeholder: `{{OPERATOR_EMAIL}}` (and `{{STRIPE_CHECKOUT_URL}}` if you
wire Stripe). `render.py` substitutes these from env vars or `.local/config.env`
(gitignored). **Real values never enter git.**

## 1. Configure operator values (local)

- Copy `config.env.example` -> `.local/config.env`
- Fill `OPERATOR_EMAIL` (address buyers reply to)
- Leave `STRIPE_CHECKOUT_URL` blank for now (email-intake path needs no Stripe)
- Render: `python3 render.py` -> output in `.local/dist/`
- Missing keys leave placeholders untouched (warning printed) — you can render +
  deploy with email only and add Stripe later

## 2. Deploy the landing page

Pick one.

### Option A: GitHub Pages (move to own repo)

- Move this business directory into its own git repo
- Copy `deploy-pages.yml.tmpl` -> `.github/workflows/pages.yml` in that repo
- Repo Settings -> Pages -> Source = "GitHub Actions"
- Repo Settings -> Secrets and variables -> Actions -> add `OPERATOR_EMAIL`
  (and `STRIPE_CHECKOUT_URL` when you have it)
- Push any change under `storefront/` -> workflow renders + deploys

### Option B: Cloudflare Pages

- Connect the business repo via the CF dashboard
- Build command: `python3 storefront/render.py`
- Output dir: `storefront/.local/dist/landing`
- Add `OPERATOR_EMAIL`, `STRIPE_CHECKOUT_URL` as CF environment variables

### Option C: local-only verify

- Set config in `.local/config.env`
- `python3 render.py`
- `cd .local/dist/landing && python3 -m http.server 8000`
- Open `http://localhost:8000`

## 3. Test-customer loop verify (done-condition)

- Open the deployed (or locally served) landing page
- Click the CTA -> your mail client opens a draft to `OPERATOR_EMAIL`
- Send the request from a second email address (test customer)
- From the operator address: receive it -> reply with the intake template
  (`.local/dist/intake.md`) + a manual invoice (bank transfer / invoice link)
- From the test-customer address: receive the intake email -> confirm round-trip

When all of the above succeed end-to-end -> **loop verified.**

## 4. Real-customer acquisition (out-of-session, post-deploy)

The builder does NOT do this step. First paying customer outside any warm list
is the first real signal. The market verifies business-success; the factory only
verifies the loop deploys and round-trips.

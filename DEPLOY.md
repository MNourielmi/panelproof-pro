# Deploy the public demonstration

`public_site/index.html` is the sales page and `public_site/app.html` is the browser application.

Option A: create a new public GitHub repository and upload the contents of `public_site` to the repository root. In Settings > Pages, deploy from the main branch root. Confirm the URL loads and the demo works.

Option B: drag the `public_site` folder into a static-host upload interface (for example, Netlify Drop). Confirm the final URL before sharing.

IMPORTANT: The demo is an early-access prototype. Browser localStorage is not a secure multi-user database. Do not use it to store confidential client information without a security review. Export JSON backups; browser data can be cleared. No payment processing, seller contact, license or privacy policy is configured. Do not advertise a checkout until those exist.

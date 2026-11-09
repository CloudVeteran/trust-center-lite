# Trust Center Lite

Trust Center Lite is a mini security trust center like the ones companies publish for customers. It shows a security posture page and a security questionnaire, with each answer mapped to NIST 800-53 controls.

![Home page](screenshots/home.png)
![Security posture page](screenshots/posture.png)
![Security questionnaire page](screenshots/questionnaire.png)

## How it's built
- Written in Flask and served by gunicorn on the minimal `cgr.dev/chainguard/python` image, running as a non-root user
- Read-only pages: no login, no uploads, no database
- Pinned dependencies and strict security headers (CSP, nosniff, X-Frame-Options, Referrer-Policy, HSTS)
- A GitHub Actions pipeline builds the image, generates an SPDX SBOM, and signs the image keyless with Sigstore cosign

## Control map
| Topic | NIST 800-53 |
|---|---|
| MFA for admin access | IA-2, IA-2(1) |
| Account management | AC-2 |
| Least privilege | AC-6 |
| Software inventory (SBOM) | CM-8, SR-4 |
| Image integrity (signing) | SI-7, SR-4 |
| Secure baseline | CM-2, CM-6, CM-7 |
| Change control | CM-3 |
| Logging | AU-2, AU-12 |

## Security decisions
- **Read-only by design.** With no forms, logins or database, there's very little for an attacker to work with.
- **Minimal base image.** No shell or package manager at runtime, and it starts near zero known CVEs.
- **Pinned dependencies.** Every build installs exactly the versions that were tested.
- **Signed images with an SBOM.** Anyone can verify where the image came from and what's inside it.

## Verify the signature
```
cosign verify ghcr.io/cloudveteran/trust-center-lite:latest \
  --certificate-identity-regexp "https://github.com/CloudVeteran/trust-center-lite/.*" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

## Status
On the Chainguard Harness beta waitlist (Nov 2026). Scan pending.
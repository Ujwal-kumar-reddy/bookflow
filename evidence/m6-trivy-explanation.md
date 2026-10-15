# DevSecOps: Trivy Security Scan Explanation (Module 6)

### 1. Scan Scope and Pipeline Configuration
In the BookFlow CI/CD pipeline (`.github/workflows/ci-cd.yml`), Aqua Security's **Trivy** container scanner scans both the backend (`python:3.12-slim`) and frontend (`nginxinc/nginx-unprivileged:1.27-alpine`) container images immediately after building and before publishing to GitHub Container Registry (GHCR). The scanner evaluates operating system packages (Debian/Alpine base layers) as well as installed language libraries (Python packages and NPM dependencies).

### 2. Quality Gate and Vulnerability Thresholds
The scan enforces a strict security quality gate using `severity: HIGH,CRITICAL` with `exit-code: '1'`. This guarantees that if any exploitable high or critical Common Vulnerabilities and Exposures (CVEs) are detected in either container image, the GitHub Actions pipeline immediately terminates with a non-zero exit code, blocking the promotion and deployment of vulnerable images.

### 3. Justification for `ignore-unfixed: true`
The pipeline specifies `ignore-unfixed: true` as a deliberate, defensible engineering decision. This filter focuses build gating strictly on actionable CVEs that have vendor-released security patches available for remediation. Unactionable vulnerabilities with no upstream fix available (such as documentation flaws or low-impact disclosures awaiting upstream maintainer patches) will not cause false-positive pipeline halts, while all fixable security flaws must be patched (via base image bump or package upgrades) before CI passes.

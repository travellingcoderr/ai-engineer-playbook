# Cert-Manager + Let's Encrypt SOP

This document shows how to secure `research_agent` on AKS with a real public TLS certificate for:

- `research.purpletechllc.com`

This replaces the manual TLS secret workflow with an automated certificate lifecycle using:
- `cert-manager`
- Let's Encrypt

## Why Use This Approach

Benefits:
- no manual `tls.crt` / `tls.key` handling
- automatic certificate issuance
- automatic renewal
- easier long-term maintenance

Why it is needed:
- ingress can terminate HTTPS only if it has a valid certificate
- browsers show `Not Secure` when the certificate is self-signed, mismatched, or missing
- Let's Encrypt provides a browser-trusted public certificate

## Current Environment Assumptions

- AKS cluster exists
- AKS app routing add-on is enabled
- ingress class is `webapprouting.kubernetes.azure.com`
- hostname will be `research.purpletechllc.com`
- DNS `A` record points to your ingress public IP

## Before You Start

Make sure this resolves publicly:

```bash
dig research.purpletechllc.com
```

It should resolve to your ingress IP, for example:

```text
20.75.248.23
```

If DNS is not correct, certificate issuance will fail.

## Step 1: Install cert-manager

Add the Helm repo:

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

Install cert-manager:

```bash
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```

Verify:

```bash
kubectl get pods -n cert-manager
```

You should see cert-manager pods running.

Official docs:
- <https://cert-manager.io/docs/installation/helm/>

## Step 2: Create a ClusterIssuer for Let's Encrypt

Create a file named `clusterissuer-letsencrypt.yaml`:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: you@purpletechllc.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
      - http01:
          ingress:
            ingressClassName: webapprouting.kubernetes.azure.com
```

Apply it:

```bash
kubectl apply -f clusterissuer-letsencrypt.yaml
```

Verify:

```bash
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-prod
```

## Step 3: Update Your Ingress To Use cert-manager

Your ingress needs:
- the real host `research.purpletechllc.com`
- a TLS secret name
- a cert-manager annotation

The important annotation is:

```yaml
cert-manager.io/cluster-issuer: letsencrypt-prod
```

## Step 4: Update Helm Values / Chart

The ingress should be configured like this conceptually:

```yaml
ingress:
  enabled: true
  className: webapprouting.kubernetes.azure.com
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  host: research.purpletechllc.com
  tls:
    enabled: true
    secretName: research-agent-tls
```

Then redeploy the Helm release.

## Step 5: Watch Certificate Issuance

Check these resources:

```bash
kubectl get certificate -n research-agent-dev
kubectl get certificaterequest -n research-agent-dev
kubectl get order -n research-agent-dev
kubectl get challenge -n research-agent-dev
```

Describe the certificate:

```bash
kubectl describe certificate research-agent-tls -n research-agent-dev
```

Check ingress:

```bash
kubectl get ingress -n research-agent-dev
kubectl describe ingress research-agent -n research-agent-dev
```

## Step 6: Validate TLS

Once issued:

```bash
openssl s_client \
  -connect research.purpletechllc.com:443 \
  -servername research.purpletechllc.com </dev/null 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

You want the SAN to include:

```text
DNS:research.purpletechllc.com
```

Also test:

```bash
curl -I https://research.purpletechllc.com/health
curl -I https://research.purpletechllc.com/docs
```

## Common Failure Reasons

### DNS not pointing to ingress IP

If `research.purpletechllc.com` does not resolve to the ingress IP, the HTTP-01 challenge will fail.

### Wrong ingress host

If ingress still points to `research-agent.example.com`, cert-manager will issue for the wrong hostname or fail.

### cert-manager annotation missing

Without `cert-manager.io/cluster-issuer`, cert-manager will not know to issue the certificate.

### Ingress class mismatch

If the solver or ingress uses the wrong ingress class, the ACME challenge route may never be served.

## Operational Notes

- Let’s Encrypt certificates renew automatically when cert-manager is configured correctly.
- The Kubernetes TLS secret is still used by ingress, but cert-manager manages it for you.
- You should not manually overwrite the TLS secret after cert-manager takes over.

## Recommended Steady State

- DNS `A` record: `research.purpletechllc.com -> ingress IP`
- ingress host: `research.purpletechllc.com`
- cert-manager installed in cluster
- `ClusterIssuer`: `letsencrypt-prod`
- ingress annotation points to `letsencrypt-prod`
- ingress TLS secret name remains stable: `research-agent-tls`

## References

- AKS custom domain + SSL: <https://learn.microsoft.com/en-us/azure/aks/app-routing-dns-ssl>
- AKS application routing: <https://learn.microsoft.com/en-us/azure/aks/app-routing>
- cert-manager Helm install: <https://cert-manager.io/docs/installation/helm/>

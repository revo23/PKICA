# PKI Lab

Hands-on Public Key Infrastructure lab using OpenSSL.

## What's Included

```
├── ca/                     # Certificate Authority
│   ├── certs/ca.cert.pem   # Root CA certificate
│   ├── private/ca.key.pem  # Root CA private key
│   ├── crl/ca.crl.pem      # Certificate Revocation List
│   ├── openssl.cnf         # CA configuration
│   └── index.txt           # Certificate database
├── server/                 # Server certificates
│   ├── server.key.pem      # Server private key
│   ├── server.csr.pem      # Certificate Signing Request
│   └── server.cert.pem     # Signed server certificate
└── https_server.py         # Test HTTPS server
```

## Quick Start

### Run the HTTPS Server

```bash
python3 https_server.py
```

### Test with curl

```bash
curl --cacert ca/certs/ca.cert.pem https://localhost:8443
```

## Commands Reference

### Create a Root CA

```bash
# Generate private key
openssl genrsa -out ca/private/ca.key.pem 4096

# Create self-signed certificate
openssl req -config ca/openssl.cnf \
  -key ca/private/ca.key.pem \
  -new -x509 -days 7300 -sha256 -extensions v3_ca \
  -out ca/certs/ca.cert.pem
```

### Issue a Server Certificate

```bash
# Generate server key
openssl genrsa -out server/server.key.pem 2048

# Create CSR
openssl req -config ca/openssl.cnf \
  -key server/server.key.pem \
  -new -sha256 -out server/server.csr.pem

# Sign with CA
openssl ca -config ca/openssl.cnf \
  -extensions server_cert -days 365 -notext -md sha256 \
  -in server/server.csr.pem \
  -out server/server.cert.pem
```

### Verify a Certificate

```bash
openssl verify -CAfile ca/certs/ca.cert.pem server/server.cert.pem
```

### Revoke a Certificate

```bash
# Revoke
openssl ca -config ca/openssl.cnf -revoke server/server.cert.pem

# Generate CRL
openssl ca -config ca/openssl.cnf -gencrl -out ca/crl/ca.crl.pem
```

### View Certificate Details

```bash
# View certificate
openssl x509 -noout -text -in server/server.cert.pem

# View CRL
openssl crl -noout -text -in ca/crl/ca.crl.pem

# View CA database
cat ca/index.txt
```

## Certificate Status

The `ca/index.txt` file tracks certificate status:
- `V` = Valid
- `R` = Revoked
- `E` = Expired

## Notes

- Root CA validity: 20 years
- Server certificate validity: 1 year
- The server certificate has been revoked (for demonstration)
- Private keys in this repo are for learning only - never commit real keys

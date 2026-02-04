# PKI Process Diagram

## Certificate Issuance Flow

```mermaid
flowchart TD
    subgraph CA["Certificate Authority"]
        CA_KEY[/"CA Private Key<br/>(ca.key.pem)"/]
        CA_CERT[("CA Certificate<br/>(ca.cert.pem)")]
        DB[(index.txt<br/>Database)]
    end

    subgraph Server["Server"]
        S_KEY[/"Server Private Key<br/>(server.key.pem)"/]
        CSR["Certificate Signing<br/>Request (CSR)"]
        S_CERT[("Server Certificate<br/>(server.cert.pem)")]
    end

    S_KEY -->|"openssl req -new"| CSR
    CSR -->|"Submit to CA"| CA
    CA_KEY -->|"Signs"| CSR
    CA_CERT -->|"Issues"| S_CERT
    CSR -->|"Record"| DB
```

## Certificate Verification

```mermaid
flowchart LR
    Client([Client]) -->|"Connect"| Server([Server])
    Server -->|"Present Certificate"| Client
    Client -->|"Verify against"| CA_CERT[("CA Certificate")]
    CA_CERT -->|"Trust Chain Valid"| OK{{"Secure Connection"}}
```

## Certificate Revocation

```mermaid
flowchart TD
    REVOKE["Revoke Certificate<br/>openssl ca -revoke"] -->|"Update"| DB[(index.txt<br/>Status: R)]
    DB -->|"Generate"| CRL[("CRL<br/>ca.crl.pem")]

    subgraph Verification
        Client([Client]) -->|"Check"| CRL
        CRL -->|"Serial in CRL?"| Decision{Revoked?}
        Decision -->|"Yes"| REJECT[Reject Connection]
        Decision -->|"No"| ACCEPT[Accept Connection]
    end
```

## Complete PKI Lifecycle

```mermaid
sequenceDiagram
    participant S as Server
    participant CA as Certificate Authority
    participant C as Client

    Note over CA: Setup Phase
    CA->>CA: Generate CA Key Pair
    CA->>CA: Create Self-Signed CA Cert

    Note over S,CA: Issuance Phase
    S->>S: Generate Server Key Pair
    S->>S: Create CSR
    S->>CA: Submit CSR
    CA->>CA: Verify CSR
    CA->>S: Issue Signed Certificate

    Note over S,C: Usage Phase
    C->>S: TLS Handshake
    S->>C: Present Certificate
    C->>C: Verify Cert Chain
    C->>S: Encrypted Communication

    Note over CA: Revocation Phase
    CA->>CA: Revoke Certificate
    CA->>CA: Generate CRL
    C->>CA: Check CRL
    CA->>C: Certificate Revoked
    C->>S: Reject Connection
```

## ASCII Diagram (for terminals)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PKI CERTIFICATE LIFECYCLE                     │
└─────────────────────────────────────────────────────────────────┘

1. CA SETUP
   ┌──────────────────┐
   │  Root CA         │
   │  ┌────────────┐  │
   │  │ Private Key│──┼──► Self-signed Certificate
   │  └────────────┘  │
   └──────────────────┘

2. CERTIFICATE ISSUANCE
   ┌──────────┐         ┌──────────┐         ┌──────────┐
   │  Server  │──CSR───►│    CA    │──Cert──►│  Server  │
   │  Key     │         │  Signs   │         │  Cert    │
   └──────────┘         └──────────┘         └──────────┘

3. TLS CONNECTION
   ┌──────────┐                              ┌──────────┐
   │  Client  │◄─────── Certificate ────────│  Server  │
   │          │                              │          │
   │ Verify   │                              │          │
   │ against  │                              │          │
   │ CA Cert  │◄──────── Encrypted ────────►│          │
   └──────────┘                              └──────────┘

4. REVOCATION
   ┌──────────┐         ┌──────────┐         ┌──────────┐
   │    CA    │──Rev───►│   CRL    │◄──Check─│  Client  │
   │          │         │          │         │          │
   └──────────┘         └──────────┘         └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │ REJECTED │
                        └──────────┘
```

.. _release_notes:

Release Notes
=============

Release v2.4
--------------


 * Confidential VM support for AMD SEV & SEV-SNP in AWS, Azure, and Google Cloud
 * Integrity Measurement Architecture (IMA) integrations and enhancements (improved intrusion prevention and detection)
 * SELinux policy enhancements (improved intrusion detection and prevention)
 * System report now includes IMA policy, IMA violations, and SELinux enforcement status
 * Audit Log now available over REST API and Web UI
 * Improved storage encryption for private keys, open CSRs, and certificates
 * TPM 2.0 support for disk encryption keys
 * Expanded test and validations on more VM sizes in AWS, Azure, and Google Cloud


 Bug Fixes:

 * REST API & Web UI bug fixes, updates to support new features
 * Improved REST API certs/v2/tls/client-cert endpoints and certs/v2/tls/reload (separate reload which restarts the TLS web server may close the current connection)



Release v2.3
--------------


 * Initial User Creation API updates to require Instance ID
 * Instance ID is known only to the VM instance owner making the initial user creation process more secure.

 Bug Fixes:

 * Web UI bug fixes, updates to support Instance ID for initial user creation



Release v2.2
--------------

AWS Support:

 * AWS is now a supported platform
 * Update kernel and drivers for AWS infrastructure
 * Terraform Modules released to support AWS SecureKey VPN deployment
 
 Bug Fixes:

 * Web UI updates, enhancements, and bug fixes



Release v2.1
--------------

Post Quantum Support

 * Post-Quantum Safe ML-KEM (RFC 9370 and RFC 9242) support for IKEv2 Connections.
    * ML KEM for a Hybrid Post Quantum Safe KEM (IKEv2 will always use the DH group in addition to an optional ML KEM)
    * CNSA v2.0 allows MLKEM-1024 (Kyber1024) only - this is enforced by default and so only mlkem1024 is supported in SK-VPN
    * RFC allows selection of up to 7 additional KEMs
    * Configurable using REST API and Web UI
 * Post Quantum Preshared Key (PPK, RFC 8784) support for IKEv2 Connections. Configurable using REST API and Web UI.
 * Improve DH Group, PRF and other IKEv2 parameters selection on the Web UI. 

 Bug Fixes:

 * Fix ESN configuration for IKEv2 connections - added ESN selectionto Web UI.
 * Numerous Web UI updates and enhancements.


Release v2.0
--------------

SecureKey Crypto Library v2.0 updates:
 * Improved AES throughput over SecureKey v1 (3X+ increase for small packets)
 * Added support for AES-256-CTR and AES-256-CBC modes
 * SecureKey OpenSSL Provider updates:
 * SecureKey provider protects Certificates, Private Keys and Secret data in memory for Authentication and Key Exchange
 * SecureKey provider protects AES keys in memory during encryption and decryption
 * FIPS Certification is in progress


* SecureKey OpenSSL Provider used for Management Plane (SSH, HTTPS, and IKEv2)
* Enforce strong algorithms/curves for SSH and HTTPS (AES-256, and CNSA v1.0 algorithms where available)
* Multi-layer encryption for stored Private Keys using LUKS and Database encryption
* Update SecureKey Logo and Web UI color scheme
* Stateful Firewall improvements - added ACL session management


Bug Fixes:

* Update COTS packages to latest versions
* Bug fixes for the REST API and Web UI


Release v1.3
--------------
Google Cloud support.

Bug Fixes and improvements:

* Support for Google Cloud (required drivers have been added)
* Update data plane package versions
* Bug fixes and new features for the Web UI


Release v1.2
--------------
Web User Interface improvements.

Bug Fixes and improvements:

* Historical statistics endpoints return a 10 minute history
* Fixes and new features for the Web UI
* Interface, Firewall, IPsec, and drop counters for charts now use historical data
* Changes to IPsec connection to allow editing existing connections
* Update certificate details for all certificate types
* Add Interface chart and Runtime staistics 
* Allow download of CSR PEM file data
* Add support for Extended Sequence Numbers (ESNs)
* Various API updates and bug fixes in support of the Web User Interface
* Open Source package updates and bug fixes



Release v1.1
--------------
Web User Interface has been added to allow management and configuration of the SK-VPN using a web browser.

Bug Fixes and improvements.

* Fix MAC/LAN address Role assignment - was failing if the initial LAN/WAN ip address was 10.X.0.X where X >= 10
* REST API now allows LAN/WAN MAC assignemnt even if initial IPs are not valid or unassigned
* ACL IP Rules now use an Integer for Protocol instead of string

 
New Features and REST API updates:

* Expand Version reporting in sys/version 
* Expand system report in sys/system-report to report "build-type"
* Web User Interface 
* Various API updates and bug fixes in support of the Web User Interface



Release v1.0
--------------
v1.0.1717174796

Initial Release of the SecureKey VPN.
SecureKey Crypto library v1.0 is used to secure keys used by the data plane.


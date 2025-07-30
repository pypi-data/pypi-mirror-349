.. _ipsec_setup:

IPsec Setup
===========

.. _ipsec_certificates:

Setup IPsec Certificates
------------------------

The SK-VPN supports certificate based IKEv2 Security Associations.

The SK-VPN Web UI Certificates page is used to install and manage IPsec certificates:

.. image:: images/UI/Certificates.png
    :align: center

|

To setup IKEv2 Certificates using the REST API:

(*Pre*) Generate a CA Root Certificate and Private Key pair which will be used to sign the device Certificate.
see :ref:`ca_generation`

* Export a Certificate Signing Request: POST ``/cert/signing-request`` see :ref:`cert_csr`
* Sign the CSR with the CA Root Private Key see :ref:`cert_signing`.
* Upload the signed certificate to the SK-VPN via the POST ``/cert/signed_csr`` endpoint with the `usage` field set to `IPSEC`
* Verify the Certificate detials using the GET ``/cert/certs`` and ``/cert/details``

.. _ipsec_connections:

IPsec Connections
-----------------
An IPsec Connection is a set of parameters to define an IKE (phase 1) connection and a set of (phase 2) Child Security Associations.
The SK-VPN supports IKEv2 Certificate-based authentication only (no Pre-Shared Key PSK support due to the lack of key security).

The SK-VPN requires a user to upload then activate the connection, activation loads the connection into the dataplane. 
Details of the active (loaded) connections along with the details of the child SAs are available via the REST API and the Web UI.

Active Connections and Connection Details and Statistics are available on the Web UI IPsec -> Active Sessions page:

.. image:: images/UI/IPsec_Active_Sessions.png
    :align: center

|

Connections can be created, modified, deleted and activated using the Web UI IPsec -> Saved Connections page:

.. image:: images/UI/IPsec_Activate_Conn_Menu.png
    :align: center
    :scale: 50%

|


IPsec Connections are managed using the REST API:

* Upload a new connection: POST ``/ipsec/connections``
* Activate a connection: POST ``/ipsec/connections/loaded/<name>``
* Deactivate a connection: DELETE ``/ipsec/connections/loaded/<name>``
* Get the list of saved connections: GET ``/ipsec/connections/saved``
* Get the list of active connections: GET ``/ipsec/connections/loaded``
* Delete a connection: DELETE ``/ipsec/connections``

.. _security_associations:

IPsec Security Associations
---------------------------
IPsec Connections define a set of Security Associations (SAs) that 
will be installed on the SK-VPN. IPsec ESP Tunnel Mode is used by default.

Each Security Association defines a secure tunnel between the SK-VPN and a remote peer.

Active SAs are managed using the Web UI IPsec -> Active Sessions page and selecting the 
Actions Menu item for the Active SA to activate or terminate:

.. image:: images/UI/IPsec_Activate_SA_Menu.png
    :align: center
    :scale: 50%

|


Security Associations are managed using the REST API. 

* Get the list of active SAs: GET ``/ipsec/sas``
* Force Initiation of an SA: POST ``/ipsec/sas/initiate-child``
* Force Termination of an SA: POST ``/ipsec/sas/terminate-child``
* Get list of a Connection's SAs: GET ``/ipsec/connections`` use the `children` field for the list of SAs

.. _post_quantum_safe_mlkem:

Post Quantum Safe IPsec 
-----------------------
SecureKey VPN supports both Postquantum Preshared Keys (PPK, RFC 8784) 
and Post Quantum Safe ML KEM (RFC 9370 and RFC 9242) for IKEv2 connections.

----------------------
Post Quantum Safe PPKs
----------------------
An IKEv2 PPK is configurable using the Web UI and REST API. 
First a shared secret (PPK) must be imported to the SK-VPN. 
This shared-secret is identified using a unqiue ID string supplied by the user. 
The data is supplied as a Hexadecimal String up to 32 bytes long (64 characters).

Once uploaded, a PPK can be used in an IKEv2 connection by selecting from the list of loaded PPKs.
When the connection is activated, the SK-VPN will set the IKEv2 PPK and the SA status will indicate that PPK is in use.
Note the peer must also support PPK and have the identical PPK ID and data set.

Using the REST API: POST ``/certs/shared_secret`` 
Using the Web UI: Certificates -> Shared Secrets

.. image:: images/UI/Shared_Secret_PPK.png
    :align: center 

|

-------------------------
Post Quantum Safe ML KEMs
-------------------------
IKEv2 ML KEM (RFC 9370 and RFC 9242) are supported. 

IKEv2 Connections can be configured with additional KEMs to support Post Quantum Safe Key Exchange.
Currently MLKEM-1024 (Kyber1024) is the only CNSA v2.0 KEM.

To configure connections to use additional Post Quantum Key Exchange Methods,
select "mlkem1024" from the list of available KEMs in the Web UI. Default is None.
Note PPK can be used with additional Key Exchange Methods.

.. image:: images/UI/Post_Quantum_IPsec_Options.png
    :align: center 
    :scale: 50%

|

Next Steps
-----------
System Monitoring see :ref:`system_monitoring`
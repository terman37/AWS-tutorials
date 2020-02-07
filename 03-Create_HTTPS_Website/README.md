# AWS Deploy new webservice with encryption (Windows based)

## Architecture

- **VPC**
  - IGW
  - Public subnet
  - Route table subnet -> IGW
- **EC2 Instance** (Windows base 2019 - Free tier)
  - T3.large - 80Gb 
  - Security group (Firewalling)
    - RDP (TCP:3389) from 0.0.0.0/0 - (not SSH - windows machine)
    - HTTP (TCP:80) from 0.0.0.0/0
    - HTTPS (TCP:443) from 0.0.0.0/0
  - Attach Elastic IP
- **Route 53:**
  - not accessible with AWS training account
  - DNS (UDP:53)



## Connect via RDP

- Instance / Connect

<img src="connect_to_rdp.png" style="zoom:50%;" />

- Get the password using private key.

- Connect through RDP on windows
- Accept self signed Certificate



## Application layer: Windows Server

- Server manager

  - Add roles and features
  - In server roles: Select Web Server (IIS)
  - Install

  ![](severmanager_install_IIS.png)

  

- Administrative tools / IIS / Default website

  - Default web site: right click / bindings:

    *A web service must be bound to private IP Address and port*

    - Site binding / Add site binding  for 80 / 443 to private IP

    *Public IP Binding done at AWS console level*

  - Can change location of files in right click / bindings

    <img src="IIS_admin_tools.png" style="zoom:50%;" />

## Try connection (http)

- in web browser: http://<public IP> (no certificate yet for https)

## Encryption certificate

### Create CSR (certificate customer request)

#### Generate CSR via MS console: "mmc"

- File / "add/remove snap ins"

  - certificates snap in

    - computer account (IIS looks for certificates here)

    - <img src="mmc_certificate_snapin.png" style="zoom:50%;" />

      

- in personal (folder)

  - right click all tasks / create customer request

    <img src="console_create_CSR.png" style="zoom:50%;" />

  - next next next

    <img src="csr1.png" style="zoom:50%;" />

  - certificate information / properties / subject (mandatory fields)

    - common name

    - country

    - organization

    - organization unit

    - email

    - locality

    - state

      <img src="csr2.png" style="zoom:50%;" />

  - private key

    - select cryptographic service provider (CSP) you want to use:

      - ECDH_secP384r1... (for example)

    - Key options

      - Make private key exportable

    - select Hash algorithm

      - sha256

        <img src="csr3.png" style="zoom:50%;" />

  - OK

  - Save CSR file in <folder>/<file csr>



#### Buy certificate

​	Gandi.net

	- login
	- ... buy, paste your CSR

 - select validation method
   - via DNS: add DNS CNAME entry in route 53
     - (can check if CNAME entry is propagated: MXtoolbox.com /  CNAME lookup)

Once generated - download CRT file

#### Import Certificate

​	MMC CONSOLE / personal certificates / import

<img src="crt_import.png" alt="crt_import" style="zoom:50%;" />

#### Add binding

in IIS / bindings

<img src="https_binding_crt.png" alt="https_binding_crt" style="zoom:50%;" />


# Hesiod VCF9
Uses [Project Hesiod](https://github.com/boconnor2017/hesiod), a Photon based approach to initiate and launch an immutable VCF 9 bringup ready environment. The purpose of this project is to facilitate hands on experience with the VCF 9 installation process using a nested environment. There are two goals with this project:

| Goal | Description |
|------|-------------|
| Immutability | Every element of the lab including shared services will be Photon based "appliances" that can be destroyed and rebuilt. No backup or recovery will be used. |
| Process | All automation in this lab will be in support of accelerated VCF 9 prerequisites so that the architect can spend 90% or more of their time with VCF rather than the setup of VCF. |
| Automation | Once deployed, the environment is designed to support automation development against a small scale VCF 9 ecosystem. This environment is not scaled for performance or capacity. |

# Prerequisites
The following physical equipment is **required** to run hesiod-vcf9:

| Requirement | Description |
|-------------|-------------|
| Physical Network | ability to provision multiple /24 VLANs: Management, VLAN, VSAN, NSX |
| Physical ESXi | at least 1x physical server. See [Lab Sizing Guide](#lab-sizing-guide) below. |
| DNS Server | recommended: use [hesiod-dns](https://github.com/boconnor2017/hesiod-dns) to spin up an immutable DNS server and configure necessary DNS entries for VCF |

The following binaries are **required** to run hesiod-vcf9:

| Requirement | Description |
|-------------|-------------|
| PhotonOS OVA | version 5.0 recommended (download from [VMware GitHub](https://vmware.github.io/photon/)) |
| ESXi 9 (iso) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Installer (ova) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 NSX Manager (ova) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 NSX Content Pack for Cloud Foundation Operations (vlcp) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 vCenter (iso) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Operations (ova) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Operations Lifecycle Manager (ova) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Automation (tar) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Download Tool (tar) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Offline Depot Metadata (zip) | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |


The following shared services are **required** to run hesiod-vcf9:

| Requirement | Description |
|-------------|-------------|
| DNS | recommended: use [hesiod-dns](https://github.com/boconnor2017/hesiod-dns) to deploy and configure a PhotonOS Docker container running Tanium. |

# Quick Start
Deploy Photon OS OVA to the physical server. Follow the steps in the [Hesiod Photon OS Quick Start](https://github.com/boconnor2017/hesiod/blob/main/photon/readme.md) readme file to prep the Photon server for VCF. 

Next, install OVFTool by following the steps in the [Hesiod Install OVFTool on Photon OS](https://github.com/boconnor2017/hesiod/tree/main/ovftool) process.

Next, install PowerCLI by following the steps in the [Hesiod Install PowerCLI directly to the OS](https://github.com/boconnor2017/hesiod/blob/main/powershell/readme.md) process.

Run the following scripts as root.
```
cd /usr/local/
```
```
git clone https://github.com/boconnor2017/hesiod-vcf9
```
```
cp -r hesiod/python/ hesiod-vcf9/hesiod
```
```
cd hesiod-vcf9/
```

Next, select from one of the following modules (note the dependencies):

| Module   | Description | Dependencies | 
|--------|-------------|--------------|
| Module 1 | Build lab environment JSON File | Do this only if you want a CLI prompt to create your first `lab_environment.json` file. You can edit `json/lab_environment.json` directly if you want. Once completed, save the json file to a repository so you can skip this step in the future. | None. This step is optional. |
| Module 2 | Build lab environment documentation | When your `lab_environment.json` file is populated, do this to convert the parameters from the JSON into a Markdown file. This is helpful to document configuration details and to validate configuration inconsistencies before deploying the platform. | Module 1. This step is optional. |
| Module 3 | Deploy an Offline Depot to Store Binaries | Do this to create an Offline Depot to store VCF binary files. Binaries will need to be downloaded manually using appropriate entitlements. This step is optional if you prefer to use an Online Depot. | None. |
| Module 4 | Build a VCF 9 Ready Nested Management Cluster | Deploys and configures 4x nested ESXi 9 hosts. These hosts will be the target for the VCF 9 installation process. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated. |
| Module 5 | Deploy VCF 9 Fleet | Uses the VCF 9 Installer API to deploy the VCF management workload domain (fleet), including VCF Operations and VCF Automation. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated. Module 4 Nested Management Cluster needs to be deployed. |
| Module 6 | Build a VCF 9 Ready Nested VI Cluster | Deploys and configures 4x nested ESXi 9 hosts. These hosts will be the target for VCF 9 workloads. This is useful capacity for automation, operations, and other services use cases such as VMaaS, CaaS, DBaaS, LBaaS, FWaaS, and K8aaS. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated.  |
| Module 7 | Build a VCF 9 VI Workload Domain | Uses the VCF 9 Operations Manager API to deploy a VCF VI workload domain, including Supervisor Cluster and VPC for modern VCF Automation workloads. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated. Module 6 Nested VI Cluster needs to be deployed. |
| Module 8 | Deploy "Hello World" VM as a Service | Uses the VCF 9 Automation API to deploy a "Hello World" VM as a Service using Photon as the Linux image. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated. Module 7 VI Workload Domain needs to be deployed. |
| Module 9 | Deploy "Hello World" Container as a Service | Uses the VCF 9 Automation API to deploy a "Hello World" Container as a Service using Docker on Photon as the container orchestration engine. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated. Module 8 VM as a Service needs to be deployed. |
| Module 10 | Deploy "Hello World" Database as a Service | Uses the VCF 9 Automation API to deploy a "Hello World" Database as a Service using open source PostgreSQL on Photon as the database platform. | Prerequisites above need to be completed. Module 1 `lab_environment.json` needs to be populated. Module 8 VM as a Service needs to be deployed. |



## Module 1: Build lab environment JSON File (Optional)

Run the following command from Photon:
```
python3 hesiod-vcf9.py -configjson
```

## Module 2: Build lab environment documentation (Optional)

Run the following command from Photon:
```
python3 hesiod-vcf9.py -json2md myconfigfile.json mydocfile.md
```

## Module 3: Deploy an Offline Depot to Store Binaries (Optional)

* Step 1: Deploy a new PhotonOS VM with **140GB** vDisk. 
* Step 2: Follow [Hesiod Photon OS Quick Start](https://github.com/boconnor2017/hesiod/blob/main/photon/readme.md) steps to prep the Photon server for VCF.
* Step 3: Repartition the disk:
    * Run fdisk: `fdisk /dev/sda`
    * List Partitions: `p`
    * Delete Partition: `d`
    * Number 2: `2`
    * New Partition: `n`
    * Number 2: `2`
    * Start value next to sda2: `30720`
    * End value (use the default): `293599231`
    * Do not remove signature: `N`
    * List Partitions (you should see new size next to Linux Filesystem): `p`
    * Verify Partition data: `v`
    * Write table to disk: `w`
    * Rerun `fdisk /dev/sda`
    * Confirm that sda2 is now resized appropriately: `p`
    * Quit: `q`
    * Check the filesystem size (GBs): `df -BG`
    * Resize the filesystem: `resize2fs /dev/sda2`
    * Recheck the filesystem size (GBs): `df -BG`
* Step 4: Download Offline Depot Metadata
```
cd /usr/local/drop/
```
Download the `vcf-9.x.x.x-offline-depot-metadata.zip` file and the `vcf-download-tool-9.x.x.x.x.tar.gz` files from the Boradcom Portal.
```
root@photon-machine [ /usr/local/drop ]# ls -l
total 1164
-rw-r----- 1 root root 1191522 Aug 14 14:11 vcf-9.0.0.0-offline-depot-metadata.zip
```
* Step 5: Create a new file called `downloadtoken.txt` and paste your VCF 9 entitled Download Token into the text file.
```
root@photon-machine [ /usr/local/drop ]# ls -l
total 375864
-rw-r----- 1 root root        33 Aug 20 13:26 downloadtoken.txt
-rw-r----- 1 root root   1191522 Aug 20 13:23 vcf-9.0.0.0-offline-depot-metadata.zip
-rw-r----- 1 root root 383684630 Aug 20 13:23 vcf-download-tool-9.0.0.0100.24880038.tar.gz

```
* Step 6: Configure TCP Keepalive
```
vi /etc/ssh/sshd_config
```
```
TCPKeepAlive yes
```
* Step 7: create a folder for the download tool and move the download tool to the new folder
```
mkdir /usr/local/drop/vcf-download-tool
```
```
mv vcf-download-tool-9.0.0.0100.24880038.tar.gz /usr/local/drop/vcf-download-tool
```
```
cd /usr/local/drop/vcf-download-tool
```
* Step 8: Extract the Download Tool
```
tar -xvf vcf-download-tool-9.0.0.0100.24880038.tar.gz
```
* Step 9: Download the VCF 9 Binaries from the Broadcom Portal
```
cd /usr/local/drop
```
```
vcf-download-tool/bin/./vcf-download-tool binaries download --depot-store=/usr/local/drop/PROD --depot-download-token-file=downloadtoken.txt --vcf-version=9.0.0
```
* Step 10: Build Web Service
```
cd /usr/local/
```
```
git clone https://github.com/boconnor2017/hesiod-vcf9
```
```
cp -r hesiod/python/ hesiod-vcf9/hesiod
```
```
cd /usr/local/hesiod-vcf9/
```
```
python3 hesiod-vcf9.py -depot
```   

Access your Offline Depot at https://<ip_address>   

## Module 4: Build a VCF 9 Ready Nested Management Cluster

* Step 1: Edit the `lab_environment.json` file (recommended: store this file in `usr/local/drop` for future use)
* Step 2: Run the following command from Hesiod:
```
python3 hesiod-vcf9.py -eoe-mgt
```

## Module 5: Deploy VCF 9 Fleet
Coming soon...

## Module 6: Build a VCF 9 Ready Nested VI Cluster
* Step 1: Edit the `lab_environment.json` file (recommended: store this file in `usr/local/drop` for future use)
* Step 2: Run the following command from Hesiod:
```
python3 hesiod-vcf9.py -eoe-vi
```

## Module 7: Build a VCF 9 VI Workload Domain
Coming soon...

## Module 8: Deploy "Hello World" VM as a Service
Coming soon...

## Module 9: Deploy "Hello World" Container as a Service
Coming soon...

## Module 10: Deploy "Hello World" Database as a Service 
Coming soon...
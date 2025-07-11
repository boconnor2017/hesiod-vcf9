# Hesiod VCF9
Uses [Project Hesiod](https://github.com/boconnor2017/hesiod), a Photon based approach to initiate and launch a VCF 9 bringup ready environment. The purpose of this project is to facilitate hands on experience with the VCF 9 installation process using a nested environment. There are two goals with this project:

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

The following binaries are **required** to run hesiod-vcf5:

| Requirement | Description |
|-------------|-------------|
| PhotonOS OVA | version 5.0 recommended (download from [VMware GitHub](https://vmware.github.io/photon/)) |
| ESXi iso | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |
| VCF 9 Installer | version 9.0.0 is required (download from [Broadcom Portal](https://support.broadcom.com/web/ecx)) |

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

Next, select from one of the following paths:

| Path   | Description | Dependencies | 
|--------|-------------|--------------|
| Path 1 | Build a New VCF 9 Configuration JSON File | Do this first - no dependencies. Save the populated json file to a repository for future use. |
| Path 2 | Document VCF 9 Configuration JSON File as Markdown | When your configuration file is populated, use this path to convert the parameters from the JSON into a Markdown file. This is helpful to document configuration details and to validate configuration inconsistencies before deploying the platform. |
| Path 3 | Deploy an Offline Depot to Store Binaries| Use this path to create an Offline Depot to store VCF binary files. Binaries will need to be downloaded manually using appropriate entitlements. |
| Path 4 | Build a VCF 9 Ready Nested Management Cluster | Deploys and configures 4x nested ESXi 9 hosts. These hosts will be the target for the VCF 9 installation process. |
| Path 5 | Build a VCF 9 Ready Nested VI Cluster | Deploys and configures 4x nested ESXi 9 hosts. These hosts will be the target for VCF 9 workloads. This is useful capacity for automation, operations, and other services use cases such as VMaaS, CaaS, DBaaS, LBaaS, FWaaS, and K8aaS. |



## PATH 1: Build a New VCF 9 Configuration JSON File

Run the following command from Photon:
```
python3 hesiod-vcf9.py -configjson
```

## PATH 2: Document VCF 9 Configuration JSON File as Markdown

Run the following command from Photon:
```
python3 hesiod-vcf9.py -json2md myconfigfile.json mydocfile.md
```

## PATH 3: Deploy an Offline Depot to Store Binaries

* Step 1: Deploy a new PhotonOS VM with 100GB vDisk. ssh to the new VM and execute the remaining steps.
* Step 2: Repartition the disk:
    * Run fdisk: `fdisk /dev/sda/`
    * List Partitions: `p`
    * Delete Partition: `d`
    * Number 2: `2`
    * New Partition: `n`
    * Number 2: `n`
    * Start value next to sda2: `30720`
    * End value (use the default): `104857566`
    * Do not remove signature: `N`
    * List Partitions (you should see new size next to Linux Filesystem): `p`
    * Verify Partition data: `v`
    * Write table to disk: `w`
    * Run fdisk: `/dev/sda`
    * Confirm that sda2 is now resized appropriately
    * Quit: `q`
* Step 3: Follow [Hesiod Photon OS Quick Start](https://github.com/boconnor2017/hesiod/blob/main/photon/readme.md) steps to prep the Photon server for VCF
* Step 4: Clone this repo
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
* Step 5: Create the Offline Depot Web Service and File structure
```
python3 hesiod-vcf9.py -depot
```
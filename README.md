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
| Path 1 | [Build a New VCF 9 Configuration JSON File](#path-1-build-a-new-vcf-9-configuration-json-file) | Do this first - no dependencies. |
| Path 2 | [Build VCF 9 Ready ESXi Hosts for Management Cluster](#path-2-build-vcf-9-ready-esxi-hosts-for-management-cluster) | VCF 9 Configuration File must be completed (Path 1) |
| Path 3 | [Build VCF 9 Ready ESXi Hosts for VI clusters](#path-3-build-vcf-9-ready-esxi-hosts-for-vi-clusters) | VCF 9 must be installed (Path 2) |


## PATH 1: Build a New VCF 9 Configuration JSON File

```
python3 hesiod-vcf9.py -configjson
```

## PATH 2: Build VCF 9 Ready ESXi Hosts for Management Cluster 

```
python3 hesiod-vcf9.py -bringup
```

## PATH 3: Build VCF 9 Ready ESXi Hosts for VI Clusters 

```
python3 hesiod-vcf9.py -bringup
```

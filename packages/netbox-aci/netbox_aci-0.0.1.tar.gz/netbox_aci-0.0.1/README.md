# Netbox ACI Plugin
A [Netbox](https://github.com/netbox-community/netbox) plugin for [Cisco ACI](https://www.cisco.com/site/de/de/products/networking/cloud-networking/application-centric-infrastructure/index.html) related objects in Netbox.

## Features

This plugin provides the following models to be able to document an Cisco ACI setup:

- Attachable Access Entity Profiles
- Application Profiles
- Bridge Domains
- Contracts (Standard)
- Endpoint Groups
- Endpoint Security Groups
- Interface Policy Groups
- L3 Outs
- Link Level Policies

## Contributing

This project is currently maintained jointly by:

- [Marc-Aurel Mohr-Lenné](https://github.com/bechtle-bms)

## Compatibility

Below listed plugin Versions has been tested with its corresponding NetBox Version.

|Netbox       |Plugin     |
|-------------|-----------|
| 4.1.3       | >= 0.0.1  |
| 4.2.0       | >= 0.0.1  |

## Installation

### Option 1
Setup docker-compose override file as shown below.

    services:
      netbox:
        volumes:
          - ./netbox-aci/netbox_aci:/opt/netbox/netbox/netbox_aci

### Option 2
Manually copy the plugin into the NetBox directory:

    cp -r netbox-aci/netbox_aci /opt/netbox/netbox/netbox_aci

Add the `netbox-aci` tables to your database, run the `migrate` command.

    cd /opt/netbox/netbox/
    python3 manage.py migrate netbox_aci

## Configuration

Enable the plugin in `<netbox/docker path>/configuration/plugins.py`.

```
PLUGINS = [
    "netbox_aci"
]
```

## Requirements

* Custom Field:

        - name: "gateway"
          label: "Gateway"
          object_types:
            - "ipam.ipaddress"
          required: false
          type: "boolean"
          default: false

* Fixtures:

        You can load the requirements manually:
        python manage.py loaddata defaults.json

        !!! NOTE AND ADJUST THE VALUES FOR pk AND related_object_type BEFOREHAND !!!

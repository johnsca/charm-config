# charm-config

This adds a `charm config` subcommand which can read config info for a charm
in the store and present it in a friendly way.

## Installation

You must first have the `charm` snap installed:

```
snap install --classic charm
```

Then install the plugin:

```
snap install --classic charm-config
```

## Usage

Call with a charm store URL and an optional pattern for selecting options.

```
$ charm config cs:~containers/calico
Option                       Value                           Type     Description
---------------------------------------------------------------------------------
calico-node-image            'rocks.canonical.com:443/c'...  string   The image id to use for calico/node.
calico-policy-image          'rocks.canonical.com:443/c'...  string   The image id to use for calico/kube-controllers.
cidr                         '192.168.0.0/16'                string   Network CIDR assigned to Calico. This is applie...
global-as-number             64512                           int      Global AS number.
global-bgp-peers             '[]'                            string   List of global BGP peers. Each BGP peer is spec...
ipip                         'Never'                         string   IPIP mode. Must be one of "Always", "CrossSubne...
manage-pools                 True                            boolean  If true, a default pool is created using the ci...
nat-outgoing                 True                            boolean  NAT outgoing traffic
node-to-node-mesh            True                            boolean  When enabled, each Calico node will peer with e...
route-reflector-cluster-ids  '{}'                            string   Mapping of unit IDs to route reflector cluster ...
subnet-as-numbers            '{}'                            string   Mapping of subnets to AS numbers, specified as ...
subnet-bgp-peers             '{}'                            string   Mapping of subnets to lists of BGP peers. Each ...
unit-as-numbers              '{}'                            string   Mapping of unit IDs to AS numbers, specified as...
unit-bgp-peers               '{}'                            string   Mapping of unit IDs to lists of BGP peers. Each...

$ charm config cs:~containers/calico ipip
Option  Value    Type     Description
-------------------------------------
ipip  'Never'  string   IPIP mode. Must be one of "Always", "CrossSubnet", or "Never".
```

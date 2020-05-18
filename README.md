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
charm config cs:ubuntu
charm config cs:ubuntu hostname
```

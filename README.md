## quickwifiap
Maybe you know the situation: For security purposes, you routinely change the
WiFi credentials in your household. You've just finished the migration and all
clients now work with the new network. All devices? Nooooooo, because you
forgot that *one* device that still knows the old credentials and that you now
cannot reach anymore.

So do you change all the config back? No, you use quickwifiap: It creates a
WiFi access point for you (using hostapd), starts a DNS/DHCP server using
dnsmasq and optionally even sets up the routes so that your new WiFi network is
NATted into the Internet. With that network you can now quickly reconfigure the
device and everything is fine.

## Dependencies
hostapd, dnsmasq.

## Usage
```
usage: quickwifiap [-h] [-v] config_file

Quick Wifi AP configuration.

positional arguments:
  config_file    JSON file that specifies the network configuration to use

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Increases verbosity. Can be specified multiple times to
                 increase.
```

The configuration JSON file is fairly self-explanatory:

```json
{
    "interface":            "wlan0",
    "essid":                "Free Wifi",
    "network":              "172.16.42.0/24",
    "nat_ext_interface":    "eth0",
    "security": {
        "mode":     "wpa2-psk",
        "psk":      "foobar123"
    }
}
```

Above configuration would start a "Free Wifi" on wlan0, using network
172.16.42.0/24 and WPA2-PSK with the passphrase "foobar123", routing traffic to
the Internet through eth0.

# License
GNU GPL-3.

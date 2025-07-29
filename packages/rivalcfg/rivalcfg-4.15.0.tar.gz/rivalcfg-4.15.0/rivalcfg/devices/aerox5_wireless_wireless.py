from . import aerox5_wireless_wired


_WIRELESS_FLAG = 0b01000000
_READBACK_LENGTH = 64


def _patch_command(info):
    # Copy the info dict
    result = dict(info)
    # Copy the command list
    result["command"] = list(result["command"])
    # Patch the command
    result["command"][0] = result["command"][0] | _WIRELESS_FLAG
    # Add readback
    result["readback_length"] = _READBACK_LENGTH
    return result


profile = {
    "name": "SteelSeries Aerox 5 Wireless",
    "models": [
        {
            "name": "SteelSeries Aerox 5 Wireless (2.4 GHz wireless mode)",
            "vendor_id": 0x1038,
            "product_id": 0x1852,
            "endpoint": 3,
        },
        {
            "name": "SteelSeries Aerox 5 Wireless Destiny 2 Edition (2.4 GHz wireless mode)",
            "vendor_id": 0x1038,
            "product_id": 0x185C,
            "endpoint": 3,
        },
        {
            "name": "SteelSeries Aerox 5 Wireless Diablo IV Edition (2.4 GHz wireless mode)",
            "vendor_id": 0x1038,
            "product_id": 0x1860,
            "endpoint": 3,
        },
    ],
    "settings": {
        name: _patch_command(info)
        for name, info in aerox5_wireless_wired.profile["settings"].items()
    },
    "battery_level": _patch_command(aerox5_wireless_wired.profile["battery_level"]),
    "save_command": _patch_command(aerox5_wireless_wired.profile["save_command"]),
}

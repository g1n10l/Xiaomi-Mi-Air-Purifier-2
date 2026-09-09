# Xiaomi Mi Air Purifier 2 for Home Assistant

Local Home Assistant integration for Xiaomi Mi Air Purifier 2. It communicates directly with the purifier over the LAN by using its miIO token. No Xiaomi cloud connection is used after setup.

## Product

[![Xiaomi Mi Air Purifier 2](https://www.jib.co.th/img_master/uploads/Content/9301214081/xiaomi-mi-air-purifier-2-001.jpg)](https://www.mi.com/in/air2/)

The image links to the [official Xiaomi Mi Air Purifier 2 product page](https://www.mi.com/in/air2/). The product photo is hosted by [JIB](https://www.jib.co.th/web/product/readProduct/27144/MI--%E0%B9%80%E0%B8%84%E0%B8%A3%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%9F%E0%B8%AD%E0%B8%81%E0%B8%AD%E0%B8%B2%E0%B8%81%E0%B8%B2%E0%B8%A8--AIR-PURIFIER-2).

## Supported models

- `zhimi.airpurifier.m1`
- `zhimi.airpurifier.m2`
- `zhimi.airpurifier.ma1`
- `zhimi.airpurifier.ma2`

## Features

- Power control
- Auto, Silent, and Favorite modes
- Favorite fan level control
- PM2.5, temperature, and humidity sensors
- Filter life and filter operating time
- Motor speed, total operating time, and purified air volume when reported by the device
- Buzzer, child lock, and LED switches
- LED brightness selection
- Filter replacement warning
- English and Polish translations
- Diagnostics with the miIO token removed

The integration only creates optional entities when the purifier reports the matching property.

## Installation

### HACS

1. Open HACS.
2. Add this repository as a custom integration repository.
3. Install **Xiaomi Mi Air Purifier 2**.
4. Restart Home Assistant.

### Manual installation

Copy `custom_components/xiaomi_mi_air_purifier_2` to the `custom_components` directory in your Home Assistant configuration, then restart Home Assistant.

## Configuration

1. Give the purifier a fixed IP address in your router.
2. Obtain its 32-character miIO token.
3. In Home Assistant, open **Settings > Devices & services**.
4. Select **Add integration** and search for **Xiaomi Mi Air Purifier 2**.
5. Enter the purifier's IP address and token.

Home Assistant must be able to reach the purifier on the local network, usually over UDP port 54321. Do not reset or re-pair the purifier after obtaining the token because that may change it.

## Notes

Fan percentage maps to the 16 Favorite mode levels. Setting a percentage switches the purifier to Favorite mode. Auto and Silent remain available as presets.

This project is community maintained and is not affiliated with Xiaomi.

## License

[MIT](LICENSE)

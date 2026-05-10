# Z906 IR Remote HA

Beta-quality Home Assistant custom integration for controlling a Logitech Z906
speaker system through the Home Assistant `infrared` entity platform.

[![Open your Home Assistant instance and open this repository in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mastertape&repository=z906-ir-remote-ha&category=integration)

This integration is a consumer-side proof of the Home Assistant infrared
architecture introduced in Home Assistant 2026.4:

1. Logitech Z906 device/protocol knowledge lives in Home Assistant.
2. Commands are encoded with `infrared-protocols`.
3. Commands are sent with `infrared.async_send_command`.
4. Hardware is selected by `infrared.*` entity ID.
5. ESPHome IR/RF proxy devices act only as transport emitters.

It does not add Logitech-specific buttons to ESPHome YAML and does not call
ESPHome services directly.

## Requirements

- Home Assistant 2026.5.0 or newer.
- HACS installed, unless installing manually.
- An `infrared.*` transmitter entity.
- Tested target setup: ESPHome IR/RF proxy transmitter exposed as
  `infrared.xiao_smart_ir_mate_ir_proxy_transmitter`.

## Installation with HACS

Click the button above to open this repository in HACS:

1. Select `Open link`.
2. Confirm adding the custom repository if Home Assistant asks.
3. In HACS, download `Z906 IR Remote HA`.
4. Restart Home Assistant.

If the button does not work, add the repository manually:

1. Open HACS.
2. Open the three-dot menu in the top right.
3. Select `Custom repositories`.
4. Add this repository URL:

   ```text
   https://github.com/mastertape/z906-ir-remote-ha
   ```

5. Select category `Integration`.
6. Download the integration.
7. Restart Home Assistant.

## Configuration

Enable the integration from YAML. For Home Assistant packages:

```yaml
z906_ir_remote_ha:
  emitter_entity_id: infrared.xiao_smart_ir_mate_ir_proxy_transmitter
```

This creates a media player entity named:

```text
media_player.logitech_z906
```

The default `emitter_entity_id` is already
`infrared.xiao_smart_ir_mate_ir_proxy_transmitter`, so this is also valid:

```yaml
z906_ir_remote_ha:
```

Optional beta configuration:

```yaml
z906_ir_remote_ha:
  name: Logitech Z906
  emitter_entity_id: infrared.xiao_smart_ir_mate_ir_proxy_transmitter
  sources:
    input_1: INPUT 1
    input_2: INPUT 2
    input_3: OPTICAL 1
    input_4: OPTICAL 2
    input_5: COAX 1
    aux: AUX 1
```

The default source names are intentionally assistant-friendly:

- `INPUT 1` = 6-channel direct
- `INPUT 2` = stereo RCA
- `OPTICAL 1` = optical input 3
- `OPTICAL 2` = optical input 4
- `COAX 1` = digital coaxial input 5
- `AUX 1` = front-panel aux input

## Media Player

The integration exposes a real `media_player` entity with:

- `device_class: receiver`
- source list
- source selection
- volume up
- volume down

It deliberately does not expose:

- turn on / turn off
- mute
- absolute volume percentage
- sound mode

The Z906 is IR-only and has no feedback channel. The known power and mute
commands are toggles, not verified discrete on/off commands. Volume is relative
only. Effect and level selection are cyclical/contextual. The media player
therefore only advertises features it can honestly perform.

Current source is stored optimistically after `select_source`, because the Z906
has discrete direct input IR commands but no feedback channel.

## Media Player Actions

Select source:

```yaml
action: media_player.select_source
target:
  entity_id: media_player.logitech_z906
data:
  source: OPTICAL 1
```

Volume up:

```yaml
action: media_player.volume_up
target:
  entity_id: media_player.logitech_z906
```

Volume down:

```yaml
action: media_player.volume_down
target:
  entity_id: media_player.logitech_z906
```

## Low-Level Services

The original proof-of-concept services remain available.

Generic NEC / extended NEC:

```yaml
action: z906_ir_remote_ha.send_nec
data:
  entity_id: infrared.xiao_smart_ir_mate_ir_proxy_transmitter
  address: "0xA002"
  command: "0xAA"
  modulation: 38650
  repeat_count: 0
```

Known Logitech Z906 command:

```yaml
action: z906_ir_remote_ha.send_z906
data:
  command: volume_up
```

If `entity_id` is omitted, the default transmitter is:

```text
infrared.xiao_smart_ir_mate_ir_proxy_transmitter
```

The Logitech Z906 codes are represented in the byte order expected by
`infrared-protocols`. For example, the commonly published raw value
`0x400555AA` maps to `NECCommand(address=0xA002, command=0xAA)`.

## HomeKit

HomeKit requires media players with `device_class: receiver` to be exposed as a
separate accessory. Use a separate HomeKit instance that includes only this one
media player:

```yaml
homekit:
  - name: Z906 Receiver
    port: 21064
    mode: accessory
    filter:
      include_entities:
        - media_player.logitech_z906
```

Then pair this HomeKit accessory separately in Apple Home.

## Alexa and Google Assistant

The default source names use Home Assistant/Alexa-compatible input names such as
`INPUT 1`, `OPTICAL 1`, `COAX 1`, and `AUX 1`. Alexa's Smart Home input
controller only accepts a restricted set of input names, so changing source
labels may make some inputs unavailable to Alexa.

Google Assistant supports Home Assistant media player source selection and
relative volume control, but media players may not always appear as elegantly in
the Google Home app as native Google Cast or TV devices.

No separate Alexa or Google code is needed. The integration exposes one honest
Home Assistant receiver entity and lets Home Assistant's cloud/assistant
integrations consume it.

## Manual Installation

Copy this directory:

```text
custom_components/z906_ir_remote_ha
```

to your Home Assistant configuration directory:

```text
/config/custom_components/z906_ir_remote_ha
```

Then add this to YAML and restart Home Assistant:

```yaml
z906_ir_remote_ha:
```

## Scope and Future TODOs

This is intentionally still small. It does not provide a config flow, UI, broad
IR database, ESPHome buttons, or direct ESPHome service calls.

Possible future improvements:

- verify whether discrete power on/off IR codes exist
- verify whether discrete mute on/off IR codes exist
- verify whether true absolute volume is possible
- decide whether source-name customization should stay YAML-only or move to a
  config flow
- add a config flow once the beta behavior has settled
- add tests against Home Assistant's custom-component test helpers

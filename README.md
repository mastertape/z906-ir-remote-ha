# Logitech Z906 IR Proxy for Home Assistant

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

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Requirements

- Home Assistant 2026.5.0 or newer.
- HACS installed, unless installing manually.
- Any compatible Home Assistant `infrared.*` transmitter entity.
- Tested reference setup: Seeed Studio XIAO IR Mate running ESPHome IR/RF
  proxy firmware, exposed in Home Assistant as
  `infrared.xiao_smart_ir_mate_ir_proxy_transmitter`.

## IR Hardware

This integration is transport-agnostic. It does not know or care whether the IR
emitter is a Seeed device, another ESPHome proxy, or a future Home Assistant
infrared emitter. The only hardware contract is a Home Assistant entity in the
`infrared` domain that can transmit commands.

The tested reference emitter is a Seeed Studio XIAO IR Mate flashed with the
official ESPHome IR/RF proxy firmware. ESPHome lists the XIAO IR Mate on its
official [Ready-Made Projects](https://esphome.io/projects/?type=irrf) page
under `Infrared & radio frequency proxy`. That page can be used to install the
ready-made ESPHome proxy firmware directly, and the resulting device can then be
adopted in the ESPHome dashboard. This firmware is important: the XIAO IR Mate
does not ship from the factory with this Home Assistant infrared proxy firmware
already installed.

The recommended firmware source for reproducing the tested setup is the
official
[ESPHome infrared-proxies repository](https://github.com/esphome/infrared-proxies),
which hosts YAML configurations for a curated set of known, tested devices that
can serve as infrared proxies for Home Assistant.

This is different from the older Seeed factory demo firmware with `Signal0` ...
`Signal9`, `Learn`, and `Send` style controls. That factory demo interface is
not enough for this integration. This integration requires the ESPHome IR/RF
proxy firmware, because Home Assistant must see a real `infrared.*` emitter
entity so commands can flow through Home Assistant's official infrared API.

## Installation with HACS

Click the button above to open this repository in HACS:

1. Select `Open link`.
2. Confirm adding the custom repository if Home Assistant asks.
3. In HACS, download `Logitech Z906 IR Proxy`.
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
  initial_power_state: on
  initial_mute_state: off
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
- optimistic turn on
- optimistic turn off
- optimistic mute / unmute
- source list
- source selection
- volume up
- volume down

It deliberately does not expose:

- absolute volume percentage
- sound mode

The Z906 is IR-only and has no feedback channel. The known power and mute
commands are toggles, not verified discrete on/off commands. This integration
therefore implements power and mute as deliberate optimistic assumed-state
features on the `media_player` entity itself.

The media player's own stored state is the integration's state memory:

- `turn_on` always sends `power_toggle` and then stores the state as on
- `turn_off` always sends `power_toggle` and then stores the state as off
- mute always sends `mute` and then stores muted as true
- unmute always sends `mute` and then stores muted as false

This is the intended operating model for this IR-only receiver. It gives
HomeKit, Siri, Alexa, Google Assistant, and Assist one proper receiver entity to
control. No separate helper switch, button, or script is required for power or
mute.

The user command is treated as the best available real-world state signal: the
human is effectively the sensor. If someone says "turn on", the integration
assumes they can see or hear that the receiver is currently off, so it sends IR
even if the old stored Home Assistant state already said on. This prevents voice
commands such as "Ton an" and "Ton aus" from being silently ignored after drift
or routine mains-power cuts.

This is not a generic toggle UI. The exposed interface remains `turn_on`,
`turn_off`, mute, and unmute because humans naturally command target states, not
raw toggles.

The assumed state can drift if the Z906 is controlled outside this integration,
for example with the original remote or front-panel controls. If that happens,
issue the desired explicit command once, such as "turn on", "turn off", "mute",
or "unmute". Home Assistant will store that requested state again.

Important trade-off: because the physical hardware only has toggle codes and no
feedback, issuing `turn_on` while the real Z906 is already on will physically
turn it off; issuing `turn_off` while it is already off will physically turn it
on. The chosen trade-off for this integration is to never silently ignore an
explicit user command and to let human observation correct the assumed state
through normal use.

On first boot only, before a previous Home Assistant state has been restored,
the optional defaults are used:

```yaml
z906_ir_remote_ha:
  initial_power_state: on
  initial_mute_state: off
```

Restored Home Assistant state always takes precedence over these initial
defaults.

Observed behavior on a real stock Z906, and independent technical
reverse-engineering by Simon Arlott, indicate that when mains power is removed
and later restored the stock unit comes back physically off / in standby. This
is not documented here as an official Logitech manufacturer guarantee; it is
documented as observed real-device behavior and supported by independent
technical analysis. In practice this means a mains outage can make Home
Assistant's assumed power state drift if Home Assistant had stored the receiver
as on before the outage.

The existing low-level service remains available as a laboratory/manual tool. It
sends only the physical IR toggle and does not change the stored media player
state:

```yaml
action: z906_ir_remote_ha.send_z906
data:
  command: power_toggle
```

For ordinary use after drift, prefer the media player command that matches what
you want physically, such as `media_player.turn_on` when the receiver is off.

Current source is stored optimistically after `select_source`, because the Z906
has discrete direct input IR commands but no feedback channel. After a hard
power loss, the optimistic source may drift if the most recent source change was
active at runtime but had not yet been retained by a normal clean power-off
cycle. The integration does not add artificial commit or resync behavior; it
only documents this observed hardware behavior.

Volume is relative only. Effect and level selection are cyclical/contextual. The
media player therefore still does not expose absolute volume or sound modes.

## Media Player Actions

Turn on:

```yaml
action: media_player.turn_on
target:
  entity_id: media_player.logitech_z906
```

Turn off:

```yaml
action: media_player.turn_off
target:
  entity_id: media_player.logitech_z906
```

Mute:

```yaml
action: media_player.volume_mute
target:
  entity_id: media_player.logitech_z906
data:
  is_volume_muted: true
```

Unmute:

```yaml
action: media_player.volume_mute
target:
  entity_id: media_player.logitech_z906
data:
  is_volume_muted: false
```

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

Power and mute are part of the receiver media player itself, so HomeKit, Siri,
Alexa, Google Assistant, and Assist should target `media_player.logitech_z906`
directly. Do not create separate helper switches for power or mute.

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
- expose a deliberate state reset/calibration workflow if that proves useful
- decide whether source-name customization should stay YAML-only or move to a
  config flow
- add a config flow once the beta behavior has settled
- add tests against Home Assistant's custom-component test helpers

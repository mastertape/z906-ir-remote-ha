![Logitech Z906 IR Remote for Home Assistant](https://raw.githubusercontent.com/mastertape/z906-ir-remote-ha/main/custom_components/z906_ir_remote_ha/brand/logo.png)

# Logitech Z906 IR Remote for Home Assistant

Home Assistant custom integration that adds a Logitech Z906 speaker system as a
`media_player` receiver entity and controls it through the Home Assistant
`infrared` entity platform.

[![Open your Home Assistant instance and open this repository in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mastertape&repository=z906-ir-remote-ha&category=integration)

This integration is a focused consumer-side implementation of the Home
Assistant infrared architecture introduced in Home Assistant 2026.4:

1. Logitech Z906 device/protocol knowledge lives in Home Assistant.
2. Commands are encoded with `infrared-protocols`.
3. Commands are sent with `infrared.async_send_command`.
4. Hardware is selected by `infrared.*` entity ID.
5. ESPHome IR/RF proxy devices act only as transport emitters.

It does not add Logitech-specific buttons to ESPHome YAML and does not call
ESPHome services directly.

The project is intentionally narrow: it is for people who still have a Z906
doing useful old-school receiver work, such as external 5.1 over optical,
coaxial, or direct inputs, and want that device to behave like a proper Home
Assistant receiver without replacing the hardware.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Requirements

- Home Assistant 2026.5.0 or newer.
- HACS installed, unless installing manually.
- Any compatible Home Assistant `infrared.*` transmitter entity.
- Tested reference setup: Seeed Studio XIAO IR Mate running ESPHome IR/RF
  proxy firmware, exposed in Home Assistant as
  `infrared.xiao_smart_ir_mate_ir_proxy_transmitter`.

## Important Home Assistant 2026.6.x Update Note

Home Assistant 2026.6.x changed enough around custom integration loading that
older releases of this integration may no longer be loaded from YAML reliably.
When that happens, Home Assistant never imports the integration, so the
`z906_ir_remote_ha` service domain is missing and automations that call
`z906_ir_remote_ha.send_z906` can be reported as unknown actions.

Version `1.1.0` fixes this by moving the receiver setup to Home Assistant
config entries while preserving YAML import for existing users. The low-level
services are still registered by the integration setup path, and existing
automations do not need to change.

Recommended update order for existing users:

1. Create a Home Assistant backup.
2. Update this integration to `v1.1.0` or newer through HACS.
3. Restart Home Assistant.
4. Confirm that `z906_ir_remote_ha.send_z906` appears under Developer Tools ->
   Actions.
5. Then update Home Assistant Core to 2026.6.x if you have not already done so.

If Home Assistant Core is already on 2026.6.x and the service domain is missing,
update this integration to `v1.1.0` or newer, restart Home Assistant, and then
check Developer Tools -> Actions again. Existing YAML such as
`z906_ir_remote_ha:` is imported automatically into a config entry.

## IR Hardware

This integration is transport-agnostic. It does not know or care whether the IR
emitter is a Seeed device, another ESPHome proxy, or a future Home Assistant
infrared emitter. The only hardware contract is a Home Assistant entity in the
`infrared` domain that can transmit commands.

The tested reference emitter is a Seeed Studio XIAO IR Mate flashed with the
official ESPHome IR/RF proxy firmware. ESPHome lists the XIAO IR Mate on its
official [Ready-Made Projects](https://esphome.io/projects/?type=irrf) page
under `Infrared & radio frequency proxy`. To reproduce the tested setup, open
that page, choose `Infrared & radio frequency proxy`, pick `XIAO IR Mate`, and
press `Connect` with the device attached to your computer. The page then flashes
the ready-made ESPHome proxy firmware directly in the browser. After flashing,
the resulting device can be adopted in the ESPHome dashboard. This firmware is
important: the XIAO IR Mate does not ship from the factory with this Home
Assistant infrared proxy firmware already installed.

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

## Installation via HACS

Click the button above to open this repository in HACS:

1. Select `Open link`.
2. Confirm adding the custom repository if Home Assistant asks.
3. In HACS, download `Logitech Z906 IR Remote`.
4. Restart Home Assistant.

This repository is installable today as a HACS custom repository. It is being
kept in a form suitable for a later HACS default-repository submission, but it
is not part of the HACS default repositories yet.

If the button does not work, add the repository manually as a custom repository:

1. Open HACS.
2. Go to `Integrations`.
3. Open the three-dot menu in the top right.
4. Select `Custom repositories`.
5. Add this repository URL:

   ```text
   https://github.com/mastertape/z906-ir-remote-ha
   ```

6. Select category `Integration`.
7. Download the integration.
8. Restart Home Assistant.
9. Add YAML configuration as documented below.

For existing installations on Home Assistant 2026.6.x, install or update to
`v1.1.0` or newer before troubleshooting automations. Versions before `1.1.0`
may leave the `z906_ir_remote_ha` action domain unavailable because Home
Assistant does not reach the old YAML-only setup path.

## HACS Publication Status

This repository is prepared for HACS custom-repository use and is structured as
a candidate for later HACS default-repository submission.

Current in-repository preparation:

- HACS metadata is present in `hacs.json`.
- The integration manifest includes the HACS-required metadata keys.
- HACS validation and Hassfest GitHub Actions are included.
- Local brand images are included in
  `custom_components/z906_ir_remote_ha/brand/`.
- Versioned GitHub releases should be used for installs and updates.

Note: Home Assistant 2026.3+ supports local brand images for custom
integrations. The icon may still appear as `icon not available` in some HACS
repository overview lists if that view uses the older
`brands.home-assistant.io` CDN path instead of Home Assistant's local brands
API. The integration itself ships local brand assets, and Home Assistant can use
them in contexts that read the local brand folder.

Remaining external maintainer steps before opening a HACS default-repository
submission:

- Add a GitHub repository description, for example:
  `Home Assistant custom integration for Logitech Z906 over the new infrared entity platform`.
- Add GitHub topics:
  `home-assistant`, `hacs`, `custom-component`, `infrared`, `ir`, `logitech`,
  `z906`, `esphome`, `media-player`.
- Make sure GitHub Issues are enabled.
- Make sure the HACS validation and Hassfest workflows pass without ignored
  checks.
- Create a full GitHub release after validation passes, not only a tag.
- Open a PR to `hacs/default` only after the checks above are complete.

The `home-assistant/brands` repository no longer accepts new custom integration
brand PRs. The local brand images in this repository use a neutral custom
IR/speaker symbol and do not use Logitech logos or other trademarked brand
assets.

## Configuration

The integration now supports Home Assistant config entries. Existing YAML
configuration is imported automatically on startup when Home Assistant loads the
integration.

For new installations, add the integration from the Home Assistant UI:

1. Go to **Settings** -> **Devices & services**.
2. Select **Add integration**.
3. Search for **Logitech Z906 IR Remote**.
4. Enter the infrared emitter entity and optional initial/source settings.

Existing YAML configuration remains supported as an import source. For Home
Assistant packages:

```yaml
z906_ir_remote_ha:
  emitter_entity_id: infrared.xiao_smart_ir_mate_ir_proxy_transmitter
```

This creates a media player entity and a stateless level button:

```text
media_player.logitech_z906
button.logitech_z906_level
```

The default `emitter_entity_id` is already
`infrared.xiao_smart_ir_mate_ir_proxy_transmitter`, so this is also valid:

```yaml
z906_ir_remote_ha:
```

After the first successful YAML import, the receiver is represented as a Home
Assistant config entry. Keep the YAML if you want Home Assistant to continue
syncing these values on restart, or remove it after confirming the imported
integration entry has the expected settings.

Optional configuration:

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

You can also use the `sources:` block to name inputs after the devices you
actually connected, for example `PC`, `TV`, `Apple TV`, or `PlayStation`. The
default names are chosen for broad assistant compatibility, especially Alexa,
so custom names may behave differently with voice assistants.

## Media Player

The integration exposes a real `media_player` entity with:

- `device_class: receiver`
- optimistic turn on
- optimistic turn off
- optimistic mute / unmute
- source list
- source selection
- next effect
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

Volume is relative only. The Z906 effect command is a stateless cyclic next
effect button. The media player exposes it as `media_player.media_next_track`,
because the behavior is closest to moving to the next item in a cycle. Every
call sends IR; no current effect is stored or assumed.

Level selection is cyclical/contextual and does not fit a standard media player
semantic well. The integration exposes it as a separate stateless button entity
instead of forcing it into `sound_mode`.

The media player therefore still does not expose absolute volume or sound
modes.

The Logitech Z906 is a mature, IR-only receiver system. This integration keeps
the Home Assistant model as close as practical to the available standard
`media_player` semantics without inventing feedback or state that the hardware
cannot provide. The cyclic Effect button is exposed as "next effect" because it
is the closest standard media-player action for a stateless next-in-cycle IR
command. The rarely used contextual Level button is exposed as a separate
stateless button because it does not have a good media-player equivalent.

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

Next effect:

```yaml
action: media_player.media_next_track
target:
  entity_id: media_player.logitech_z906
```

Level:

```yaml
action: button.press
target:
  entity_id: button.logitech_z906_level
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

Alternatively, restart Home Assistant and add **Logitech Z906 IR Remote** from
**Settings** -> **Devices & services**.

## Sources and Acknowledgements

This project is an independent Home Assistant custom integration. The
references below document the public APIs, libraries, protocol facts, command
data, and hardware behavior research that informed the implementation. Unless
explicitly stated otherwise, this repository does not include copied code or
configuration from the projects and discussions listed here.

### Home Assistant and ESPHome

This integration uses Home Assistant's infrared consumer/emitter architecture
and sends commands through `infrared.async_send_command(...)`. Command objects
are encoded with the `infrared-protocols` Python library, which is used as a
normal dependency.

The tested reference emitter during development was a Seeed Studio XIAO IR Mate
running the official ESPHome IR/RF proxy firmware. This project remains
transport-agnostic: it targets compatible Home Assistant `infrared.*` emitter
entities and is not tied to one specific IR blaster.

Thanks to the Home Assistant and ESPHome projects for the infrared architecture,
the proxy firmware work, and the documentation that makes consumer integrations
like this possible.

### Logitech Z906 Infrared Command Research

The Logitech Z906 command set used here was assembled and cross-checked from
public community research, especially `pladaria`'s Logitech Z906 IR-code gist,
which also points to earlier hifi-remote.com and RemoteCentral discussions.

Special thanks to the public contributors in that research thread, including:

- `pladaria` for collecting the Z906 protocol and command data.
- `rafales` for the carrier-frequency note.
- `valentinkauf` for notes about converted/reversed values for transmission.
- `hatl` for LIRC-style data and working ESPHome examples.
- `tomaszkoc` for Broadlink/Home Assistant conversion notes and related tooling
  references.

This project is not a copy of the older ESPHome button-based examples. It uses
publicly documented Z906 command knowledge in a Home Assistant consumer
integration that sends through the official infrared abstraction.

### Device Behavior Research

Simon Arlott's independent reverse-engineering article about modifying the
Logitech Z906 console/firmware helped document the stock standby-after-mains
behavior. That behavior also matched testing on the maintainer's real unit. It
is documented here as independent technical analysis and observed behavior, not
as an official Logitech manufacturer guarantee.

### Trademarks and Independence

Logitech and Z906 are trademarks of their respective owner. This project is
independent and is not affiliated with, sponsored by, or endorsed by Logitech.

### References

- [Home Assistant infrared entity developer documentation](https://developers.home-assistant.io/docs/core/entity/infrared/)
- [Home Assistant developer blog: New infrared entity platform for IR device integrations](https://developers.home-assistant.io/blog/2026/03/30/infrared-entity-platform/)
- [`home-assistant-libs/infrared-protocols`](https://github.com/home-assistant-libs/infrared-protocols)
- [ESPHome Ready-Made Projects: Infrared & radio frequency proxy](https://esphome.io/projects/?type=irrf)
- [`esphome/infrared-proxies`](https://github.com/esphome/infrared-proxies)
- [`pladaria` Logitech Z906 IR-code gist](https://gist.github.com/pladaria/f8a1ce754f1ed3022b78f8a302d463b5)
- [LIRC remote database](https://lirc.sourceforge.net/remotes/)
- [`molexx/irdb2broadlinkha`](https://github.com/molexx/irdb2broadlinkha)
- [Simon Arlott: Modifying Logitech Z906 speakers](https://nom.is/2021/03/04/modifying-logitech-z906-speakers)
- [Logitech Z906 technical specifications](https://support.logi.com/hc/en-us/articles/360023466353-Z906-Technical-Specifications)
- [Logitech support: Connecting a computer to the Z906](https://support.logi.com/hc/en-us/articles/360023401833-Connecting-a-computer-to-the-Z906)

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

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
- add a config flow if YAML setup becomes limiting
- add tests against Home Assistant's custom-component test helpers

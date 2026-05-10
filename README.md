# Z906 IR Remote HA

Minimal Home Assistant custom integration for controlling a Logitech Z906
speaker system through the Home Assistant `infrared` entity platform.

[![Open your Home Assistant instance and open this repository in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mastertape&repository=z906-ir-remote-ha&category=integration)

This is a proof-of-concept consumer integration for the Home Assistant infrared
architecture introduced in Home Assistant 2026.4:

1. Device/protocol knowledge lives in Home Assistant.
2. Commands are encoded with `infrared-protocols`.
3. Commands are sent with `infrared.async_send_command`.
4. Hardware is selected by `infrared.*` entity ID.
5. ESPHome IR/RF proxy devices act only as transport emitters.

## Requirements

- Home Assistant 2026.5.0 or newer.
- HACS installed.
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

Enable the integration from YAML. For example, with Home Assistant packages:

```yaml
z906_ir_remote_ha:
```

Then restart Home Assistant again or reload YAML if your setup supports it.

## Services

After Home Assistant has started, the integration registers two services:

- `z906_ir_remote_ha.send_nec`
- `z906_ir_remote_ha.send_z906`

### Generic NEC / extended NEC

```yaml
action: z906_ir_remote_ha.send_nec
data:
  entity_id: infrared.xiao_smart_ir_mate_ir_proxy_transmitter
  address: "0xA002"
  command: "0xAA"
  modulation: 38650
  repeat_count: 0
```

### Logitech Z906

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

## Manual installation

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

## Scope

This intentionally does not provide a config flow, UI, device database, ESPHome
buttons, or direct ESPHome service calls.

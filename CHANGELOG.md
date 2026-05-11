# Changelog

All notable changes to this project will be documented in this file.

This project follows a simple Keep a Changelog-style format.

## [0.4.3] - 2026-05-11

### Changed

- Clarified that the XIAO IR Mate should be flashed from the ESPHome Ready-Made Projects page with the ESPHome IR/RF proxy firmware.
- Added the concrete Ready-Made Projects flow: choose `Infrared & radio frequency proxy`, pick `XIAO IR Mate`, and press `Connect`.
- Documented that the factory demo firmware is not enough because this integration requires a real Home Assistant `infrared.*` emitter entity.
- Added a note that source labels can be customized to match the user's connected devices, with assistant-compatibility caveats.

## [0.4.2] - 2026-05-11

### Changed

- Renamed the visible project/HACS/integration display name to `Logitech Z906 IR Proxy`.
- Kept the Home Assistant domain `z906_ir_remote_ha` unchanged for backward compatibility with existing YAML, services, and entity history.

## [0.4.1] - 2026-05-11

### Changed

- Improved README hardware/setup documentation with official ESPHome IR/RF proxy references.
- Clarified that the integration is transport-agnostic and targets any compatible Home Assistant `infrared.*` emitter entity.
- Documented the Seeed Studio XIAO IR Mate with official ESPHome IR/RF proxy firmware as the tested reference emitter, not as a hard dependency.
- Distinguished the official ESPHome IR/RF proxy firmware from the older Seeed factory slot-based firmware.

## [0.4.0] - 2026-05-11

### Changed

- Changed media player power and mute to explicit commanded-state semantics.
- `turn_on`, `turn_off`, `mute`, and `unmute` now always transmit their toggle IR command when explicitly requested.
- The stored assumed state is updated to the commanded target state after transmission.
- This prevents voice commands from being silently ignored after state drift or routine mains-power cuts.

## [0.3.1] - 2026-05-11

### Changed

- Corrected documentation for Logitech Z906 behavior after mains power loss.
- Removed the incorrect statement that the stock Z906 restores the previous on/off state after mains power is restored.
- Documented that a stock Z906 returns physically off / in standby after mains power is restored, based on user testing and independent reverse-engineering notes.
- Documented possible optimistic Home Assistant power-state drift after mains restoration.
- Documented manual recovery with the existing low-level `z906_ir_remote_ha.send_z906` service and `power_toggle` command.
- Added this changelog and linked it from the README.

### Unchanged

- No runtime media player behavior changed.
- Optimistic power and mute remain intentional media player features.
- Existing low-level services remain unchanged.

## [0.3.0] - 2026-05-11

### Added

- Added optimistic media player power support with `turn_on` and `turn_off`.
- Added optimistic media player mute support with `volume_mute`.
- Added restored assumed power, mute, and selected-source state.
- Added `initial_power_state` YAML option for first boot before state restore exists.
- Added `initial_mute_state` YAML option for first boot before state restore exists.

## [0.2.0] - 2026-05-11

### Added

- Added a real `media_player` receiver entity for the Logitech Z906.
- Added source selection through the known direct input IR commands.
- Added relative volume up/down support through the media player entity.
- Added assistant-compatible default source names:
  - `INPUT 1`
  - `INPUT 2`
  - `OPTICAL 1`
  - `OPTICAL 2`
  - `COAX 1`
  - `AUX 1`
- Added optional YAML customization for media player name, emitter entity, and source labels.

## [0.1.0] - 2026-05-10

### Added

- Initial Home Assistant custom integration proof of concept.
- Added generic NEC / extended NEC service: `z906_ir_remote_ha.send_nec`.
- Added Logitech Z906 command service: `z906_ir_remote_ha.send_z906`.
- Used `infrared-protocols` to create NEC command objects.
- Sent commands through Home Assistant's official `infrared.async_send_command(...)` helper.
- Kept IR hardware replaceable through a selected `infrared.*` emitter entity.
- Preserved the Home Assistant 2026.4+ infrared architecture without ESPHome-specific command buttons or direct ESPHome service calls.

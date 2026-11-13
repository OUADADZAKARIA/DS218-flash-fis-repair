# What remains uncertain

| Point | Status |
|---|---|
| **How the partition table was lost** | **Unknown.** Unconfirmed hypothesis: an interrupted `updater` write during tests with an unstable board |
| **Which hardware intervention stabilised the board** | Unknown: the repeated reflow of the 4 RAM chips, the metal cooling and pressure element on U3, the fan, or a combination. It was not isolated |
| **Exact RAM chip references** | To be verified on the board |
| **Role of the grey metal plate** | Unknown: original or added? Its usefulness (heat dissipation, pressure on U3) was not demonstrated |
| **RAM tests in U-Boot** | No error detected ([RAM tests](04-hardware-intervention.md#ram-tests-low-and-high-zones)), but they did not reproduce the original intermittent fault. They therefore do not prove stability on their own |
| **Hardware stability over time** | Partial: 3 cold boots and several dozen minutes without a crash. A several-hour test remains to be done |
| **DSM updates** | An update rewrites `zImage` and `rd.gz` in the flash: do it only on a board known to be stable, with a flash backup taken from the working system |
| **DSM 7.x versions supported by the DS218** | Not formally verified: DSM 7.4.1-90080 Update 1 worked on this NAS, nothing more |

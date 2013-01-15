b3-namechanger
==============

B3 plugin useful for catching namechangers


Installation
------------
Installs as any other B3 plugin. No plugin configuration file included nor needed.


Usage
-----
When ingame, one can use the command to track players that have changed their name during a defined scan duration
using the command `!namechanger [delay] [amount] (or its alias, !nc)`.

`delay` is a time delay in seconds between each scan(lower delay better for faster namechangers)
`amount` is the number of checks to be made before reporting back.

A scan will delay*amount number of seconds to complete, and using the command without any parameters will default to
`delay = 1 second`
`amount = 3 times`

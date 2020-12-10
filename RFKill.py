#	quickwifiap - Quickly configure a WiFi AP with DHCP, DNS and IP masquerading
#	Copyright (C) 2019-2020 Johannes Bauer
#
#	This file is part of quickwifiap.
#
#	quickwifiap is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	quickwifiap is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import os
import sys
import json
import subprocess

class RFKill():
	def __init__(self):
		self._phy_for_dev = { }
		base_dir = "/sys/kernel/debug/ieee80211"
		for phy in os.listdir(base_dir):
			phy_dirname = "%s/%s" % (base_dir, phy)
			if not os.path.isdir(phy_dirname):
				continue
			for filename in os.listdir(phy_dirname):
				if filename.startswith("netdev:"):
					netdev = filename[7:]
					self._phy_for_dev[netdev] = phy

		self._phy_ids = { }
		rfkill_list = json.loads(subprocess.check_output([ "rfkill", "-J" ]))
		for devlist in rfkill_list.values():
			for device in devlist:
				self._phy_ids[device["device"]] = device["id"]

	def unblock(self, netdev):
		if netdev not in self._phy_for_dev:
			print("Unable to RFKILL unblock %s: Cannot determine appropriate PHY." % (netdev), file = sys.stderr)
			return

		phy = self._phy_for_dev[netdev]
		if phy not in self._phy_ids:
			print("Unable to RFKILL unblock %s on PHY %s: Cannot determine PHY ID." % (netdev, phy), file = sys.stderr)
			return

		phy_id = self._phy_ids[phy]
		subprocess.check_call([ "rfkill", "unblock", str(phy_id) ])

if __name__ == "__main__":
	rfkill = RFKill()
	rfkill.unblock("wlan0")

#	quickwifiap - Quickly configure a WiFi AP with DHCP, DNS and IP masquerading
#	Copyright (C) 2019-2019 Johannes Bauer
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

import re

class NetSpecification():
	_IPV4_CIDR = re.compile(r"(?P<ip1>\d{1,3})\.(?P<ip2>\d{1,3})\.(?P<ip3>\d{1,3})\.(?P<ip4>\d{1,3})/(?P<subnet>\d{1,2})")

	def __init__(self, ip, subnet = None, ipv4 = True):
		assert(isinstance(ip, int))
		if subnet is None:
			if ipv4:
				subnet = (1 << 32) - 1
			else:
				subnet = (1 << 128) - 1
		assert(isinstance(subnet, int))
		self._ip = ip & subnet
		self._subnet = subnet
		self._ipv4 = ipv4
		if ipv4:
			assert(0 <= self._ip < 2 ** 32)
			assert(0 <= self._subnet < 2 ** 32)
		else:
			assert(0 <= self._ip < 2 ** 128)
			assert(0 <= self._subnet < 2 ** 128)


	@property
	def ip(self):
		return self._ip

	@property
	def subnet(self):
		return self._subnet

	@property
	def is_single_ip(self):
		netlength = 32 if self.is_ipv4 else 128
		return self.subnet == (1 << netlength) - 1

	@property
	def ipstr(self):
		if self.is_ipv4:
			return self._to_ipv4_notation(self.ip)
		else:
			return self._to_ipv6_notation(self.ip)

	@property
	def subnetstr(self):
		if self.is_ipv4:
			return self._to_ipv4_notation(self.subnet)
		else:
			return self._to_ipv6_notation(self.subnet)

	@property
	def is_ipv4(self):
		return self._ipv4

	@staticmethod
	def _to_ipv4_notation(ip):
		return ".".join("%d" % (value) for value in ip.to_bytes(length = 4, byteorder = "big"))

	@staticmethod
	def _to_ipv6_notation(ip):
		return ":".join("%02x%02x" % (ip[i], ip[i + 1]) for i in range(0, len(ip), 2))

	@classmethod
	def parse(cls, text):
		match = cls._IPV4_CIDR.fullmatch(text)
		if match is not None:
			match = { key: int(value) for (key, value) in match.groupdict().items() }
			ip = sum(value << (8 * shift) for (shift, value) in enumerate([match["ip4"], match["ip3"], match["ip2"], match["ip1"]]))
			subnet = ((1 << match["subnet"]) - 1) << (32 - match["subnet"])
			return cls(ip, subnet)
		raise Exception("Cannot parse network specification: %s" % (text))

	@property
	def first_addr(self):
		return self.ip_offset(0)

	@property
	def last_addr(self):
		address = self.ip | ~self.subnet
		return NetSpecification(address, ipv4 = self.is_ipv4)

	def ip_offset(self, offset = 0):
		return NetSpecification(self._ip + offset, ipv4 = self.is_ipv4)

	def __str__(self):
		if self.is_single_ip:
			return "%s" % (self.ipstr)
		else:
			return "%s/%s" % (self.ipstr, self.subnetstr)

# Copyright (C) 2025 the baldaquin team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Test suite for serial_.py
"""

from baldaquin import serial_


def test_device_id(pid: int = 0x0043, vid: int = 0x2341) -> None:
    """Test the DeviceId data class.
    """
    dev_id = serial_.DeviceId(vid, pid)
    print(dev_id)
    assert dev_id.vid == vid
    assert dev_id.pid == pid
    assert dev_id == serial_.DeviceId(vid, pid)
    assert dev_id != serial_.DeviceId(vid + 1, pid)
    # Check the comparison between a DeviceId object and a tuple.
    assert dev_id == (vid, pid)
    assert dev_id != (vid + 1, pid)


def test_list_com_ports() -> None:
    """Test the COM port listing.
    """
    ports = serial_.list_com_ports()
    for port in ports:
        print(port)
    assert isinstance(ports, list)
    assert all(isinstance(port, serial_.Port) for port in ports)
    ports = serial_.list_com_ports((0x2341, 0x0043))
    for port in ports:
        print(port)

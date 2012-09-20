# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#  Copyright (c) 2011 Openstack, LLC.
#  All Rights Reserved.
#
#     Licensed under the Apache License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may obtain
#     a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#     WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#     License for the specific language governing permissions and limitations
#     under the License.
#

"""
nicira network helper module
"""

import logging
import subprocess


class NVPCmdError(Exception):
    def __init__(self, status, *args, **kwargs):
        self.status = status


def run_cmd(cmd):
    # Restart network
    logging.debug("executing %s" % ' '.join(cmd))
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env={})
    logging.debug('waiting on pid %d' % p.pid)
    p.wait()
    status = p.returncode
    logging.debug('"%s" exited with code %d', ' '.join(cmd), status)

    if status != 0:
        raise NVPCmdError(status)


def nvp_cmd(cmd):
    c = ["su", "admin"]
    c.extend(cmd)
    return run_cmd(c)


def _configure_network(hostname, interfaces):
    # Reset state
    nvp_cmd(["clear", "network", "routes"])
    nvp_cmd(["clear", "network", "dns-servers"])
    nvp_cmd(["clear", "network", "ntp-servers"])

    # Set the hostname
    nvp_cmd(["set", "hostname", hostname])

    dns_servers = []

    ifnames = interfaces.keys()
    ifnames.sort()

    gateway = None

    for ifname in ifnames:
        interface = interfaces[ifname]
        ip4s = interface.get("ip4s")
        if not ip4s:
            logging.warn("interface (%s) has not ipv4 ips, skipping",
                         ifname)
            continue

        ip = ip4s[0]
        if len(ip4s) > 1:
            logging.warn("multiple ips (%s) on interface, using %s",
                         ", ".join(ip4s), ip["address"])

        dns_servers.extend(interface.get('dns', []))

        nvp_cmd(["set", "network", "interface", ifname, "ip", "config",
                 "static", ip["address"], ip["netmask"]])

        if not gateway:
            gateway = interface.get("gateway4")

            if gateway:
                nvp_cmd(["add", "network", "default-route", gateway])

        for route in interface['routes']:
            nvp_cmd(["add", "networks", "route", route["network"],
                     route["netmask"], route["gateway"]])

    for dns_server in dns_servers:
        nvp_cmd(["add", "network", "dns-server", dns_server])


def configure_network(hostname, interfaces):
    try:
        _configure_network(hostname, interfaces)
    except NVPCmdError as e:
        logging.exception("error running cmd")
        return (500, "Couldn't setup network: %d" % e.status)
    return(0, '')


def get_interface_files(interfaces):
    return {"interfaces": ''}

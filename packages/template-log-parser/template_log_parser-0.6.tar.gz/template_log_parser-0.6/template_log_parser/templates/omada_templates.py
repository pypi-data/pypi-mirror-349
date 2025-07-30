from template_log_parser.column_functions import (
    calc_time,
    calc_data_usage,
    split_name_and_mac,
)

# Base templates for Omada Log Analysis

# Client Activity #####################################################################################################
# Blocked
blocked = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "failed to connected to [{network_device_type}:{network_device}:{network_device_mac}] "
    'with SSID "{ssid}" on channel {channel} because the user '
    "is blocked by Access Control.({number} {discard_text})"
)

blocked_mac = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}]"
    ' failed to connect to [{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" '
    "on channel {channel} because the user was blocked by MAC block/MAC Filter/Lock To AP.({number} {discard_text})"
)

# Connections
conn_hw = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "is connected to [{network_device_type}:{network_device}:{network_device_mac}] on {network} network."
)

conn_w = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'is connected to [{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" '
    "on channel {channel}."
)

# Disconnections
disc_hw = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'was disconnected from network "{network}" on [{network_device_type}:{network_device}:{network_device_mac}]'
    "(connected time:{connected_time} connected, traffic: {data})."
)

disc_w = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'is disconnected from SSID "{ssid}" on [{network_device_type}:{network_device}:{network_device_mac}] '
    "({connected_time} connected, {data})."
)

disc_hw_recon = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'was disconnected from network "{disc_network}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}](connected time:{connected_time} "
    'connected, traffic: {data}) and connected to network "{recon_network}" on '
    "[{recon_network_device_type}:{recon_network_device}:{recon_network_device_mac}]."
)

disc_w_recon = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'is disconnected from SSID "{disc_ssid}" on [{network_device_type}:{network_device}:{network_device_mac}] '
    '({connected_time} connected, {data}) and connected to SSID "{recon_ssid}" on '
    "[{recon_network_device_type}:{recon_network_device}:{recon_network_device_mac}]."
)

# DHCP
dhcp_assign = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "DHCP Server allocated IP address {client_ip} for the client[MAC: {client_mac}].#015"
)

dhcp_decline = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "DHCP Server received DHCP Decline from client {client_ip}. IP address {client_mac} is not available.#015"
)

dhcp_reject = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - DHCP Server rejected the request"
    " of the client[MAC: {client_mac} IP: {client_ip}].#015"
)

# Failed connections
failed_w = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}]"
    ' failed to connect to [{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" on'
    " channel {channel} because the password was wrong.({number} {discard_text})"
)
# Offline
offline_hw = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'went offline from network "{network}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}](connected time:{connected_time} "
    "connected, traffic: {data})."
)

offline_w = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}]"
    '  went offline from SSID "{ssid}" on [{network_device_type}:{network_device}:{network_device_mac}]'
    " ({connected_time} connected, {data})."
)

offline_w_username = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    '(IP: {client_ip}, Username: {username}) went offline from SSID "{ssid}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}] ({connected_time} connected, {data})."
)

offline_w_no_username = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}]"
    ' (IP: {client_ip}) went offline from SSID "{ssid}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}] ({connected_time} connected, {data})."
)

# Online
online_hw = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "went online on [{network_device_type}:{network_device}:{network_device_mac}] on {network} network."
)

online_w = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}]"
    "  went online on [{network_device_type}:{network_device}:{network_device_mac}] "
    'with SSID "{ssid}" on channel {channel}.'
)

online_w_username = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "(IP: {client_ip}, Username:{username}) went online on "
    '[{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" on channel {channel}.'
)

online_w_no_username = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}]"
    " (IP: {client_ip}) went online on [{network_device_type}:{network_device}:{network_device_mac}]"
    ' with SSID "{ssid}" on channel {channel}.'
)

# Roaming
roaming = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "is roaming from [{network_device_type}:{network_device}:{network_device_mac}][Channel {channel}] to "
    "[{roaming_network_device_type}:{roaming_network_device}:{roaming_network_device_mac}][channel {roaming_channel}] "
    "with SSID {roaming_ssid}"
)


# Logins ##############################################################################################################
login = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "{user} logged in to the controller from {client_ip}."
)

failed_login = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "{user} failed to log in to the controller from {client_ip}."
)

# Network device activity #############################################################################################
device_connected = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was connected."
)

device_disconnected = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was disconnected."
)

dhcps = "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - DHCPS initialization {result}.#015"

got_ip_address = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] "
    "got IP address {ip_address}/{subnet_mask}."
)

online_detection = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}]: "
    "The online detection result of [{interface}] was {state}.#015"
)

up_or_down = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "[{interface}] of [{network_device_type}:{network_device}:{network_device_mac}] is {state}.#015"
)

upgrade = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was upgrade to {result}"
)

# System ##############################################################################################################
auto_backup = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "Auto Backup executed with generating file {filename}."
)

auto_backup_2 = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "Backup Schedule executed with generating file {filename}."
)

log_storage_limit = (
    "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - "
    "The number of logs is about to reach the storage limit of the Controller. "
    "Please back up the data in time, otherwise oldest data will be deleted after the limit is reached."
)

generic_message = "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - {message}"

resolved = "{time} {hardware_controller}  {omada_date} {omada_time} {controller} - - - Resolved: {message}"


client_activity_dict = {
    "blocked by Access Control": [blocked, 13, "blocked"],
    "blocked by MAC": [blocked_mac, 13, "blocked"],
    "failed to connect": [failed_w, 13, "failed_wireless_connection"],
    "is connected to": [conn_hw, 10, "hardwired_connection"],
    "connected to": [conn_w, 11, "wireless_connection"],
    "allocated IP address": [dhcp_assign, 7, "dhcp_assign"],
    "rejected the request": [dhcp_reject, 7, "dhcp_reject"],
    "DHCP Decline": [dhcp_decline, 7, "dhcp_decline"],
    "was disconnected from network": [disc_hw, 12, "hardwired_disconnect"],
    "is disconnected from SSID": [disc_w, 12, "wireless_disconnect"],
    "disconnected from network": [disc_hw_recon, 16, "hardwired_reconnect"],
    "disconnected from SSID": [disc_w_recon, 16, "wireless_reconnect"],
    "went online": [online_hw, 10, "hardwired_online"],
    "went offline from network": [offline_hw, 12, "hardwired_offline"],
    "went online on": [online_w_username, 13, "wireless_online_username"],
    " went online on ": [online_w, 11, "wireless_online"],
    " went online ": [online_w_no_username, 12, "wireless_online_no_username"],
    "went offline from SSID": [offline_w_username, 14, "wireless_offline_username"],
    "went offline from SSID ": [offline_w, 12, "wireless_offline"],
    " went offline from SSID": [
        offline_w_no_username,
        13,
        "wireless_offline_no_username",
    ],
    "roaming": [roaming, 15, "roaming"],
}

logins_dict = {
    "logged in to": [login, 7, "login"],
    "failed to log in": [failed_login, 7, "failed_login"],
}

network_devices_activity_dict = {
    "was connected.": [device_connected, 8, "device_connected"],
    "was disconnected.": [device_disconnected, 8, "device_disconnected"],
    "DHCPS initialization": [dhcps, 6, "dhcps_initialization"],
    "] of [": [
        up_or_down,
        10,
        "interface_up_or_down",
    ],  # This search string is pretty goofy, but it works
    "got IP address": [got_ip_address, 10, "device_dhcp_assign"],
    "online detection": [online_detection, 10, "online_detection"],
    "upgrade": [upgrade, 9, "upgrade"],
}

system_dict = {
    "Auto Backup executed": [auto_backup, 6, "auto_backup"],
    "Backup Schedule": [auto_backup_2, 6, "auto_backup"],
    "about to reach the storage limit": [log_storage_limit, 5, "log_storage_limit"],
    "- {": [generic_message, 6, "generic_message"],
    "Resolved": [resolved, 6, "resolved"],
}

omada_template_dict = {
    **client_activity_dict,
    **logins_dict,
    **network_devices_activity_dict,
    **system_dict,
}


# Additional Dictionaries
# Three columns need cleanup, connection time, data usage, and client_name/mac
omada_column_process_dict = {
    "connected_time": [calc_time, "conn_time_min"],
    "data": [calc_data_usage, "data_usage_MB"],
    "client_name_and_mac": [split_name_and_mac, ["client_name", "client_mac"]],
}

# Merging events for consolidation
omada_merge_events_dict = {
    "client_activity": [value[2] for value in client_activity_dict.values()],
    "logins": [value[2] for value in logins_dict.values()],
    "network_device_activity": [value[2] for value in network_devices_activity_dict.values()],
    "system": [value[2] for value in system_dict.values()],
}

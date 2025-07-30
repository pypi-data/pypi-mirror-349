# Base templates for PFSense Log Analysis
# Note: These templates adhere to syslog format

from template_log_parser.column_functions import split_by_delimiter

# # Filter Log

# ICMP
filter_log_icmp_ipv4_address_mask = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},address mask{message}"
filter_log_icmp_ipv4_information = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},information {message}"
filter_log_icmp_ipv4_maskreply = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},maskreply,{message}"
filter_log_icmp_ipv4_redirect = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},redirect,{message}"
filter_log_icmp_ipv4_reply = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},reply,{icmp_ipv4_reply_info}"
filter_log_icmp_ipv4_request = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},request,{icmp_ipv4_request_info}"
filter_log_icmp_ipv4_router = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},router {message}"
filter_log_icmp_ipv4_source = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},source {message}"
filter_log_icmp_ipv_time_exceed = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},timexceed,{message}"
filter_log_icmp_ipv4_type = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},type-{type}"
filter_log_icmp_ipv4_tstamp = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},tstamp,{icmp_ipv4_tstamp_info}"
filter_log_icmp_ipv4_tstampreply = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},tstampreply,{icmp_ipv4_tstampreply_info}"
filter_log_icmp_ipv4_unreachport = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},unreachport,{icmp_ipv4_unreachport_info}"
filter_log_icmp_ipv4_unreachproto = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},unreachproto,{icmp_ipv4_unreachproto_info}"
filter_log_icmp_ipv4_unreach = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},icmp,{icmp_ipv4_ip_info},unreach,{message}"

filter_log_icmp_ipv6 = "{time} {firewall} filterlog[{process_id}] {rule_info},6,{icmp_ipv6_protocol_info},ICMPv6,{icmp_ipv6_ip_info}"

# MISC
filter_log_esp_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},esp,{ipv4_ip_info}"
filter_log_idrp_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},idrp,{ipv4_ip_info}"
filter_log_igmp_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},igmp,{ipv4_ip_info}"
filter_log_fire_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},fire,{ipv4_ip_info}"
filter_log_gre_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},gre,{ipv4_ip_info}"
filter_log_mobile_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},mobile,{ipv4_ip_info}"
filter_log_rvd_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},rvd,{ipv4_ip_info}"
filter_log_sctp_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},sctp,{sctp_ipv4_ip_info}"
filter_log_sun_nd = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},sun-nd,{ipv4_ip_info}"
filter_log_swipe_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},swipe,{ipv4_ip_info}"
filter_log_unknown_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},unknown,{ipv4_ip_info}"

filter_log_ipv4_in_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},ipencap,{ipv4_in_ipv4_ip_info},IPV4-IN-IPV4,"
filter_log_ipv6_in_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},ipv6,{ipv4_in_ipv6_ip_info},IPV6-IN-IPV4,"

# TCP
filter_log_tcp_ipv4_bad_options = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},tcp,{tcp_ipv4_ip_info}[bad opt]{message}"
filter_log_tcp_ipv4_error = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},tcp,{tcp_ipv4_error_ip_info},errormsg={message}"
filter_log_tcp_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},tcp,{tcp_ipv4_ip_info}"

# UDP
filter_log_udp_ipv4 = "{time} {firewall} filterlog[{process_id}] {rule_info},4,{ipv4_protocol_info},udp,{udp_ipv4_ip_info}"


# General
cmd = "{time} {firewall} {source}[{process_id}] ({user}) CMD ({command})"
check_reload_status = "{time} {firewall} check_reload_status[{process_id}] {message}"
cron = "{time} {firewall} {path}cron[{process_id}] {message}"
dhclient = "{time} {firewall} dhclient[{process_id}] {message}"
dhcp_lfc = "{time} {firewall} DhcpLFC[{process_id}] {level}  {message}"
kea_dhcp4 = "{time} {firewall} kea-dhcp4[{process_id}] {levelt}  {message}"
kernel = "{time} {firewall} kernel {item}: {message}"
nginx = '{time} {firewall} nginx {dest_ip} - {user} [{timestamp}] "{type} {message}"'
nginx_error = "{time} {firewall} nginx {message_time} [error] {message}"
ntpd = "{time} {firewall} ntpd[{process_id}] {message}"
openvpn = "{time} {firewall} openvpn[{process_id}] {message}"
php = "{time} {firewall} php[{process_id}] {message}"
php_fpm = "{time} {firewall} php-fpm[{process_id}]{message}"
pkg_static = "{time} {firewall} pkg-static[{process_id}] {message}"
rc_gateway_alarm = "{time} {firewall} rc.gateway_alarm[{process_id}] {message}"
root = "{time} {firewall} root[{process_id}] {message}"
sudo = "{time} {firewall} sudo[{process_id}] {message}"
sshd = "{time} {firewall} sshd[{process_id}] {message}"
sasldblistusers2 = "{time} {firewall} sasldblistusers2[{process_id}] {message}"
saslpasswd2 = "{time} {firewall} saslpasswd2[{process_id}] {message}"
sshguard = "{time} {firewall} sshguard[{process_id}] {message}"
syslogd = "{time} {firewall} syslogd {message}"
unbound = "{time} {firewall} unbound[{process_id}] {message}"
upsd = "{time} {firewall} upsd[{process_id}] {message}"
upsmon = "{time} {firewall} upsmon[{process_id}] {message}"
usbhid = "{time} {firewall} usbhid-ups[{process_id}] {message}"

filter_log_dict = {
    # TCP
    # Search these templates before the standard tcp ipv4 template
    "tcp,": [filter_log_tcp_ipv4_error, 7, "filter_tcp_ipv4_error"],
    ",tcp": [filter_log_tcp_ipv4_bad_options, 7, "filter_tcp_ipv4_bad_options"],
    "tcp": [filter_log_tcp_ipv4, 6, "filter_tcp_ipv4"],  # Standard tcp ipv4 template
    # ICMP
    "address mask": [filter_log_icmp_ipv4_address_mask, 7, "filter_icmp_ipv4_address_mask"],
    "information": [filter_log_icmp_ipv4_information, 7, "filter_icmp_ipv4_information"],
    "maskreply": [filter_log_icmp_ipv4_maskreply, 7, "filter_icmp_ipv4_maskreply"],
    "type": [filter_log_icmp_ipv4_type, 7, "filter_icmp_ipv4_type"],
    "reply": [filter_log_icmp_ipv4_reply, 7, "filter_icmp_ipv4_reply"],
    "request": [filter_log_icmp_ipv4_request, 7, "filter_icmp_ipv4_request"],
    "router": [filter_log_icmp_ipv4_router, 7, "filter_icmp_ipv4_router"],
    "source": [filter_log_icmp_ipv4_source, 7, "filter_icmp_ipv4_source"],
    "timexceed": [filter_log_icmp_ipv_time_exceed, 7, "filter_icmp_ipv4_time_exceed"],
    "tstamp": [filter_log_icmp_ipv4_tstamp, 7, "filter_icmp_ipv4_tstamp"],
    "tstampreply": [filter_log_icmp_ipv4_tstampreply, 7, "filter_icmp_ipv4_tstampreply"],
    "unreachport": [filter_log_icmp_ipv4_unreachport, 7, "filter_icmp_ipv4_unreachport"],
    "unreachproto": [filter_log_icmp_ipv4_unreachproto, 7, "filter_icmp_ipv4_unreachproto"],
    "unreach,": [filter_log_icmp_ipv4_unreach, 7, "filter_icmp_ipv4_unreach"],
    "redirect": [filter_log_icmp_ipv4_redirect, 7, "filter_icmp_ipv4_redirect"],
    "ICMPv6": [filter_log_icmp_ipv6, 6, "filter_icmp_ipv6"],
    # Misc
    "esp": [filter_log_esp_ipv4, 6, "filter_esp_ipv4"],
    "fire": [filter_log_fire_ipv4, 6, "filter_fire_ipv4"],
    "gre": [filter_log_gre_ipv4, 6, "filter_gre_ipv4"],
    "idrp": [filter_log_idrp_ipv4, 6, "filter_idrp_ipv4"],
    "igmp": [filter_log_igmp_ipv4, 6, "filter_igmp_ipv4"],
    "mobile": [filter_log_mobile_ipv4, 6, "filter_mobile_ipv4"],
    "rvd": [filter_log_rvd_ipv4, 6, "filter_rvd_ipv4"],
    "sctp": [filter_log_sctp_ipv4, 6, "filter_sctp_ipv4"],
    "sun-nd": [filter_log_sun_nd, 6, "filter_sun_nd_ipv4"],
    "swipe": [filter_log_swipe_ipv4, 6, "filter_swipe_ipv4"],
    "unknown": [filter_log_unknown_ipv4, 6, "filter_ipv4_unknown"],
    "IPV6-IN-IPV4": [filter_log_ipv6_in_ipv4, 6, "filter_ipv6_in_ip4v"],
    "IPV4-IN-IPV4": [filter_log_ipv4_in_ipv4, 6, "filter_ipv4_in_ipv4"],
    # UDP
    "udp": [filter_log_udp_ipv4, 6, "filter_udp_ipv4"],
}

general_dict = {
    "CMD": [cmd, 6, "cmd"],
    "check_reload_status": [check_reload_status, 4, "check_reload_status"],
    "cron": [cron, 5, "cron"],
    "dhclient": [dhclient, 4, "dhclient"],
    "kea-dhcp4": [kea_dhcp4, 5, "kea_dhcp4"],
    "kernel": [kernel, 4, "kernel"],
    "DhcpLFC": [dhcp_lfc, 5, "dhcp_lfc"],
    "nginx": [nginx, 7, "nginx"],
    "error": [nginx_error, 4, "nginx_error"],
    "ntpd": [ntpd, 4, "ntpd"],
    "openvpn[": [openvpn, 4, "openvpn"],
    "pkg-static": [pkg_static, 4, "pkg_static"],
    "php[": [php, 4, "php"],
    "php-fpm": [php_fpm, 4, "php_fpm"],
    "rc.gateway_alarm": [rc_gateway_alarm, 4, "rc_gateway_alarm"],
    "root": [root, 4, "root"],
    "sasldblistusers2": [sasldblistusers2, 4, "sasldblistusers2"],
    "saslpasswd2": [saslpasswd2, 4, "saslpasswd2"],
    "sudo": [sudo, 4, "sudo"],
    "sshd": [sshd, 4, "sshd"],
    "sshguard": [sshguard, 4, "ssh_guard"],
    "syslogd": [syslogd, 3, "syslogd"],
    "unbound": [unbound, 4, "unbound"],
    "upsd": [upsd, 4, "upsd"],
    "upsmon": [upsmon, 4, "upsmon"],
    "usbhid": [usbhid, 4, "usbhid"],
}

pfsense_template_dict = {**filter_log_dict, **general_dict}

# Rule Columns
generic_rule_info_columns = [
    "rule_number",
    "sub_rule",
    "anchor",
    "tracker",
    "real_interface",
    "reason",
    "action",
    "direction",
]

# Protocol Columns
generic_ipv4_protocol_info_columns = [
    "tos",
    "ecn",
    "ttl",
    "id",
    "offset",
    "flags",
    "protocol_id",
]

icmp_ipv6_protocol_info_columns = [
    "class",
    "flow_label",
    "hop_limit"
]

# IP Info Columns
base_ipv4_ip_info_columns = [
    "length",
    "src_ip",
    "dest_ip"
]

generic_ipv4_ip_info_columns = base_ipv4_ip_info_columns + ["data_length"]

base_ipv4_tcp_udp_ip_info_columns = base_ipv4_ip_info_columns + [
    "src_port",
    "dest_port",
    "data_length",
]

tcp_ipv4_ip_info_error_columns = base_ipv4_tcp_udp_ip_info_columns + ["tcp_flags"]

tcp_ipv4_ip_info_columns = base_ipv4_tcp_udp_ip_info_columns + [
    "tcp_flags",
    "seq_number",
    "ack_number",
    "tcp_window",
    "urg",
    "tcp_options",
]

icmp_ipv6_ip_info_columns = [
    "protocol_id",
    "length",
    "src_ip",
    "dest_ip",
    "icmp_data"
]

# Instance specific Columns
icmp_ipv4_generic_info_columns = [
    "icmp_id",
    "icmp_sequence"
]

icmp_ipv4_unreachport_info_columns = [
    "icmp_dest_ip",
    "unreach_protocol",
    "unreach_port",
]
icmp_ipv4_unreachproto_info_columns = [
    "icmp_dest_ip",
    "unreach_protocol"
]

icmp_ipv4_tstampreply_info_columns = [
    "icmp_id",
    "icmp_sequence",
    "icmp_otime",
    "icmp_rtime",
    "icmp_ttime",
]

split_by_delimiter_column_pairs = {
    # Generic
    "rule_info": generic_rule_info_columns,
    "ipv4_protocol_info": generic_ipv4_protocol_info_columns,
    "ipv4_ip_info": generic_ipv4_ip_info_columns,
    # ICMP
    "icmp_ipv4_ip_info": base_ipv4_ip_info_columns,
    "icmp_ipv4_reply_info": icmp_ipv4_generic_info_columns,
    "icmp_ipv4_request_info": icmp_ipv4_generic_info_columns,
    "icmp_ipv4_tstamp_info": icmp_ipv4_generic_info_columns,
    "icmp_ipv4_tstampreply_info": icmp_ipv4_tstampreply_info_columns,
    "icmp_ipv4_unreachport_info": icmp_ipv4_unreachport_info_columns,
    "icmp_ipv4_unreachproto_info": icmp_ipv4_unreachproto_info_columns,
    "icmp_ipv6_protocol_info": icmp_ipv6_protocol_info_columns,
    "icmp_ipv6_ip_info": icmp_ipv6_ip_info_columns,
    # SCTP
    "sctp_ipv4_ip_info": base_ipv4_tcp_udp_ip_info_columns,
    # TCP
    "tcp_ipv4_ip_info": tcp_ipv4_ip_info_columns,
    "tcp_ipv4_error_ip_info": tcp_ipv4_ip_info_error_columns,
    # UDP
    "udp_ipv4_ip_info": base_ipv4_tcp_udp_ip_info_columns,
    # IPv4 in IPv6, IPv4 in IPv4, etc
    "ipv4_in_ipv6_ip_info": base_ipv4_ip_info_columns,
    "ipv4_in_ipv4_ip_info": base_ipv4_ip_info_columns,
}

pfsense_split_by_delimiter_process_dict = {
    column: [split_by_delimiter, columns]
    for column, columns in split_by_delimiter_column_pairs.items()
}

pfsense_column_process_dict = {**pfsense_split_by_delimiter_process_dict}

pfsense_merge_events_dict = {
    "filter_log": [value[2] for value in filter_log_dict.values()],
    "general": [value[2] for value in general_dict.values()],
}

from template_log_parser.templates.debian_templates import debian_template_dict

# Base templates for Pihole log analysis

# DNSMASQ
pihole_dnsmasq_cached = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: cached {query} is {cached_resolved_ip}"
pihole_dnsmasq_cached_stale = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: cached-stale {query} is {cached_resolved_ip}"
pihole_dnsmasq_compile = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: compile time options: {message}"
pihole_dnsmasq_config = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: config {host} is {result}"
pihole_dnsmasq_domain = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: {type} domain {query} is {result}"
pihole_dnsmasq_exactly_blacklisted = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: exactly blacklisted {query} is {result}"
pihole_dnsmasq_exactly_denied = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: exactly denied {query} is {result}"
pihole_dnsmasq_exiting = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: exiting on receipt of SIGTERM"
pihole_dnsmasq_forward = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: forwarded {query} to {dns_server}"
pihole_dnsmasq_gravity_blocked = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: gravity blocked {query} is {result}"
pihole_dnsmasq_host_name_resolution = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: /etc/hosts {host_ip} is {host_name}"
pihole_dnsmasq_host_name = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: Pi-hole hostname {host_name} is {host_ip}"
pihole_dnsmasq_locally_known = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: using only locally-known addresses for {result}"
pihole_dnsmasq_query = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: query[{query_type}] {destination} from {client}"
pihole_dnsmasq_rate_limiting = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: Rate-limiting {query} is {message}"
pihole_dnsmasq_read = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: read {path} - {names} names"
pihole_dnsmasq_reply = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: reply {query} is {resolved_ip}"
pihole_dnsmasq_reply_truncated = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: reply is truncated"
pihole_dnsmasq_started = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: started, version {version} cachesize {cachesize}"
pihole_dnsmasq_using_nameserver = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: using nameserver {nameserver_ip}#53"

# FTL
pi_ftl_error = "{time} {server_name} piFTL {pihole_time} [{ids}] ERROR: {message}"
pi_ftl_info = "{time} {server_name} piFTL {pihole_time} [{ids}] INFO: {message}"
pihole_ftl_info = "{time} {server_name} pihole-FTL[{id}]: {pihole_time} [{ids}] INFO: {message}"

pihole_dnsmasq = {
    "query": [pihole_dnsmasq_query, 7, "dnsmasq_query"],
    "reply": [pihole_dnsmasq_reply, 6, "dnsmasq_reply"],
    "cached": [pihole_dnsmasq_cached, 6, "dnsmasq_cached"],
    "cached-stale": [pihole_dnsmasq_cached_stale, 6, "dnsmasq_cached_stale"],
    "forwarded": [pihole_dnsmasq_forward, 6, "dnsmasq_forward"],
    "exactly denied": [pihole_dnsmasq_exactly_denied, 6, "pihole_exact_denied"],
    "gravity blocked": [pihole_dnsmasq_gravity_blocked, 6, "dnsmasq_gravity_blocked"],
    "domain": [pihole_dnsmasq_domain, 7, "dnsmasq_domain"],
    "hostname": [pihole_dnsmasq_host_name, 6, "dnsmasq_hostname_resolution"],
    "config": [pihole_dnsmasq_config, 6, "dnsmasq_config"],
    "compile time options": [pihole_dnsmasq_compile, 5, "dnsmasq_compile_time_options"],
    "exactly blacklisted": [pihole_dnsmasq_exactly_blacklisted, 6, "pihole_exact_blacklist"],
    "exiting on receipt of SIGTERM": [pihole_dnsmasq_exiting, 4, "pihole_exiting_sigterm"],
    "hosts": [pihole_dnsmasq_host_name_resolution, 6, "dnsmasq_hostname_resolution"],
    "locally-known": [pihole_dnsmasq_locally_known, 5, "dnsmasq_locally_known"],
    "Rate-limiting": [pihole_dnsmasq_rate_limiting, 6, "dnsmasq_rate_limiting"],
    "read ": [pihole_dnsmasq_read, 6, "dnsmasq_read"],
    "reply is truncated": [pihole_dnsmasq_reply_truncated, 4, "dnsmasq_reply_truncated"],
    "started": [pihole_dnsmasq_started, 6, "dnsmasq_started"],
    "using nameserver": [pihole_dnsmasq_using_nameserver, 5, "dnsmasq_using_nameserver"],
}

pihole_ftl = {
    "ERROR": [pi_ftl_error, 5, "pi_ftl_error"],
    "INFO": [pi_ftl_info, 5, "pi_ftl_info"],
    "INFO:": [pihole_ftl_info, 6, "pihole_ftl_info"],
}


pihole_events_dict = {**pihole_dnsmasq, **pihole_ftl}


# Pihole often runs on debian, so it makes sense to use templates from that dictionary rather than create new ones
pihole_template_dict = {**pihole_events_dict, **debian_template_dict}

# Additional Dictionaries
# Merging events for consolidation
pihole_merge_events_dict = {
    "dnsmasq": [value[2] for value in pihole_dnsmasq.values()],
    "ftl": [value[2] for value in pihole_ftl.values()],
}

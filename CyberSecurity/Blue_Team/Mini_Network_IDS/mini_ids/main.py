for i, iface in enumerate(interfaces):
    iface_name = iface['name']
    iface_mac = iface['mac']
    iface_ip = iface['ip']
    iface_status = "Enabled" if iface['is_enabled'] else "Disabled"
    print(f"[[{i}] {iface_name}] : {iface_status}")
    print(f"  ├─ IP  : {iface_ip}")
    print(f"  └─ MAC : {iface_mac}")
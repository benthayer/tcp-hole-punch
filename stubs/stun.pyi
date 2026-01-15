from typing import Optional

def get_ip_info(
    source_ip: str = ...,
    source_port: int = ...,
    stun_host: Optional[str] = ...,
    stun_port: int = ...
) -> tuple[str, str, int]:
    """Returns (nat_type, external_ip, external_port)"""
    ...



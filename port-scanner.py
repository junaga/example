import asyncio
from random import randint
from ipaddress import IPv4Network, IPv4Address
import os
from collections.abc import Iterator


def generate_ips(path: str) -> Iterator[str]:
    """
    This function is a generator, and will yield an infinite amount of IPv4 addresses.

    IPv4 addresses _already generated_ are in a file `path`, separated by newlines. Those addresses, are not to be yielded again, similar to `excluded`. File integrity is not verified, and the file will be created, and appended into, if it does not exist.
    """

    excluded = [
        IPv4Network("127.0.0.0/8"),  # Localhost
        IPv4Network("10.0.0.0/8"),  # Private network
        IPv4Network("192.168.0.0/16"),  # Private network
        IPv4Network("172.16.0.0/12"),  # Private network
    ]

    # make sure the file exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.path.exists(path) or open(path, "w").close()

    # read the file into memory
    with open(path, "r") as read_file:
        previous = set(read_file.read().splitlines())

    # yield, and append to the file
    with open(path, "a") as append_file:
        while True:
            # this works right now because there is an address space of
            # 256 ^ 4 - EXCLUDED_V4_IPS
            byte = lambda: randint(0, 255)
            four_bytes = f"{byte()}.{byte()}.{byte()}.{byte()}"
            ip_address = IPv4Address(four_bytes)

            skip = False

            if ip_address in previous:
                skip = True
            for ip_addresses in excluded:
                if ip_address in ip_addresses:
                    skip = True

            if not skip:
                previous.add(ip_address)
                append_file.write(f"{ip_address}\n")
                append_file.flush()

                # https://docs.python.org/3/glossary.html#term-generator-iterator
                yield str(ip_address)


async def scan_port(ip: str, port: str):
    """
    This function will attempt to connect to a TCP port on an IPv4 address.

    It's important to note that the absence of a TimeoutError doesn't guarantee that the port is open at all times. Network conditions can change rapidly, and a port that is open one moment may become closed or inaccessible shortly after. Additionally, firewalls, network policies, or other network restrictions can prevent successful connections even if the port is technically open.
    """

    timeout = 2

    # `asyncio.open_connection()` uses `socket.create_connection()`
    connecting = asyncio.open_connection(ip, port)
    timeout_coro = asyncio.wait_for(connecting, timeout=timeout)
    try:
        reader, writer = await timeout_coro
        writer.close()
        await writer.wait_closed()

        if port == 443:
            print(f"found a link!\nhttps://{ip}\n", flush=True)
        elif port == 80:
            print(f"found an unencrypted website!\nhttp://{ip}\n", flush=True)
        else:
            print(f"{ip}:{port}\nhttps://www.infobyip.com/ip-{ip}.html\n", flush=True)
    except:
        pass


async def main():
    path = "./ips.log"
    wellknown = 1023
    start = 0
    end = wellknown

    coros = []
    coros_batch_size = 1024 * 4  # if network is slow, lower this number

    print("scanning for IPv4 TCP ports...", flush=True)
    print("https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers", flush=True)
    print("press CTRL+C to stop\n", flush=True)

    for ip in generate_ips(path):
        for port in range(start, end):
            coros.append(scan_port(ip, port))

            if len(coros) == coros_batch_size:
                await asyncio.gather(*coros)
                coros = []


if __name__ == "__main__":
    asyncio.run(main())

    # best music playlist ever uwuw (lumie wrote this)
    # https://www.youtube.com/watch?v=zp0w346xI28&list=PLQZptMlquotXbF5z3_Z1ZMPwlhpvkahkI&index=1

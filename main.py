import asyncio
import random
import plyer

counts = {}


async def handler(_reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip, port = writer.get_extra_info('peername')

    if ip not in counts:
        plyer.notification.notify(message='Мы поймали новый неопознанный пингующий объект!\n'
                                          f'Его ip: {ip}',
                                  app_name='Trapper Turtle Ha-ha',
                                  app_icon='image.ico',
                                  title='Ой ой... А кто это?!',
                                  toast=True)
    counts.setdefault(ip, {"ports": set(), "cons": 0, "pkg": 0})
    counts[ip]["ports"].add(port)
    counts[ip]["cons"] += 1

    print(f"\nПопался\t{ip}:{port}\t({counts[ip]['cons']})\t" + "=" * 100)

    try:
        while True:
            pkg = await _reader.read(1024)
            try:
                pkg = repr(pkg.decode('windows-1251'))
            except UnicodeDecodeError:
                pass

            if pkg != "''":
                print(f"\tТрафик от {ip}:{port}\t-", pkg)
                counts[ip]["pkg"] += 1

            await asyncio.sleep(10)
            writer.write(b'%x\r\n' % random.randint(0, 2 ** 32))
            await writer.drain()
    except ConnectionResetError:
        pass
    print(f'\nСбежал {ip}:{port}\t' + "=" * 100)


async def main():
    host, port = '0.0.0.0', 22

    print(f'Слушаю на хосте {host}:{port}\n'
          f'Если что-то ниже появится, значит я кого-то поймал и приготовлю его тебе на костре...\n'
          f'==========output==========')

    server = await asyncio.start_server(handler, host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

import { describe, expect, it, vi } from 'vitest';
import { HTTPClient } from '../src/core/http.js';
import { MachineConnection } from '../src/machines/connection.js';
import { MachineTransport } from '../src/machines/transport.js';
import { MachinesResource } from '../src/resources/resources.js';

describe('machines connect', () => {
  it('builds wss url from https base url with auth header', async () => {
    const connectSpy = vi
      .spyOn(MachineTransport, 'connect')
      .mockResolvedValue({
        send: vi.fn(),
        emit: vi.fn(),
        on: vi.fn(),
        close: vi.fn(),
      } as unknown as MachineTransport);

    const client = new HTTPClient({
      apiKey: 'sk-test',
      baseURL: 'https://api.layerbrain.com',
      fetch: vi.fn(),
    });

    const machines = new MachinesResource(client);
    await machines.connect('mach_123');

    expect(connectSpy).toHaveBeenCalledWith(
      'wss://api.layerbrain.com/v1/machines/mach_123/connect',
      { Authorization: 'Bearer sk-test' },
    );

    connectSpy.mockRestore();
  });

  it('builds ws url from http base url', async () => {
    const connectSpy = vi
      .spyOn(MachineTransport, 'connect')
      .mockResolvedValue({
        send: vi.fn(),
        emit: vi.fn(),
        on: vi.fn(),
        close: vi.fn(),
      } as unknown as MachineTransport);

    const client = new HTTPClient({
      apiKey: 'sk-test',
      baseURL: 'http://localhost:8000',
      fetch: vi.fn(),
    });

    const machines = new MachinesResource(client);
    await machines.connect('mach_local');

    expect(connectSpy).toHaveBeenCalledWith(
      'ws://localhost:8000/v1/machines/mach_local/connect',
      { Authorization: 'Bearer sk-test' },
    );

    connectSpy.mockRestore();
  });
});

describe('machine shell and filesystem mapping', () => {
  it('maps shell and inodes methods to transport protocol', async () => {
    const send = vi
      .fn()
      .mockResolvedValueOnce({ stdout: 'ok', stderr: '', code: 0 })
      .mockResolvedValueOnce({ data: [{ name: 'file.txt' }] });

    const transport = {
      send,
      emit: vi.fn(),
      on: vi.fn(),
      close: vi.fn(),
    } as unknown as MachineTransport;

    const connection = new MachineConnection('mach_test', transport);

    const shellResult = await connection.shell.execute('ls', { cwd: '/root/brain', timeout: 30 });
    const files = await connection.filesystem.list('~', false);

    expect(shellResult.stdout).toBe('ok');
    expect(files[0].name).toBe('file.txt');

    expect(send).toHaveBeenNthCalledWith(
      1,
      'shell.execute',
      { command: 'ls', timeout: 30, cwd: '/root/brain' },
      35000,
    );

    expect(send).toHaveBeenNthCalledWith(2, 'inodes.list', { path: '~', all: false });
  });
});

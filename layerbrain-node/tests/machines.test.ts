import { describe, expect, it, vi } from 'vitest';
import { HTTPClient } from '../src/core/http.js';
import { MachineConnection } from '../src/machines/connection.js';
import { MachineTransport } from '../src/machines/transport.js';
import { MachinesResource } from '../src/resources/resources.js';

describe('machines connect', () => {
  it('builds wss url from https base url with upgrade auth', async () => {
    const authenticate = vi.fn();
    const connectSpy = vi
      .spyOn(MachineTransport, 'connect')
      .mockResolvedValue({
        send: vi.fn(),
        authenticate,
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
    await machines.connect('mch_123');

    expect(connectSpy).toHaveBeenCalledWith(
      'wss://api.layerbrain.com/v1/machines/mch_123',
      { Authorization: 'Bearer sk-test', 'x-layerbrain-source': 'api' },
    );
    expect(authenticate).not.toHaveBeenCalled();

    connectSpy.mockRestore();
  });

  it('builds ws url from http base url', async () => {
    const authenticate = vi.fn();
    const connectSpy = vi
      .spyOn(MachineTransport, 'connect')
      .mockResolvedValue({
        send: vi.fn(),
        authenticate,
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
    await machines.connect('mch_local');

    expect(connectSpy).toHaveBeenCalledWith(
      'ws://localhost:8000/v1/machines/mch_local',
      { Authorization: 'Bearer sk-test', 'x-layerbrain-source': 'api' },
    );
    expect(authenticate).not.toHaveBeenCalled();

    connectSpy.mockRestore();
  });

});

describe('machine shell and filesystem mapping', () => {
  it('maps run, shell, and inodes methods to transport protocol', async () => {
    const send = vi
      .fn()
      .mockResolvedValueOnce({ object: 'machine.run_result', result: { stdout: 'v22.22.2\n' } })
      .mockResolvedValueOnce({ stdout: 'ok', stderr: '', code: 0 })
      .mockResolvedValueOnce({ data: [{ name: 'file.txt' }] });

    const transport = {
      send,
      authenticate: vi.fn(),
      emit: vi.fn(),
      on: vi.fn(),
      close: vi.fn(),
    } as unknown as MachineTransport;

    const connection = new MachineConnection('mch_test', transport);

    const runResult = await connection.run('node -v', { timeout: 60 });
    const shellResult = await connection.shell.execute('ls', { cwd: '/root/brain', timeout: 30 });
    const files = await connection.filesystem.list('~', false);

    expect(runResult.result).toEqual({ stdout: 'v22.22.2\n' });
    expect(shellResult.stdout).toBe('ok');
    expect(files[0].name).toBe('file.txt');

    expect(send).toHaveBeenNthCalledWith(
      1,
      'machine.run',
      {
        body: { command: 'node -v', timeout: 60 },
        timeout: 65000,
      },
    );

    expect(send).toHaveBeenNthCalledWith(
      2,
      'shell.execute',
      {
        params: { command: 'ls', timeout: 30, cwd: '/root/brain' },
        timeout: 35000,
      },
    );

    expect(send).toHaveBeenNthCalledWith(3, 'inodes.list', {
      params: { path: '~', all: false },
    });
  });
});

import { describe, expect, it, vi } from 'vitest';
import { HTTPClient } from '../src/core/http.js';
import { MachineConnection } from '../src/machines/connection.js';
import { MachineTransport } from '../src/machines/transport.js';
import { MachinesResource } from '../src/resources/resources.js';

describe('machines connect', () => {
  it('builds wss url from https base url with upgrade auth', async () => {
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
    await machines.connect('mch_123');

    expect(connectSpy).toHaveBeenCalledWith(
      'wss://api.layerbrain.com/v1/machines/mch_123',
      { Authorization: 'Bearer sk-test', 'x-layerbrain-source': 'api' },
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
    await machines.connect('mch_local');

    expect(connectSpy).toHaveBeenCalledWith(
      'ws://localhost:8000/v1/machines/mch_local',
      { Authorization: 'Bearer sk-test', 'x-layerbrain-source': 'api' },
    );

    connectSpy.mockRestore();
  });

});

describe('machine command mapping', () => {
  it('maps exec and session info to the WebSocket protocol', async () => {
    const send = vi
      .fn()
      .mockResolvedValueOnce({
        object: 'machine.command_result',
        stdout: 'ok\n',
        stderr: '',
        exit_code: 0,
        metadata: { transport: 'nsenter' },
      })
      .mockResolvedValueOnce({ object: 'machine.session', state: 'ready' });

    const transport = {
      send,
      emit: vi.fn(),
      on: vi.fn(),
      close: vi.fn(),
    } as unknown as MachineTransport;

    const connection = new MachineConnection('mch_test', transport);

    const execResult = await connection.exec('ls', { cwd: '/root/brain', timeout: 30 });
    const info = await connection.info();

    expect(execResult.stdout).toBe('ok\n');
    expect(execResult.metadata?.transport).toBe('nsenter');
    expect(info.state).toBe('ready');

    expect(send).toHaveBeenNthCalledWith(
      1,
      'machine.command',
      {
        body: { command: 'ls', timeout: 30, cwd: '/root/brain' },
        timeout: 35000,
      },
    );

    expect(send).toHaveBeenNthCalledWith(2, 'session.info');
  });
});

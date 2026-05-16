import { describe, expect, it, vi } from 'vitest';
import { EventEmitter } from 'node:events';
import WebSocket from 'ws';
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
    const controller = new AbortController();
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

    const execResult = await connection.exec('ls', { cwd: '/root/brain', signal: controller.signal });
    const info = await connection.info();

    expect(execResult.stdout).toBe('ok\n');
    expect(execResult.metadata?.transport).toBe('nsenter');
    expect(info.state).toBe('ready');

    expect(send).toHaveBeenNthCalledWith(
      1,
      'machine.command',
      {
        body: { command: 'ls', cwd: '/root/brain' },
        timeout: null,
        signal: controller.signal,
      },
    );

    expect(send).toHaveBeenNthCalledWith(2, 'session.info');
  });

  it('maps explicit exec timeouts to the WebSocket command and request deadline', async () => {
    const send = vi.fn().mockResolvedValue({
      object: 'machine.command_result',
      stdout: 'ok\n',
      stderr: '',
      exit_code: 0,
    });
    const transport = {
      send,
      emit: vi.fn(),
      on: vi.fn(),
      close: vi.fn(),
    } as unknown as MachineTransport;

    const connection = new MachineConnection('mch_test', transport);
    await connection.exec('sleep 1', { timeout: 30 });

    expect(send).toHaveBeenCalledWith(
      'machine.command',
      {
        body: { command: 'sleep 1', timeout: 30 },
        timeout: 35000,
        signal: undefined,
      },
    );
  });
});

describe('machine transport close', () => {
  it('terminates the socket when the close handshake does not finish', async () => {
    vi.useFakeTimers();
    const socket = new EventEmitter() as EventEmitter & {
      readyState: number;
      close: ReturnType<typeof vi.fn>;
      terminate: ReturnType<typeof vi.fn>;
      send: ReturnType<typeof vi.fn>;
    };
    socket.readyState = WebSocket.OPEN;
    socket.close = vi.fn();
    socket.terminate = vi.fn(() => {
      socket.readyState = WebSocket.CLOSED;
    });
    socket.send = vi.fn();
    const transport = new MachineTransport(socket as unknown as WebSocket);

    const close = transport.close(25);
    await vi.advanceTimersByTimeAsync(25);
    await close;

    expect(socket.close).toHaveBeenCalledOnce();
    expect(socket.terminate).toHaveBeenCalledOnce();
    vi.useRealTimers();
  });

  it('rejects pending sends when the abort signal fires', async () => {
    const socket = new EventEmitter() as EventEmitter & {
      readyState: number;
      close: ReturnType<typeof vi.fn>;
      terminate: ReturnType<typeof vi.fn>;
      send: ReturnType<typeof vi.fn>;
    };
    socket.readyState = WebSocket.OPEN;
    socket.close = vi.fn();
    socket.terminate = vi.fn();
    socket.send = vi.fn((_payload: string, callback: (error?: Error) => void) => callback());
    const transport = new MachineTransport(socket as unknown as WebSocket);
    const controller = new AbortController();

    const response = transport.send('machine.command', { signal: controller.signal });
    controller.abort();

    await expect(response).rejects.toThrow('Request aborted: machine.command');
  });
});

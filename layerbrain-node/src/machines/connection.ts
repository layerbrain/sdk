import { MachineTransport } from './transport.js';
import { TimeoutError } from '../core/errors.js';

export interface MachineCommandOptions {
  cwd?: string;
  environment?: Record<string, string>;
  signal?: AbortSignal;
  timeout?: number;
}

export interface MachineCommandResult extends Record<string, unknown> {
  object?: 'machine.command_result';
  exit_code?: number;
  stdout?: string;
  stderr?: string;
  metadata?: Record<string, unknown>;
}

export class MachineConnection {
  constructor(readonly id: string, private readonly transport: MachineTransport) {}

  on(event: string, handler: (data: unknown) => void): () => void {
    return this.transport.on(event, handler);
  }

  emit(method: string, body: Record<string, unknown>): Promise<void> {
    return this.transport.emit(method, body);
  }

  async info(): Promise<Record<string, unknown>> {
    return ((await this.transport.send('session.info')) as Record<string, unknown>) ?? {};
  }

  async exec(command: string | string[], options: MachineCommandOptions = {}): Promise<MachineCommandResult> {
    const body: Record<string, unknown> = {
      command,
    };
    if (options.timeout !== undefined) {
      body.timeout = options.timeout;
    }
    if (options.cwd) {
      body.cwd = options.cwd;
    }
    if (options.environment) {
      body.environment = options.environment;
    }

    let result: unknown;
    try {
      result = await this.transport.send('machine.command', {
        body,
        timeout: options.timeout === undefined ? null : options.timeout * 1000 + 5000,
        signal: options.signal,
      });
    } catch (error) {
      if (error instanceof TimeoutError) {
        await this.close().catch(() => {});
      }
      throw error;
    }
    return (result as MachineCommandResult) ?? {};
  }

  async close(timeout?: number): Promise<void> {
    await this.transport.close(timeout);
  }
}

import { MachineTransport } from './transport.js';

export interface ShellExecuteOptions {
  cwd?: string;
  timeout?: number;
}

export class MachineShell {
  constructor(private readonly transport: MachineTransport) {}

  async execute(command: string, options: ShellExecuteOptions = {}): Promise<Record<string, unknown>> {
    const timeout = options.timeout ?? 30;
    const params: Record<string, unknown> = {
      command,
      timeout,
    };

    if (options.cwd) {
      params.cwd = options.cwd;
    }

    const result = await this.transport.send('shell.execute', params, timeout * 1000 + 5000);
    return (result as Record<string, unknown>) ?? {};
  }
}

export class MachineFilesystem {
  constructor(private readonly transport: MachineTransport) {}

  async list(path = '~', showAll = false): Promise<Record<string, unknown>[]> {
    const result = (await this.transport.send('inodes.list', { path, all: showAll })) as Record<string, unknown>;
    return (Array.isArray(result.data) ? result.data : []) as Record<string, unknown>[];
  }

  async stat(path: string): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.stat', { path })) as Record<string, unknown>) ?? {};
  }

  async read(path: string): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.get', { path })) as Record<string, unknown>) ?? {};
  }

  async write(path: string, data: string, encoding = 'utf-8'): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.put', { path, data, encoding })) as Record<string, unknown>) ?? {};
  }

  async mkdir(path: string): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.mkdir', { path })) as Record<string, unknown>) ?? {};
  }

  async delete(path: string): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.delete', { path })) as Record<string, unknown>) ?? {};
  }

  async move(from: string, to: string): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.move', { from, to })) as Record<string, unknown>) ?? {};
  }

  async copy(from: string, to: string): Promise<Record<string, unknown>> {
    return ((await this.transport.send('inodes.copy', { from, to })) as Record<string, unknown>) ?? {};
  }

  async search(pattern: string, path = '~/brain', limit = 50): Promise<Record<string, unknown>[]> {
    const result = (await this.transport.send('inodes.search', {
      pattern,
      path,
      limit,
    })) as Record<string, unknown>;

    return (Array.isArray(result.data) ? result.data : []) as Record<string, unknown>[];
  }

  async recents(path = '~/brain', limit = 20, days = 7): Promise<Record<string, unknown>[]> {
    const result = (await this.transport.send('inodes.recents', {
      path,
      limit,
      days,
    })) as Record<string, unknown>;

    return (Array.isArray(result.data) ? result.data : []) as Record<string, unknown>[];
  }
}

export class MachineConnection {
  readonly shell: MachineShell;
  readonly filesystem: MachineFilesystem;

  constructor(readonly id: string, private readonly transport: MachineTransport) {
    this.shell = new MachineShell(transport);
    this.filesystem = new MachineFilesystem(transport);
  }

  on(event: string, handler: (data: unknown) => void): () => void {
    return this.transport.on(event, handler);
  }

  emit(method: string, params: Record<string, unknown>): Promise<void> {
    return this.transport.emit(method, params);
  }

  async close(): Promise<void> {
    await this.transport.close();
  }
}

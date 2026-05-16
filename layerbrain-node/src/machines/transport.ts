import { randomUUID } from 'node:crypto';
import WebSocket from 'ws';
import { ConnectionError, MachineError, TimeoutError } from '../core/errors.js';

export interface TransportMessage {
  id?: string;
  method?: string;
  body?: Record<string, unknown>;
  data?: unknown;
  error?: { type?: string; message?: string };
  event?: string;
}

export interface SendOptions {
  body?: Record<string, unknown>;
  timeout?: number;
  signal?: AbortSignal;
}

type PendingRequest = {
  resolve: (value: unknown) => void;
  reject: (error: Error) => void;
  timeout: NodeJS.Timeout;
  cleanup: () => void;
};

export class MachineTransport {
  private readonly pending = new Map<string, PendingRequest>();
  private readonly eventHandlers = new Map<string, Set<(data: unknown) => void>>();
  private closing = false;

  constructor(private readonly socket: WebSocket) {
    this.socket.on('message', (data) => {
      this.handleMessage(typeof data === 'string' ? data : data.toString('utf8'));
    });

    this.socket.on('close', () => {
      if (!this.closing) {
        this.rejectAll(new ConnectionError('WebSocket connection closed'));
      }
    });

    this.socket.on('error', (error) => {
      this.rejectAll(new ConnectionError(`WebSocket error: ${error.message}`));
    });
  }

  static async connect(
    url: string,
    headers: Record<string, string> = {},
    timeout = 10_000,
  ): Promise<MachineTransport> {
    const socket = new WebSocket(url, { headers });

    await new Promise<void>((resolve, reject) => {
      const timer = setTimeout(() => {
        socket.terminate();
        reject(new TimeoutError(`Machine connection timed out after ${timeout}ms`));
      }, timeout);

      socket.once('open', () => {
        clearTimeout(timer);
        resolve();
      });

      socket.once('error', (error) => {
        clearTimeout(timer);
        reject(new ConnectionError(`Machine connection failed: ${error.message}`));
      });
    });

    return new MachineTransport(socket);
  }

  on(event: string, handler: (data: unknown) => void): () => void {
    const handlers = this.eventHandlers.get(event) ?? new Set<(data: unknown) => void>();
    handlers.add(handler);
    this.eventHandlers.set(event, handlers);

    return () => {
      const current = this.eventHandlers.get(event);
      current?.delete(handler);
      if (current && current.size === 0) {
        this.eventHandlers.delete(event);
      }
    };
  }

  async send(method: string, options: SendOptions = {}): Promise<unknown> {
    const { body = {}, timeout = 30_000, signal } = options;
    if (signal?.aborted) {
      throw new ConnectionError(`Request aborted: ${method}`);
    }

    const id = randomUUID();

    const responsePromise = new Promise<unknown>((resolve, reject) => {
      const timeoutHandle = setTimeout(() => {
        const request = this.pending.get(id);
        this.pending.delete(id);
        request?.cleanup();
        this.socket.terminate();
        reject(new TimeoutError(`Request timed out: ${method}`));
      }, timeout);
      timeoutHandle.unref?.();
      const abort = () => {
        this.pending.delete(id);
        clearTimeout(timeoutHandle);
        signal?.removeEventListener('abort', abort);
        this.socket.terminate();
        reject(new ConnectionError(`Request aborted: ${method}`));
      };
      signal?.addEventListener('abort', abort, { once: true });

      this.pending.set(id, {
        resolve,
        reject,
        timeout: timeoutHandle,
        cleanup: () => signal?.removeEventListener('abort', abort),
      });
    });

    await this.sendRaw({ id, method, body });
    return responsePromise;
  }

  async emit(method: string, body: Record<string, unknown> = {}): Promise<void> {
    await this.sendRaw({ method, body });
  }

  async close(timeout = 1_000): Promise<void> {
    this.closing = true;
    this.rejectAll(new ConnectionError('WebSocket transport closed'));

    if (this.socket.readyState === WebSocket.CLOSED) {
      return;
    }

    await new Promise<void>((resolve) => {
      let settled = false;
      const finish = () => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        this.socket.off('close', finish);
        resolve();
      };
      const timer = setTimeout(() => {
        if (this.socket.readyState !== WebSocket.CLOSED) {
          this.socket.terminate();
        }
        finish();
      }, timeout);
      timer.unref?.();

      this.socket.once('close', finish);
      if (this.socket.readyState === WebSocket.OPEN) {
        this.socket.close();
      } else {
        this.socket.terminate();
      }
    });
  }

  private async sendRaw(message: TransportMessage): Promise<void> {
    if (this.socket.readyState !== WebSocket.OPEN) {
      throw new ConnectionError('WebSocket is not open');
    }

    await new Promise<void>((resolve, reject) => {
      this.socket.send(JSON.stringify(message), (error) => {
        if (error) {
          reject(new ConnectionError(`WebSocket send failed: ${error.message}`));
          return;
        }
        resolve();
      });
    });
  }

  private handleMessage(raw: string): void {
    let message: TransportMessage;

    try {
      message = JSON.parse(raw) as TransportMessage;
    } catch {
      return;
    }

    if (message.id && this.pending.has(message.id)) {
      const request = this.pending.get(message.id);
      if (!request) {
        return;
      }

      this.pending.delete(message.id);
      clearTimeout(request.timeout);
      request.cleanup();

      if (message.error) {
        request.reject(
          new MachineError(
            message.error.type ?? 'error',
            message.error.message ?? 'Machine operation failed',
          ),
        );
        return;
      }

      request.resolve(message.data);
      return;
    }

    if (message.event) {
      const handlers = this.eventHandlers.get(message.event);
      if (!handlers) {
        return;
      }

      for (const handler of handlers) {
        handler(message.data);
      }
    }
  }

  private rejectAll(error: Error): void {
    for (const [id, request] of this.pending) {
      this.pending.delete(id);
      clearTimeout(request.timeout);
      request.cleanup();
      request.reject(error);
    }
  }
}

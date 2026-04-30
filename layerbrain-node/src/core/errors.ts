export class LayerbrainError extends Error {
  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class APIError extends LayerbrainError {
  readonly statusCode: number;
  readonly errorType?: string;
  readonly body?: unknown;

  constructor(
    message: string,
    options: {
      statusCode: number;
      errorType?: string;
      body?: unknown;
    },
  ) {
    super(message);
    this.statusCode = options.statusCode;
    this.errorType = options.errorType;
    this.body = options.body;
  }
}

export class ValidationError extends APIError {
  constructor(message = 'Validation failed', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 400, errorType: 'validation_error' });
  }
}

export class AuthenticationError extends APIError {
  constructor(message = 'Authentication failed', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 401, errorType: 'authentication_error' });
  }
}

export class InsufficientFundsError extends APIError {
  constructor(message = 'Insufficient funds', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 402, errorType: 'insufficient_funds' });
  }
}

export class PermissionDeniedError extends APIError {
  constructor(message = 'Permission denied', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 403, errorType: 'authorization_error' });
  }
}

export class NotFoundError extends APIError {
  constructor(message = 'Resource not found', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 404, errorType: 'not_found' });
  }
}

export class MethodNotAllowedError extends APIError {
  constructor(message = 'Method not allowed', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 405, errorType: 'method_not_allowed' });
  }
}

export class ConflictError extends APIError {
  constructor(message = 'Conflict', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 409, errorType: 'conflict' });
  }
}

export class RateLimitError extends APIError {
  constructor(message = 'Rate limit exceeded', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 429, errorType: 'rate_limit_exceeded' });
  }
}

export class InternalServerError extends APIError {
  constructor(message = 'Internal server error', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 500, errorType: 'internal_error' });
  }
}

export class ProviderError extends APIError {
  constructor(message = 'Provider error', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 502, errorType: 'provider_error' });
  }
}

export class CapacityError extends APIError {
  constructor(message = 'No capacity available', options: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'> = {}) {
    super(message, { ...options, statusCode: 503, errorType: 'capacity_error' });
  }
}

export class ConnectionError extends LayerbrainError {}

export class TimeoutError extends LayerbrainError {}

export class MachineError extends LayerbrainError {
  readonly errorType: string;

  constructor(errorType: string, message: string) {
    super(`${errorType}: ${message}`);
    this.errorType = errorType;
  }
}

type APIErrorCtor = new (
  message?: string,
  options?: Omit<ConstructorParameters<typeof APIError>[1], 'statusCode' | 'errorType'>,
) => APIError;

const STATUS_CODE_TO_EXCEPTION: Record<number, APIErrorCtor> = {
  400: ValidationError,
  401: AuthenticationError,
  402: InsufficientFundsError,
  403: PermissionDeniedError,
  404: NotFoundError,
  405: MethodNotAllowedError,
  409: ConflictError,
  429: RateLimitError,
  500: InternalServerError,
  502: ProviderError,
  503: CapacityError,
};

const ERROR_TYPE_TO_EXCEPTION: Record<string, APIErrorCtor> = {
  validation_error: ValidationError,
  invalid_request_error: ValidationError,
  invalid_request: ValidationError,
  bad_request: ValidationError,
  authentication_error: AuthenticationError,
  authentication_failed: AuthenticationError,
  expired: AuthenticationError,
  insufficient_funds: InsufficientFundsError,
  amount_exceeded: InsufficientFundsError,
  subscription_error: InsufficientFundsError,
  authorization_error: PermissionDeniedError,
  forbidden: PermissionDeniedError,
  not_found: NotFoundError,
  object_not_found: NotFoundError,
  method_not_allowed: MethodNotAllowedError,
  rate_limit_exceeded: RateLimitError,
  internal_error: InternalServerError,
  internal_server_error: InternalServerError,
  server_error: InternalServerError,
  event_creation_failed: InternalServerError,
  stripe_error: InternalServerError,
  provider_error: ProviderError,
  capacity_error: CapacityError,
};

export function raiseForStatus(statusCode: number, body: unknown): void {
  if (statusCode >= 200 && statusCode < 300) {
    return;
  }

  const payload = typeof body === 'object' && body !== null ? (body as Record<string, unknown>) : {};
  const errorBlock =
    typeof payload.error === 'object' && payload.error !== null ? (payload.error as Record<string, unknown>) : {};

  const message =
    (typeof errorBlock.message === 'string' && errorBlock.message) ||
    (typeof payload.message === 'string' && payload.message) ||
    `HTTP ${statusCode}`;

  const errorType = typeof errorBlock.type === 'string' ? errorBlock.type : undefined;

  const ErrorCtor =
    (errorType ? ERROR_TYPE_TO_EXCEPTION[errorType] : undefined) ?? STATUS_CODE_TO_EXCEPTION[statusCode];

  if (!ErrorCtor) {
    throw new APIError(message, { statusCode, errorType, body });
  }

  throw new ErrorCtor(message, { body });
}

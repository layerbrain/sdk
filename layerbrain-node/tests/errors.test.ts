import { describe, expect, it } from 'vitest';
import {
  APIError,
  AuthenticationError,
  NotFoundError,
  ValidationError,
  raiseForStatus,
} from '../src/core/errors.js';

describe('raiseForStatus', () => {
  it('does not throw on successful statuses', () => {
    expect(() => raiseForStatus(200, {})).not.toThrow();
    expect(() => raiseForStatus(201, {})).not.toThrow();
  });

  it('maps 400 validation errors', () => {
    expect(() =>
      raiseForStatus(400, {
        error: { type: 'validation_error', message: 'model is required' },
      }),
    ).toThrow(ValidationError);
  });

  it('maps 401 auth errors', () => {
    expect(() =>
      raiseForStatus(401, {
        error: { type: 'authentication_failed', message: 'Invalid token' },
      }),
    ).toThrow(AuthenticationError);
  });

  it('maps 404 not found errors', () => {
    expect(() =>
      raiseForStatus(404, {
        error: { type: 'not_found', message: 'Not found' },
      }),
    ).toThrow(NotFoundError);
  });

  it('falls back to generic api error for unknown statuses', () => {
    try {
      raiseForStatus(418, { error: { type: 'teapot', message: "I'm a teapot" } });
      throw new Error('expected throw');
    } catch (error) {
      expect(error).toBeInstanceOf(APIError);
      const apiError = error as APIError;
      expect(apiError.statusCode).toBe(418);
      expect(apiError.errorType).toBe('teapot');
    }
  });
});

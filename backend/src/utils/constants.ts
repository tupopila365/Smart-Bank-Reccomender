export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
} as const;

export const ERROR_MESSAGES = {
  VALIDATION_ERROR: 'Validation error',
  ML_SERVICE_ERROR: 'ML service communication error',
  INTERNAL_ERROR: 'Internal server error',
  NOT_FOUND: 'Resource not found',
} as const;

import axios, { AxiosInstance, AxiosError } from 'axios';
import logger from '../utils/logger';
import { UserProfile, RecommendationResponse } from '../types';

class MLServiceClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.ML_SERVICE_URL || 'http://localhost:8000';
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    logger.info(`ML Service client initialized with URL: ${this.baseURL}`);
  }

  async predict(profile: UserProfile): Promise<RecommendationResponse> {
    try {
      logger.info('Sending prediction request to ML Service', { profile });

      const response = await this.client.post<RecommendationResponse>('/predict', profile);

      logger.info('Received prediction response from ML Service', {
        data: response.data,
      });

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        logger.error('ML Service communication error', {
          message: axiosError.message,
          status: axiosError.response?.status,
          data: axiosError.response?.data,
        });

        throw new Error(`ML Service error: ${axiosError.message}`);
      }

      logger.error('Unexpected error during ML Service communication', { error });
      throw new Error('Unexpected error communicating with ML Service');
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.status === 200;
    } catch (error) {
      logger.error('ML Service health check failed', { error });
      return false;
    }
  }
}

export default new MLServiceClient();

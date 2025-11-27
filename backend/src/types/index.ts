export interface UserProfile {
  income: number;
  spending_score: number;
  saving_frequency: number;
  loan_behavior: number;
}

export interface RecommendationResponse {
  recommended_account: string;
  recommended_savings: string;
  recommended_loan: string;
  recommended_digital_service: string;
  cluster_segment: number;
}

export interface ApiResponse {
  success: boolean;
  message?: string;
  data?: any;
}

export interface UsageLog {
  user_id: number;
  action: string;
  metadata: Record<string, any>;
}

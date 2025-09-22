export interface Store {
  store_id: string;
  name: string;
  latitude: number;
  longitude: number;
  address: string;
  is_linked: boolean;
  offer_type: 'review_photo' | 'review_text' | 'both';
}

export interface User {
  user_id: string;
  email: string;
  name: string;
  points: number;
  created_at: string;
}

export interface Review {
  review_id: string;
  user_id: string;
  store_id: string;
  rating: number;
  text: string;
  images: string[];
  target_platforms: Platform[];
  points_earned: number;
  created_at: string;
  status: 'pending' | 'approved' | 'rejected';
}

export interface Platform {
  platform_id: string;
  name: 'Google' | 'Naver' | 'Kakao' | 'TripAdvisor';
  url?: string;
}

export interface PointsTransaction {
  transaction_id: string;
  user_id: string;
  type: 'earned' | 'redeemed';
  amount: number;
  description: string;
  created_at: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
}

export interface StoreState {
  stores: Store[];
  selectedStore: Store | null;
  loading: boolean;
  error: string | null;
}

export interface ReviewState {
  reviews: Review[];
  loading: boolean;
  error: string | null;
}

export interface PointsState {
  balance: number;
  transactions: PointsTransaction[];
  loading: boolean;
  error: string | null;
}

export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
  Login: undefined;
  Register: undefined;
  StoreDetail: { store: Store };
  ReviewForm: { store: Store };
  Camera: { onPhotoTaken: (uri: string) => void };
};

export type MainTabParamList = {
  Home: undefined;
  Search: undefined;
  Review: undefined;
  Points: undefined;
  Profile: undefined;
};
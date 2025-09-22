import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ReviewState, Review } from '@/types';

const initialState: ReviewState = {
  reviews: [],
  loading: false,
  error: null,
};

const reviewSlice = createSlice({
  name: 'review',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
      if (action.payload) {
        state.error = null;
      }
    },
    setReviews: (state, action: PayloadAction<Review[]>) => {
      state.reviews = action.payload;
      state.loading = false;
      state.error = null;
    },
    addReview: (state, action: PayloadAction<Review>) => {
      state.reviews.unshift(action.payload);
    },
    updateReview: (state, action: PayloadAction<Review>) => {
      const index = state.reviews.findIndex(
        (review) => review.review_id === action.payload.review_id
      );
      if (index !== -1) {
        state.reviews[index] = action.payload;
      }
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  setLoading,
  setReviews,
  addReview,
  updateReview,
  setError,
  clearError,
} = reviewSlice.actions;
export default reviewSlice.reducer;
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { PointsState, PointsTransaction } from '@/types';

const initialState: PointsState = {
  balance: 0,
  transactions: [],
  loading: false,
  error: null,
};

const pointsSlice = createSlice({
  name: 'points',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
      if (action.payload) {
        state.error = null;
      }
    },
    setBalance: (state, action: PayloadAction<number>) => {
      state.balance = action.payload;
    },
    setTransactions: (state, action: PayloadAction<PointsTransaction[]>) => {
      state.transactions = action.payload;
      state.loading = false;
      state.error = null;
    },
    addTransaction: (state, action: PayloadAction<PointsTransaction>) => {
      state.transactions.unshift(action.payload);
      // Update balance based on transaction type
      if (action.payload.type === 'earned') {
        state.balance += action.payload.amount;
      } else {
        state.balance -= action.payload.amount;
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
  setBalance,
  setTransactions,
  addTransaction,
  setError,
  clearError,
} = pointsSlice.actions;
export default pointsSlice.reducer;
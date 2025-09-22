import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { StoreState, Store } from '@/types';

const initialState: StoreState = {
  stores: [],
  selectedStore: null,
  loading: false,
  error: null,
};

const storeSlice = createSlice({
  name: 'store',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
      if (action.payload) {
        state.error = null;
      }
    },
    setStores: (state, action: PayloadAction<Store[]>) => {
      state.stores = action.payload;
      state.loading = false;
      state.error = null;
    },
    setSelectedStore: (state, action: PayloadAction<Store | null>) => {
      state.selectedStore = action.payload;
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
  setStores,
  setSelectedStore,
  setError,
  clearError,
} = storeSlice.actions;
export default storeSlice.reducer;
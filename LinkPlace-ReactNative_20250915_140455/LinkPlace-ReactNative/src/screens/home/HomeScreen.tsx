import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  FlatList,
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { setStores } from '@/store/slices/storeSlice';
import { Card } from '@/components/common';
import { theme } from '@/theme';
import { Store } from '@/types';

const HomeScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { stores } = useSelector((state: RootState) => state.store);
  const [nearbyStores, setNearbyStores] = useState<Store[]>([]);

  useEffect(() => {
    // Mock fetch nearby stores
    const mockStores: Store[] = [
      {
        store_id: 'store-1',
        name: '강남 커피',
        latitude: 37.4979,
        longitude: 127.0276,
        address: '서울 강남구',
        is_linked: true,
        offer_type: 'review_photo',
      },
      {
        store_id: 'store-2',
        name: '홍대 레스토랑',
        latitude: 37.5507,
        longitude: 126.9234,
        address: '서울 마포구',
        is_linked: true,
        offer_type: 'review_text',
      },
    ];

    dispatch(setStores(mockStores));
    setNearbyStores(mockStores);
  }, [dispatch]);

  const renderStoreItem = ({ item }: { item: Store }) => (
    <Card style={styles.storeCard}>
      <Text style={styles.storeName}>{item.name}</Text>
      <Text style={styles.storeAddress}>{item.address}</Text>
      <View style={styles.offerBadge}>
        <Text style={styles.offerText}>
          {item.offer_type === 'review_photo' ? '사진 리뷰' : '텍스트 리뷰'}
        </Text>
      </View>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.greeting}>안녕하세요, {user?.name}님!</Text>
          <Text style={styles.points}>{user?.points || 0} P</Text>
        </View>

        <Card style={styles.statsCard}>
          <Text style={styles.statsTitle}>이번 주 활동</Text>
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>5</Text>
              <Text style={styles.statLabel}>작성한 리뷰</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>250</Text>
              <Text style={styles.statLabel}>획득한 포인트</Text>
            </View>
          </View>
        </Card>

        <Text style={styles.sectionTitle}>내 주변 매장</Text>

        <FlatList
          data={nearbyStores}
          renderItem={renderStoreItem}
          keyExtractor={(item) => item.store_id}
          scrollEnabled={false}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  content: {
    flex: 1,
    padding: theme.spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  greeting: {
    ...theme.typography.h3,
    color: theme.colors.textPrimary,
  },
  points: {
    ...theme.typography.h4,
    color: theme.colors.primary,
    fontWeight: 'bold',
  },
  statsCard: {
    marginBottom: theme.spacing.lg,
  },
  statsTitle: {
    ...theme.typography.h4,
    marginBottom: theme.spacing.md,
    color: theme.colors.textPrimary,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    ...theme.typography.h2,
    color: theme.colors.primary,
    fontWeight: 'bold',
  },
  statLabel: {
    ...theme.typography.body2,
    color: theme.colors.textSecondary,
  },
  sectionTitle: {
    ...theme.typography.h4,
    marginBottom: theme.spacing.md,
    color: theme.colors.textPrimary,
  },
  storeCard: {
    marginBottom: theme.spacing.sm,
  },
  storeName: {
    ...theme.typography.h4,
    marginBottom: theme.spacing.xs,
    color: theme.colors.textPrimary,
  },
  storeAddress: {
    ...theme.typography.body2,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.sm,
  },
  offerBadge: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.sm,
    alignSelf: 'flex-start',
  },
  offerText: {
    ...theme.typography.caption,
    color: theme.colors.white,
    fontWeight: '600',
  },
});

export default HomeScreen;
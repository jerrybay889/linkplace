import React from 'react';
import { View, Text, StyleSheet, SafeAreaView } from 'react-native';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import { Card } from '@/components/common';
import { theme } from '@/theme';

const PointsScreen: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>포인트</Text>

        <Card style={styles.pointsCard}>
          <Text style={styles.pointsLabel}>보유 포인트</Text>
          <Text style={styles.pointsValue}>{user?.points || 0} P</Text>
        </Card>

        <Text style={styles.subtitle}>포인트 사용 내역</Text>
        <Text style={styles.emptyText}>아직 사용 내역이 없습니다.</Text>
      </View>
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
  title: {
    ...theme.typography.h2,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
  },
  pointsCard: {
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  pointsLabel: {
    ...theme.typography.body1,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.sm,
  },
  pointsValue: {
    ...theme.typography.h1,
    color: theme.colors.primary,
    fontWeight: 'bold',
  },
  subtitle: {
    ...theme.typography.h4,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.md,
  },
  emptyText: {
    ...theme.typography.body2,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginTop: theme.spacing.xl,
  },
});

export default PointsScreen;
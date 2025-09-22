import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useDispatch } from 'react-redux';
import { loginSuccess } from '@/store/slices/authSlice';
import { Button, Input } from '@/components/common';
import { theme } from '@/theme';

const LoginScreen: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('오류', '이메일과 비밀번호를 입력해주세요.');
      return;
    }

    setLoading(true);

    try {
      // Mock login API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      const mockUser = {
        user_id: '1',
        email: email,
        name: '사용자',
        points: 1000,
        created_at: new Date().toISOString(),
      };

      dispatch(loginSuccess({
        user: mockUser,
        token: 'mock-jwt-token',
      }));
    } catch (error) {
      Alert.alert('로그인 실패', '이메일 또는 비밀번호를 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>링크플레이스에 오신 것을 환영합니다</Text>
        <Text style={styles.subtitle}>로그인하여 리뷰를 작성하고 포인트를 적립하세요</Text>

        <View style={styles.form}>
          <Input
            label="이메일"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            placeholder="이메일을 입력하세요"
          />

          <Input
            label="비밀번호"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            placeholder="비밀번호를 입력하세요"
          />

          <Button
            title={loading ? "로그인 중..." : "로그인"}
            onPress={handleLogin}
            disabled={loading}
          />
        </View>

        <TouchableOpacity style={styles.registerLink}>
          <Text style={styles.registerText}>
            계정이 없으신가요? <Text style={styles.registerLinkText}>회원가입</Text>
          </Text>
        </TouchableOpacity>
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
    padding: theme.spacing.lg,
    justifyContent: 'center',
  },
  title: {
    ...theme.typography.h2,
    textAlign: 'center',
    marginBottom: theme.spacing.sm,
    color: theme.colors.textPrimary,
  },
  subtitle: {
    ...theme.typography.body1,
    textAlign: 'center',
    marginBottom: theme.spacing.xxl,
    color: theme.colors.textSecondary,
  },
  form: {
    marginBottom: theme.spacing.xl,
  },
  registerLink: {
    alignItems: 'center',
  },
  registerText: {
    ...theme.typography.body2,
    color: theme.colors.textSecondary,
  },
  registerLinkText: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
});

export default LoginScreen;
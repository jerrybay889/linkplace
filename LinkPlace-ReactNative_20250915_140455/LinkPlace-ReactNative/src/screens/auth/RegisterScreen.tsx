import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Button, Input } from '@/components/common';
import { theme } from '@/theme';

const RegisterScreen: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!name || !email || !password || !confirmPassword) {
      Alert.alert('오류', '모든 필드를 입력해주세요.');
      return;
    }

    if (password !== confirmPassword) {
      Alert.alert('오류', '비밀번호가 일치하지 않습니다.');
      return;
    }

    setLoading(true);

    try {
      // Mock register API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      Alert.alert('회원가입 완료', '회원가입이 완료되었습니다. 로그인해주세요.');
    } catch (error) {
      Alert.alert('회원가입 실패', '다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>회원가입</Text>
        <Text style={styles.subtitle}>새 계정을 만들어 시작하세요</Text>

        <View style={styles.form}>
          <Input
            label="이름"
            value={name}
            onChangeText={setName}
            placeholder="이름을 입력하세요"
          />

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

          <Input
            label="비밀번호 확인"
            value={confirmPassword}
            onChangeText={setConfirmPassword}
            secureTextEntry
            placeholder="비밀번호를 다시 입력하세요"
          />

          <Button
            title={loading ? "가입 중..." : "회원가입"}
            onPress={handleRegister}
            disabled={loading}
          />
        </View>

        <TouchableOpacity style={styles.loginLink}>
          <Text style={styles.loginText}>
            이미 계정이 있으신가요? <Text style={styles.loginLinkText}>로그인</Text>
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
  loginLink: {
    alignItems: 'center',
  },
  loginText: {
    ...theme.typography.body2,
    color: theme.colors.textSecondary,
  },
  loginLinkText: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
});

export default RegisterScreen;
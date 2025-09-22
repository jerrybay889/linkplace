import React from 'react';
import { Card, Form, Input, Button, Switch, Space, Divider } from 'antd';

const Settings: React.FC = () => {
  const onFinish = (values: any) => {
    console.log('Settings saved:', values);
  };

  return (
    <Card title="계정 설정">
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item label="업체명" name="companyName" initialValue="ABC 카페">
          <Input />
        </Form.Item>

        <Form.Item label="담당자 이메일" name="email" initialValue="manager@abc-cafe.com">
          <Input type="email" />
        </Form.Item>

        <Form.Item label="연락처" name="phone" initialValue="02-1234-5678">
          <Input />
        </Form.Item>

        <Divider />

        <Form.Item label="리뷰 알림" name="reviewNotification" valuePropName="checked" initialValue={true}>
          <Switch />
        </Form.Item>

        <Form.Item label="캠페인 자동 승인" name="autoApproval" valuePropName="checked" initialValue={false}>
          <Switch />
        </Form.Item>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit">저장</Button>
            <Button>취소</Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default Settings;

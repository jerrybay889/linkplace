import React from 'react';
import { Card, Form, Input, Button, Switch, Space, Divider } from 'antd';

const Settings: React.FC = () => {
  const onFinish = (values: any) => {
    console.log('Settings saved:', values);
  };

  return (
    <div>
      <Card title="시스템 설정">
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item label="사이트 이름" name="siteName" initialValue="LinkPlace">
            <Input />
          </Form.Item>

          <Form.Item label="관리자 이메일" name="adminEmail" initialValue="admin@linkplace.com">
            <Input type="email" />
          </Form.Item>

          <Divider />

          <Form.Item label="신규 사용자 자동 승인" name="autoApproval" valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>

          <Form.Item label="이메일 알림" name="emailNotification" valuePropName="checked" initialValue={false}>
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
    </div>
  );
};

export default Settings;

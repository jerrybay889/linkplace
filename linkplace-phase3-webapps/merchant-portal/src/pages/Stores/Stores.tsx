import React, { useState } from 'react';
import { Card, Table, Button, Space, Tag, Modal, Form, Input, Select, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons';

const Stores: React.FC = () => {
  const [stores, setStores] = useState([
    {
      key: 1,
      id: 1,
      name: '강남 본점',
      address: '서울 강남구 테헤란로 123',
      category: '카페',
      phone: '02-1234-5678',
      status: 'active',
      rating: 4.5,
      reviewCount: 128,
    },
    {
      key: 2,
      id: 2,
      name: '홍대 지점',
      address: '서울 마포구 홍익로 456',
      category: '카페',
      phone: '02-8765-4321',
      status: 'active',
      rating: 4.3,
      reviewCount: 95,
    },
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const columns = [
    { title: '매장명', dataIndex: 'name', key: 'name' },
    { title: '주소', dataIndex: 'address', key: 'address' },
    { title: '카테고리', dataIndex: 'category', key: 'category', 
      render: (category: string) => <Tag>{category}</Tag>
    },
    { title: '연락처', dataIndex: 'phone', key: 'phone' },
    { title: '평점', dataIndex: 'rating', key: 'rating',
      render: (rating: number) => `⭐ ${rating}`
    },
    { title: '리뷰수', dataIndex: 'reviewCount', key: 'reviewCount',
      render: (count: number) => `${count}개`
    },
    { 
      title: '상태', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '운영중' : '중단'}
        </Tag>
      )
    },
    {
      title: '작업',
      key: 'actions',
      render: (record: any) => (
        <Space>
          <Button type="text" icon={<EyeOutlined />} />
          <Button type="text" icon={<EditOutlined />} />
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Space>
      ),
    },
  ];

  return (
    <Card title="매장 관리" 
          extra={
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalVisible(true)}>
              매장 등록
            </Button>
          }>

      <Table columns={columns} dataSource={stores} />

      <Modal
        title="매장 등록"
        open={isModalVisible}
        onOk={() => form.submit()}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="매장명" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="address" label="주소" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="category" label="카테고리" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="카페">카페</Select.Option>
              <Select.Option value="음식점">음식점</Select.Option>
              <Select.Option value="쇼핑">쇼핑</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="phone" label="연락처">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Stores;

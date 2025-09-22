import React, { useState, useEffect } from 'react';
import { Table, Card, Button, Input, Space, Tag, Avatar, Modal, Form, message } from 'antd';
import { UserOutlined, EditOutlined, DeleteOutlined, PlusOutlined, SearchOutlined } from '@ant-design/icons';

const Users: React.FC = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchText, setSearchText] = useState('');
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    // 모의 데이터 로딩
    setTimeout(() => {
      const mockUsers = Array.from({ length: 50 }, (_, i) => ({
        key: i + 1,
        id: i + 1,
        name: `사용자${i + 1}`,
        email: `user${i + 1}@example.com`,
        phone: `010-${String(Math.floor(Math.random() * 9000) + 1000)}-${String(Math.floor(Math.random() * 9000) + 1000)}`,
        joinDate: new Date(2024, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28) + 1).toLocaleDateString(),
        status: Math.random() > 0.3 ? 'active' : 'inactive',
        reviewCount: Math.floor(Math.random() * 50),
        level: ['브론즈', '실버', '골드', '플래티넘'][Math.floor(Math.random() * 4)],
      }));
      setUsers(mockUsers);
      setLoading(false);
    }, 1000);
  }, []);

  const columns = [
    {
      title: '사용자',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: any) => (
        <Space>
          <Avatar icon={<UserOutlined />} />
          <div>
            <div>{text}</div>
            <div style={{ fontSize: '12px', color: '#666' }}>{record.email}</div>
          </div>
        </Space>
      ),
    },
    {
      title: '연락처',
      dataIndex: 'phone',
      key: 'phone',
    },
    {
      title: '가입일',
      dataIndex: 'joinDate',
      key: 'joinDate',
    },
    {
      title: '등급',
      dataIndex: 'level',
      key: 'level',
      render: (level: string) => {
        const colors = { 브론즈: 'orange', 실버: 'gray', 골드: 'gold', 플래티넘: 'purple' };
        return <Tag color={colors[level]}>{level}</Tag>;
      },
    },
    {
      title: '리뷰수',
      dataIndex: 'reviewCount',
      key: 'reviewCount',
      render: (count: number) => <span>{count}개</span>,
    },
    {
      title: '상태',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '활성' : '비활성'}
        </Tag>
      ),
    },
    {
      title: '작업',
      key: 'actions',
      render: (record: any) => (
        <Space>
          <Button type="text" icon={<EditOutlined />} onClick={() => handleEdit(record)} />
          <Button type="text" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)} />
        </Space>
      ),
    },
  ];

  const handleEdit = (record: any) => {
    form.setFieldsValue(record);
    setIsModalVisible(true);
  };

  const handleDelete = (id: number) => {
    Modal.confirm({
      title: '사용자를 삭제하시겠습니까?',
      content: '삭제된 사용자는 복구할 수 없습니다.',
      okText: '삭제',
      cancelText: '취소',
      onOk: () => {
        setUsers(users.filter(user => user.id !== id));
        message.success('사용자가 삭제되었습니다.');
      },
    });
  };

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchText.toLowerCase()) ||
    user.email.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <Card title="사용자 관리" 
          extra={
            <Button type="primary" icon={<PlusOutlined />}>
              사용자 추가
            </Button>
          }>
      <Space style={{ marginBottom: 16 }}>
        <Input
          placeholder="사용자 검색"
          prefix={<SearchOutlined />}
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          style={{ width: 300 }}
        />
      </Space>

      <Table
        columns={columns}
        dataSource={filteredUsers}
        loading={loading}
        pagination={{
          pageSize: 10,
          showSizeChanger: true,
          showTotal: (total) => `총 ${total}명`,
        }}
      />

      <Modal
        title="사용자 정보 수정"
        open={isModalVisible}
        onOk={() => form.submit()}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="이름" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="email" label="이메일" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="phone" label="연락처">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Users;
